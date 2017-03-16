from flask import Flask
from flask import render_template
from flask import request
import requests
from src.models.connection import db
# Inicializacion del objeto Flask
from src.models import Budget

app = Flask(__name__)

# Generacion del dict (diccionario) de configuracion desde fichero
app.config.from_pyfile('config.cfg')

# Enlaza la aplicacion y la base de datos
db.app = app
db.init_app(app)

# Url /
@app.route('/presupuesto/crear', methods=["GET", "POST"])
def budget_create():
    if request.method == "GET":
        url = 'https://delegacion.uc3m.es/deleapi/school'
        res = requests.get(url)
        school = res.json()
        print(school)
        return render_template("create.html", schools=school)

    elif request.method == "POST":
        name = request.form.get('name')
        school = request.form.get('school')
        public = True if request.form.get('public') == 'on' else False
        if name and school:
            budget = Budget(name, school, False, public, [])
            db.session.add(budget)
            db.session.commit()
        return name

@app.route('/presupuesto/editar/<id:int>', methods=["GET", "POST"])
def budget_id(id):
    budget = Budget.query.filter_by(id=id).first()
    if request.method == "GET":
        url = 'https://delegacion.uc3m.es/deleapi/school'
        res = requests.get(url)
        school = res.json()
        print(school)
        return render_template("create.html", schools=school, budget = budget)
@app.route('/')
def index():
    return 'Hola mundo'

if __name__ == '__main__':
    app.run()
