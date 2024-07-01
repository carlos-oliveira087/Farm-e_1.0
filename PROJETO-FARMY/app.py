from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessário para usar flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Carlos/Desktop/PROJETO-FARMY/instance/fazenda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identificacao = db.Column(db.String(50), unique=True, nullable=False)
    raca = db.Column(db.String(100), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    data_de_nascimento = db.Column(db.String(10), nullable=False)
    data_de_cobertura = db.Column(db.String(10), nullable=False)

@app.route('/')
def home():
    return redirect(url_for('add_animal_page'))

@app.route('/add', methods=['GET', 'POST'])
def add_animal_page():
    if request.method == 'POST':
        identificacao = request.form['identificacao']
        raca = request.form['raca']
        sexo = request.form['sexo']
        peso = float(request.form['peso'])
        data_de_nascimento = request.form['data_de_nascimento']
        data_de_cobertura = request.form['data_de_cobertura']

        novo_animal = Animal(identificacao=identificacao, raca=raca, sexo=sexo, peso=peso,
                             data_de_nascimento=data_de_nascimento, data_de_cobertura=data_de_cobertura)
        try:
            db.session.add(novo_animal)
            db.session.commit()
            return render_template('add_animal.html', message="Animal adicionado com sucesso!", message_type="success")
        except Exception as e:
            return render_template('add_animal.html', message=f'Esse número de animal já está registrado.', message_type="error")

    return render_template('add_animal.html')


@app.route('/list')
def animal_list():
    animais = Animal.query.all()
    return render_template('animal_list.html', animais=animais)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

