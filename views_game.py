import os
import time
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from livraria import app, db  
from models import Livros  
from helpers import recupera_imagem, deleta_arquivo, FormularioLivro 

@app.route('/')
def index():
    lista = Livros.query.order_by(Livros.id) 
    return render_template('lista.html', titulo='Livros', livros=lista) 

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioLivro()  
    return render_template('novo.html', titulo='Novo Livro', form=form)  

@app.route('/criar', methods=['POST', ])
def criar():
    form = FormularioLivro(request.form)  

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    titulo = form.titulo.data  
    genero = form.genero.data  
    autor = form.autor.data 
    editora = form.editora.data 

    livro = Livros.query.filter_by(titulo=titulo).first()  

    if livro:
        flash('Livro já existente!')  
        return redirect(url_for('index'))

    novo_livro = Livros(titulo=titulo, genero=genero, autor=autor, editora=editora)  
    db.session.add(novo_livro)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_livro.id}-{timestamp}.jpg')  

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    livro = Livros.query.filter_by(id=id).first()  
    form = FormularioLivro() 
    form.titulo.data = livro.titulo  
    form.genero.data = livro.genero  
    form.autor.data = livro.autor  
    form.editora.data = livro.editora 
    capa_livro = recupera_imagem(id) 
    return render_template('editar.html', titulo='Editando Livro', id=id, capa_livro=capa_livro, form=form) 

@app.route('/atualizar', methods=['POST', ])
def atualizar():
    form = FormularioLivro(request.form)  

    if form.validate_on_submit():
        livro = Livros.query.filter_by(id=request.form['id']).first()  
        livro.titulo = form.titulo.data  
        livro.genero = form.genero.data  
        livro.autor = form.autor.data  
        livro.editora = form.editora.data 

        db.session.add(livro) 
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(livro.id)
        arquivo.save(f'{upload_path}/capa{livro.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    Livros.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Livro deletado com sucesso!')  

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
