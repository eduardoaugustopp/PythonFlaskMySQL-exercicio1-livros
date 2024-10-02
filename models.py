from livraria import db

class Livros(db.Model):  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(50), nullable=False) 
    genero = db.Column(db.String(40), nullable=False)  
    autor = db.Column(db.String(20), nullable=False)  
    editora = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<Livro {self.titulo}>' 


class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Usuário {self.nickname}>' 
