from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/cadastro_func'
db = SQLAlchemy(app)

class Setor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)

class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    primeiro_nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    status_funcionario = db.Column(db.Boolean, nullable=False)
    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargo.id'), nullable=False)


def verifica_e_cria_tabelas():
    with app.app_context():
        inspector = inspect(db.engine)
        tabelas_existentes = inspector.get_table_names()
        tabelas_necessarias = ['setor', 'cargo', 'funcionario']
        
        for tabela in tabelas_necessarias:
            if tabela not in tabelas_existentes:
                print(f"A tabela '{tabela}' não existe. Criando...")
                db.create_all()
                print(f"Tabela '{tabela}' criada com sucesso.")
            else:
                print(f"A tabela '{tabela}' já existe.")



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastrar_setor', methods=['GET', 'POST'])
def cadastrar_setor():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_setor = Setor(nome=nome)
        try:
            db.session.add(novo_setor)
            db.session.commit()
            return redirect(url_for('sucesso', mensagem="Setor cadastrado com sucesso"))
        except Exception as e:
            return 'Ocorreu um erro ao cadastrar o setor: ' + str(e)

    return render_template('setor.html')


@app.route('/cadastrar_cargo', methods=['GET', 'POST'])
def cadastrar_cargo():
    if request.method == 'POST':
        nome = request.form['nome']
        id_setor = request.form['id_setor']
        novo_cargo = Cargo(nome=nome,id_setor=id_setor)

        try:
            db.session.add(novo_cargo)
            db.session.commit()
            return redirect(url_for('sucesso', mensagem="Cargo cadastrado com sucesso"))
        except Exception as e:
            return 'Ocorreu um erro ao cadastrar o setor: ' + str(e)
    
    setores = Setor.query.all()
    return render_template('cargo.html', setores=setores)



@app.route('/cadastrar_funcionario', methods=['GET', 'POST'])
def cadastrar_funcionario():
    if request.method == 'POST':
        primeiro_nome = request.form['primeiro_nome']
        sobrenome = request.form['sobrenome']
        data_admissao = request.form['data_admissao']
        status_funcionario = request.form['status_funcionario']
        if status_funcionario == '1':
            status_funcionario = True
        else:
            status_funcionario = False
        id_setor = request.form['id_setor']
        id_cargo = request.form['id_cargo']
        
        novo_funcionario = Funcionario(
            primeiro_nome=primeiro_nome,
            sobrenome=sobrenome,
            data_admissao=data_admissao,
            status_funcionario=status_funcionario,
            id_setor=id_setor,
            id_cargo=id_cargo)

        try:
            db.session.add(novo_funcionario)
            db.session.commit()
            return redirect(url_for('sucesso', mensagem="Funcionário cadastrado com sucesso")) 
        except Exception as e:
            return 'Ocorreu um erro ao cadastrar o setor: ' + str(e)
    
    setores = Setor.query.all()
    cargos = Cargo.query.all()
    return render_template('funcionario.html', setores=setores, cargos=cargos)

@app.route('/sucesso')
def sucesso():
    mensagem = request.args.get('mensagem')
    return render_template('sucesso.html', mensagem=mensagem)

if __name__ == '__main__':
    verifica_e_cria_tabelas()
    app.run(debug=True)
    
