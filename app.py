from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text

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
    pai_mae = db.Column(db.String(3), nullable=False, default='nao')
    id_pai = db.Column(db.Integer, nullable=True)
    id_mae = db.Column(db.Integer, nullable=True)

# Atualizar a tabela para adicionar as novas colunas, se necessário
with app.app_context():
    inspector = inspect(db.engine)
    columns = [column['name'] for column in inspector.get_columns('animal')]

    with db.engine.connect() as conn:
        if 'pai_mae' not in columns:
            conn.execute(text('ALTER TABLE animal ADD COLUMN pai_mae TEXT DEFAULT "nao";'))
        if 'id_pai' not in columns:
            conn.execute(text('ALTER TABLE animal ADD COLUMN id_pai INTEGER;'))
        if 'id_mae' not in columns:
            conn.execute(text('ALTER TABLE animal ADD COLUMN id_mae INTEGER;'))

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
        pai_mae = request.form.get('pai_mae', 'nao')
        id_pai = request.form.get('id_pai')
        id_mae = request.form.get('id_mae')

        if pai_mae == 'sim':
            # Verifique se os IDs de pai e mãe são válidos com base no campo "identificacao" e sexo
            if id_pai and id_mae:
                pai_existe = Animal.query.filter_by(identificacao=id_pai, sexo='Macho').first()
                mae_existe = Animal.query.filter_by(identificacao=id_mae, sexo='Fêmea').first()
                if not pai_existe or not mae_existe:
                    return render_template('add_animal.html', message='ID do pai ou da mãe não está registrado ou não corresponde ao sexo correto.', message_type='error')
            else:
                return render_template('add_animal.html', message='IDs de pai e mãe são obrigatórios quando "Sim" é selecionado.', message_type='error')

        else:
            id_pai = None
            id_mae = None

        novo_animal = Animal(
            identificacao=identificacao, 
            raca=raca, 
            sexo=sexo, 
            peso=peso,
            data_de_nascimento=data_de_nascimento, 
            data_de_cobertura=data_de_cobertura,
            pai_mae=pai_mae,
            id_pai=id_pai,
            id_mae=id_mae
        )
        try:
            db.session.add(novo_animal)
            db.session.commit()
            return render_template('add_animal.html', message="Animal adicionado com sucesso!", message_type="success")
        except Exception as e:
            return render_template('add_animal.html', message='Esse número de animal já está registrado.', message_type="error")

    # Fetch existing animals for parent selection
    animais = Animal.query.all()
    return render_template('add_animal.html', animais=animais)


@app.route('/list')
def animal_list():
    animais = Animal.query.all()
    return render_template('animal_list.html', animais=animais)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
