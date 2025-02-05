from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

db = SQLAlchemy(app)

# Adicione isso após a criação do objeto `db`
migrate = Migrate(app, db)


# Modelo do Personagem
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(20), nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)  # Novo campo

# Cria o banco de dados
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    characters = Character.query.all()
    return render_template('index.html', characters=characters)

@app.route('/add', methods=['GET', 'POST'])
def add_character():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        strength = request.form['strength']
        hp = request.form['hp']
        size = request.form['size']
        speed = request.form['speed']
        photo = request.files['photo']
        description = request.form['description']



        # Salva a foto na pasta uploads
        if photo:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(photo_path)
            photo_name = photo.filename
        else:
            photo_name = None

        # Cria um novo personagem
        new_character = Character(
		    name=name,
		    type=type,
		    strength=strength,
		    hp=hp,
		    size=size,
		    speed=speed,
		    photo=photo_name,
		    description=description  # Adiciona a descrição
		)

        db.session.add(new_character)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_character.html')

@app.route('/character/<int:id>')
def character(id):
    character = Character.query.get_or_404(id)
    return render_template('character.html', character=character)

if __name__ == '__main__':
    app.run(debug=True)