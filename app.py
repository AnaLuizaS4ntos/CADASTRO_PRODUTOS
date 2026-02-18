from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

## modelo do produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    estoque = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    sku = request.form.get('sku')
    name = request.form.get('name')
    category = request.form.get('category')
    color = request.form.get('color')
    estoque = request.form.get('estoque')
    price = request.form.get('price')

    ## criando o bd
    novo_produto = Produto(
        sku = sku,
        name = name,
        category = category,
        color = color,
        estoque = int(estoque) if estoque else 0,
        price = float(price) if price else 0
    )

    db.session.add(novo_produto)
    db.session.commit()

    return redirect(url_for('cadastro_produtos'))

## pagina inicial dos produtos do cadastro
@app.route("/")
def cadastro_produtos():
    todos_produtos = Produto.query.order_by(Produto.id.asc()).all()
    return render_template("base.html", produtos=todos_produtos)

@app.route('/deletar/<int:id>')
def deletar(id):
    produto = Produto.query.get(id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
    return redirect(url_for('cadastro_produtos'))


@app.route("/editar/<int:id>", methods=['GET', 'POST'])
def editar(id):
    produto = Produto.query.get(id)
    if request.method == 'POST':
        # Atualiza os dados com o que foi digitado no formulário de edição
        produto.sku = request.form.get('sku')
        produto.name = request.form.get('name')
        produto.category = request.form.get('category')
        produto.color = request.form.get('color')
        produto.estoque = int(request.form.get('estoque'))
        produto.price = float(request.form.get('price'))

        db.session.commit()
        return redirect(url_for('cadastro_produtos'))

    # Se for GET, ele abre a página de edição passando o 'produto' atual
    return render_template("editar.html", produto=produto)

if __name__ == "__main__":
    app.run(debug=True)