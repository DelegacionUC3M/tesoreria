import datetime

import requests

from flask import Flask, render_template, request
from models import Budget, Expense
from models.connection import db

# Inicializacion del objeto Flask
app = Flask(__name__)

# Generacion del dict (diccionario) de configuracion desde fichero
app.config.from_pyfile('config.cfg')

# Enlaza la aplicacion y la base de datos
db.app = app
db.init_app(app)
db.create_all()

url_api = 'https://delegacion.uc3m.es/deleapi/school'


@app.route('/', methods=["GET", "POST"])



@app.route('/index', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html",
                               public_budgets=Budget.query.filter_by(public=True),
                               private_budgets=Budget.query.filter_by(public=False))


# Crea un presupuesto
@app.route('/presupuesto/crear', methods=["GET", "POST"])
def budget_create():
    if request.method == "GET":
        # Check if the web is up and running
        # TODO Levantar la deleapi
        res = requests.get(url_api)
        school = res.json()
        return render_template("budget_create.html", schools=school)

    else:
        name = request.form['name']
        school = request.form['school']
        public = True if request.form.get('public') else False
        # Si se ha especificado el nombre y la escuela se crea el presupuesto
        if name and school:
            budget = Budget(name,
                            school,
                            False,  # Por ahora la visibilidad esta desactivada
                            public,
                            [])
            db.session.add(budget)
            db.session.commit()
        # return name
        return render_template("index.html",
                               public_budgets=Budget.query.filter_by(public=True),
                               private_budgets=Budget.query.filter_by(public=False))


# Edita el presupuesto elegido
@app.route('/presupuesto/editar/<int:id>', methods=["GET", "POST"])
def budget_id(id):
    # Obtiene el presupuesto de la base de datos
    budget = Budget.query.get(id)
    if request.method == "GET":
        res = requests.get(url_api)
        school = res.json()
        public_str = 'true' if budget.public is True else 'false'
        return render_template("budget_edit.html",
                               schools=school,
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
        # return 'Updated ' + name + "!"


# Lista todos los presupuestos
@app.route('/presupuestos', methods=["GET", "POST"])
def budget_list():
    if request.method == "GET":
        res = requests.get(url_api)
        school = res.json()
        budgets = Budget.query.all()
        return render_template("budget_list.html",
                               budgets=budgets,
                               schools=school)


@app.route('/gasto/crear', methods=["GET", "POST"])
def expense_create():
    if request.method == "GET":
        res = requests.get(url_api)
        school = res.json()
        budgets = Budget.query.all()
        return render_template("expense_create.html",
                               budgets=budgets,
                               schools=school)

    else:
        amount = request.form['amount']
        name = request.form['name']
        budget_selected = request.form['budget']
        budget = Budget.query.filter_by(name=budget_selected)
        school = budget.school
        for budget in budgets:
            if budget == budget_selected:
                school = budget.school

        expense = Expense(name,
                          school,
                          datetime.datetime.utcnow(),
                          datetime.datetime.utcnow(),
                          datetime.datetime.utcnow(),
                          amount,
                          False,
                          [],
                          'hello')
        db.session.add(expense)
        db.session.commit()
        return 'name'


@app.route('/gastos', methods=["GET", "POST"])
def get_expenses():
    if request.method == "GET":
        res = requests.get(url_api)
        school = res.json()
        expenses = Expense.query.all()
        return render_template("expense_list.html",
                               expenses=expenses,
                               schools=school)


@app.route('/estadisticas', methods=['GET'])
def get_statistics():
    if request.method == 'GET':
        presupuestos = Budget.query.all()
        return render_template('statistics.html', budgets=presupuestos)


if __name__ == '__main__':
    app.run()
