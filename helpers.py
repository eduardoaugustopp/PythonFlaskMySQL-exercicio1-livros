import os
from livraria import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

class FormularioLivro(FlaskForm):  
    titulo = StringField('Título do Livro', [validators.DataRequired(), validators.Length(min=1, max=50)])  
    genero = StringField('Gênero', [validators.DataRequired(), validators.Length(min=1, max=40)])
    autor = StringField('Autor', [validators.DataRequired(), validators.Length(min=1, max=20)])  
    editora = StringField('Editora', [validators.DataRequired(), validators.Length(min=1, max=30)])  
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
