import datetime

import jinja2
from flask import Flask
from flask import render_template
from flask import request
import requests

from src.models import Expense
from src.models.connection import db
# Inicializacion del objeto Flask
from src.models import Budget

app = Flask(__name__)

# Generacion del dict (diccionario) de configuracion desde fichero
app.config.from_pyfile('config.cfg')

# Enlaza la aplicacion y la base de datos
db.app = app
db.init_app(app)
db.create_all()

# Url /
@app.route('/presupuesto/crear', methods=["GET", "POST"])
def budget_create():
    if request.method == "GET":
        url = 'https://delegacion.uc3m.es/deleapi/school'
        res = requests.get(url)
        school = res.json()
        print(school)
        return render_template("budget_create.html", schools=school)

    elif request.method == "POST":
        name = request.form.get('name')
        school = request.form.get('school')
        public = True if request.form.get('public') == 'on' else False
        if name and school:
            budget = Budget(name, school, False, public, [])
            db.session.add(budget)
            db.session.commit()
        return name

@app.route('/presupuesto/editar/<int:id>', methods=["GET", "POST"])
def budget_id(id):
    budget = Budget.query.filter_by(id=id).first()
    if request.method == "GET":
        url = 'https://delegacion.uc3m.es/deleapi/school'
        res = requests.get(url)
        school = res.json()
        if budget.public is True:
            public_str = 'true'
        else:
            public_str = 'false'
        return render_template("budget_edit.html", schools=school, budget = budget, public = public_str, id = id)
    elif request.method == "POST":
        name = request.form.get('name')
        school = request.form.get('school')
        public = True if request.form.get('public') == 'on' else False
        if name and school:
            budget = Budget.query.filter_by(id=id).first()
            budget.name = name
            budget.school = school
            budget.public = public
            db.session.commit()
        return 'Updated ' + name + "!"
@app.route('/presupuestos', methods=["GET", "POST"])
def get_budgets():
    if request.method == "GET":
        url = 'https://delegacion.uc3m.es/deleapi/school'
        res = requests.get(url)
        school = res.json()
        budgets = Budget.query.all()
        return render_template("budget_list.html", budgets=budgets, schools=school)
@app.route('/gasto/crear', methods=["GET", "POST"])
def expense_create():
    if request.method == "GET":
        url = 'https://delegacion.uc3m.es/deleapi/school'
        res = requests.get(url)
        school = res.json()
        budgets = Budget.query.all()
        return render_template("expense_create.html", budgets=budgets, schools=school)
    elif request.method == "POST":
        amount = request.form.get('amount')
        name = request.form.get('name')
        budgetGot = request.form.get('budget')
        print(budgetGot)
        budgets = Budget.query.all()
        school = 0
        for budget in budgets:
            if budget == budgetGot:
                school = budget.school
        expense = Expense(name, school, datetime.datetime.utcnow(), datetime.datetime.utcnow(), datetime.datetime.utcnow(), amount, False, [], 'hello')
        db.session.add(expense)
        db.session.commit()

        return 'name'
@app.route('/gastos', methods=["GET", "POST"])
def get_expenses():
    if request.method == "GET":
        url = 'https://delegacion.uc3m.es/deleapi/school'
        res = requests.get(url)
        school = res.json()
        expenses = Expense.query.all()
        return render_template("expense_list.html", expenses=expenses, schools=school)
@app.route('/')
def index():
    return 'Hola mundo'

if __name__ == '__main__':
    app.run()
