import datetime
import json

import requests

from flask import Flask, render_template, request
from models import Budget, Expense, BudgetHeading
from models.connection import db

# Inicializacion del objeto Flask
app = Flask(__name__)

# Generacion del dict (diccionario) de configuracion desde fichero
app.config.from_pyfile('config.cfg')

# Enlaza la aplicacion y la base de datos
db.app = app
db.init_app(app)
db.create_all()

url_api = 'https://delegacion.uc3m.es/dele_api/school'


@app.route('/', methods=["GET", "POST"])


@app.route('/index', methods=["GET", "POST"])
def index():
    """
    Pagina principal de la aplicacion
    Muestra presupuestos publicos y privados y redirecciona al resto de funcionalidades
    """
    if request.method == "GET":
        publics = Budget.query.filter_by(public=True)
        privates = Budget.query.filter_by(public=False, school=2)
        return render_template("index.html", public_budgets=publics, private_budgets=privates) 


@app.route('/presupuestos/crear', methods=["GET", "POST"])
def budget_create():
    """
    Crea presupuestos para una universidad.
    El presupuesto se guarda en Budget
    """
    if request.method == "GET":
        res = requests.get(url_api)
        schools = res.json()
        return render_template("budget_create.html", schools=schools)

    else:
        name = str(request.form['name'])
        school = int(request.form.get('school'))
        public = True if request.form.getlist('publico') else False

        # Si el presupuesto no existe se crea
        if Budget.query.filter_by(name=name, school=school).count() == 0:
            presupuesto = Budget(name,
                                 school,
                                 False,  # Por ahora la visibilidad esta desactivada
                                 public,
                                 [])
            db.session.add(presupuesto)
            db.session.commit()
            # Volver al inicio
            publics=Budget.query.filter_by(public=True)
            privates=Budget.query.filter_by(public=False, school=2)
            return render_template( "index.html", public_budgets=publics, private_budgets=privates) 
        # El presupuesto ya existe
        else:
            # Volver al inicio
            error = "El presupuesto creado ya existe"
            publics=Budget.query.filter_by(public=True)
            privates=Budget.query.filter_by(public=False, school=2)
            return render_template( "index.html", public_budgets=publics, private_budgets=privates, error=error) 


@app.route('/presupuestos/editar/<int:id>', methods=["GET", "POST"])
def budget_edit(id):
    """
    Edita el presupuesto elegido
    """
    # Obtiene el presupuesto de la base de datos
    budget = Budget.query.get(id)
    if request.method == "GET":
        res = requests.get(url_api)
        school = res.json()
        return render_template("budget_edit.html",
                               budget=budget,
                               school=school[1],
                               id=id)

    else:
        nombre = request.form['name']
        budget.name = nombre if nombre else budget.name
        db.session.commit()
        # Volver al inicio
        publics=Budget.query.filter_by(public=True)
        privates=Budget.query.filter_by(public=False, school=2)
        return render_template( "index.html", public_budgets=publics, private_budgets=privates) 


@app.route('/presupuestos', methods=["GET", "POST"])
def budget_list():
    """
    Muestra todos los presupuestos separados en publicos y privados
    Permite editar los presupuestos y añadir gastos
    """
    if request.method == "GET":
        res = requests.get(url_api)
        schools = res.json()
        publics=Budget.query.filter_by(public=True)
        privates=Budget.query.filter_by(public=False, school=2)
        return render_template("budget_list.html",
                               public_budgets=publics,
                               private_budgets=privates,
                               schools=schools)


@app.route('/presupuestos/<int:id>', methods=["GET"])
def budget_show(id):
    """
    Muesta la informacion sobre un presupuesto
    Muestra las partidas del presupuesto y permite añadir gastos y partidas
    """
    res = requests.get(url_api)
    budget=Budget.query.get(id)
    return render_template("budget_show.html",
                           headings=budget.budget_headings,
                           budget=budget)
    

@app.route('/partidas/crear/<int:id>', methods=["GET", "POST"])
def budget_heading_create(id):
    """
    Crea una partida para el presupuesto
    """
    if request.method == "GET":
        return render_template("budget_heading_create.html")
    else:
        # Creamos la partida
        name = request.form['name']
        amount = request.form["initial_amount"]
        # Si la partida no existe se crea
        if BudgetHeading.query.filter_by(name=name, initial_amount=amount).count() == 0:
            heading = BudgetHeading(id,
                                    name,
                                    amount)
            db.session.add(heading)
            db.session.commit()
            publics=Budget.query.filter_by(public=True)
            privates=Budget.query.filter_by(public=False, school=2)
            return render_template("index.html", 
                                   public_budgets=publics,
                                   private_budgets=privates) 
        # La partida ya existe
        else:
            error = "La partida creada ya existe"
            publics=Budget.query.filter_by(public=True)
            privates=Budget.query.filter_by(public=False, school=2)
            return render_template("index.html", 
                                   public_budgets=publics,
                                   private_budgets=privates,
                                   error=error) 


@app.route('/partidas/editar/<int:id>', methods=["GET", "POST"])
def budget_heading_edit(id):
    """
    Edita una partida
    """
    # Obtiene la partida de la base de datos
    heading = BudgetHeading.query.get(id)
    if request.method == "GET":
        res = requests.get(url_api)
        school = res.json()
        return render_template("budget_edit.html",
                               budget=heading,
                               id=id)
    else:
        nombre = request.form['name']
        heading.name = nombre if nombre else heading.name
        db.session.commit()
        # Volver al inicio
        publics=Budget.query.filter_by(public=True)
        privates=Budget.query.filter_by(public=False, school=2)
        return render_template("index.html", 
                               public_budgets=publics, 
                               private_budgets=privates) 


@app.route('/partidas/transferir/<int:id>', methods=["GET", "POST"])
def budget_heading_transfer(id):
    """
    Transfiere dinero entre dos partidas
    """
    budget = Budget.query.get(id)
    if request.method == "GET":
        return render_template("budget_heading_transfer.html",
                               headings=budget.budget_headings)
    else:
        # TODO: Crear gasto en la deudora e ingreso en la adeudada en vez de cambiar la cantidad inicial
        amount = int(request.form['amount'])
        from_heading_id = int(request.form.get('from_heading'))
        to_heading_id = int(request.form.get('to_heading'))
        from_heading = BudgetHeading.query.get(from_heading_id)
        to_heading = BudgetHeading.query.get(to_heading_id)

        # Gasto creado en la partida deudora
        # Todas las fechas del gasto se ponen al dia en el que se hace la transferencia
        from_expense = Expense(from_heading_id,
                               "Transferencia",
                               budget.school,
                               amount,
                               datetime.datetime.utcnow(),
                               datetime.datetime.utcnow(),
                               False,  # Revoked, por ahora es falso
                               datetime.datetime.utcnow(),
                               [],
                               "Transferencia a " + to_heading.name)

        # Ingreso creado en la partida adeudada
        to_expense = Expense(to_heading_id,
                             "Transferencia",
                             budget.school,
                             -amount,
                             datetime.datetime.utcnow(),
                             datetime.datetime.utcnow(),
                             False,  # Revoked, por ahora es falso
                             datetime.datetime.utcnow(),
                             [],
                             "Recibido de " + from_heading.name)

        db.session.add(from_expense)
        db.session.add(to_expense)
        db.session.commit()
        # Volvemos al inicio
        publics=Budget.query.filter_by(public=True)
        privates=Budget.query.filter_by(public=False, school=2)
        return render_template("index.html", 
                               public_budgets=publics,
                               private_budgets=privates)


@app.route('/gastos/crear/<int:id>', methods=["GET", "POST"])
def expense_create(id):
    """
    Crea un gasto para la partida
    """
    budget = Budget.query.get(id)
    if request.method == "GET":
        res = requests.get(url_api)
        # Obtiene la partida para el prestamo especificado
        # budget_heading = BudgetHeading.query.get(id)
        headings = budget.budget_headings
        return render_template("expense_create.html",
                               headings=headings,
                               budget=budget)

    else:
        amount = - int(request.form['amount'])
        name = str(request.form['name'])
        budget_heading_id = int(request.form.get("budget_heading"))
        register_date = request.form['register_date']
        add_date = request.form['add_date']
        expense_date = request.form['expense_date']

        partida = BudgetHeading.query.get(budget_heading_id)
        expense = Expense(budget_heading_id,
                          name,
                          budget.school,
                          amount,
                          expense_date,
                          add_date,
                          False,  # Revoked, por ahora es falso
                          register_date,
                          [],
                          "")# Observaciones en caso de haber
        print(amount)
        db.session.add(expense)
        db.session.commit()
        publics=Budget.query.filter_by(public=True)
        privates=Budget.query.filter_by(public=False, school=2)
        return render_template("index.html", 
                               public_budgets=publics,
                               private_budgets=privates)


@app.route('/gastos/<int:id>', methods=["GET", "POST"])
def expense_show(id):
    """
    Muestra los gastos de una partida
    """
    heading = BudgetHeading.query.get(id)
    expenses = Expense.query.filter_by(budgetheading_id=id)
    if request.method == "GET":
        res = requests.get(url_api)
        schools = res.json()
        return render_template("expense_list.html",
                               expenses=expenses)


@app.route('/gastos/editar/<int:id>', methods=["GET", "POST"])
def expense_edit(id):
    """
    Edita las observaciones de un gasto
    """
    # Obtiene el gasto de la base de datos
    expense = expense.query.get(id)
    if request.method == "GET":
        res = requests.get(url_api)
        school = res.json()
        return render_template("budget_edit.html",
                               budget=expense,
                               id=id)
    else:
        observations = request.form['observations']
        expense.observations = observations if observations else expense.observations
        db.session.commit()
        # Volver al inicio
        publics=Budget.query.filter_by(public=True)
        privates=Budget.query.filter_by(public=False, school=2)
        return render_template("index.html", 
                               public_budgets=publics, 
                               private_budgets=privates) 

@app.route('/estadisticas', methods=['GET'])
def get_statistics():
    """
    TODO: Crear estadistica para los presupuestos y los gastos
    """
    if request.method == 'GET':
        presupuestos = Budget.query.all()
        return render_template('statistics.html', budgets=presupuestos)


if __name__ == '__main__':
    app.run()
