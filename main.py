import datetime

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
        publics=Budget.query.filter_by(public=True)
        privates=Budget.query.filter_by(public=False, school=2)
        return render_template( "index.html", public_budgets=publics, private_budgets=privates) 

@app.route('/presupuesto/crear', methods=["GET", "POST"])
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
        school = request.form.get('school')
        public = True if request.form.getlist('publico') else False

        # Si se ha especificado el nombre y la escuela se crea el presupuesto
        if name and school:
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


@app.route('/presupuesto/editar/<int:id>', methods=["GET", "POST"])
def budget_edit(id):
    """
    Edita el presupuesto elegido
    """
    # Obtiene el presupuesto de la base de datos
    budget = Budget.query.get(id)
    if request.method == "GET":
        res = requests.get(url_api)
        schools = res.json()
        public_str = 'true' if budget.public is True else 'false'
        return render_template("budget_edit.html",
                               schools=schools,
                               budget=budget,
                               public=public_str,
                               id=id)

    else:
        nombre = request.form.get('name')
        escuela = request.form.get('school')
        publico = True if request.form.getlist('public') else False
        if nombre and escuela:
            budget = Budget.query.get(id)
            budget.name = nombre if nombre else budget.name
            budget.school = escuela if escuela else budget.school
            budget.public = publico if publico else budget.public
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
    schools = res.json()
    budget=Budget.query.get(id)
    return render_template("budget_show.html",
                           schools=schools,
                           budget=budget)
    


@app.route('/gasto/crear/<int:id>', methods=["GET", "POST"])
def expense_create(id):
    """
    Crea un gasto para el presupuesto 
    """
    if request.method == "GET":
        res = requests.get(url_api)
        schools = res.json()
        # Obtiene los presupuestos para el prestamo especificado
        budgets = Budget.query.get(id)
        return render_template("expense_create.html",
                               budgets=budgets,
                               schools=schools)

    else:
        amount = int(request.form['amount'])
        name = str(request.form['name'])
        budget_selected = request.form['budget']

        presupuesto = BudgetHeading.query.filter_by(name=budget_selected)
        school = (Budget.query.get(presupuesto.budget_id)).school
        expense = Expense(name,
                          school,
                          datetime.datetime.utcnow(),
                          datetime.datetime.utcnow(),
                          datetime.datetime.utcnow(),
                          amount,
                          False,
                          [],
                          '')# Observaciones en caso de haber
        db.session.add(gasto)
        db.session.commit()
        return render_template(
            "index.html", public_budgets=Budget.query.filter_by(
                public=True), private_budgets=Budget.query.filter_by(
                public=False))


@app.route('/gastos', methods=["GET", "POST"])
def get_expenses():
    """
    TODO: Obtener todos los gastos disponibles
    """
    if request.method == "GET":
        res = requests.get(url_api)
        schools = res.json()
        expenses = Expense.query.all()
        return render_template("expense_list.html",
                               expenses=expenses,
                               schools=schools)

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
