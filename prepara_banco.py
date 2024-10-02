import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin123'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `livraria`;")  

cursor.execute("CREATE DATABASE `livraria`;")  

cursor.execute("USE `livraria`;")  

TABLES = {}
TABLES['Livros'] = ('''
      CREATE TABLE `livros` ( 
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `titulo` varchar(50) NOT NULL,  
      `genero` varchar(40) NOT NULL,  
      `autor` varchar(50) NOT NULL,  
      `editora` varchar(30) NOT NULL, 
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
    ("Eduardo Augusto", "Eduardo", generate_password_hash("admin1").decode('utf-8')),
    ("João Paulo", "Paulo", generate_password_hash("admin2").decode('utf-8')),
    ("Ana Carolina", "Ana", generate_password_hash("admin3").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('SELECT * FROM livraria.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

livros_sql = 'INSERT INTO livros (titulo, genero, autor, editora) VALUES (%s, %s, %s, %s)'
livros = [
    ('O Milagre da Manhã', 'Desenvolvimento Pessoal', 'Hal Elrod', 'BestSeller'),
    ('Pense e Enriqueça', 'Desenvolvimento Pessoal', 'Napoleon Hill', 'Fundamento'),
    ('O Poder do Hábito', 'Psicologia/Negócios', 'Charles Duhigg', 'Objetiva'),
    ('A Mágica da Arrumação', 'Autoajuda/Organização', 'Marie Kondo', 'Sextante'),
    ('Desperte Seu Gigante Interior', 'Desenvolvimento Pessoal', 'Anthony Robbins', 'BestSeller'),
    ('Os Segredos da Mente Milionária', 'Desenvolvimento Pessoal/Finanças', 'T. Harv Eker', 'Sextante'),
    ('Os 7 Hábitos das Pessoas Altamente Eficazes', 'Desenvolvimento Pessoal/Liderança', 'Stephen R. Covey', 'BestSeller'),
    ('A Única Coisa', 'Produtividade', 'Gary Keller e Jay Papasan', 'Novo Século'),
    ('O Poder do Agora', 'Espiritualidade/Autoajuda', 'Eckhart Tolle', 'Sextante'),
    ('O Homem Mais Rico da Babilônia', 'Finanças/Autoajuda', 'George S. Clason', 'HarperCollins Brasil'),
    ('A Guerra da Arte', 'Criatividade/Desenvolvimento Pessoal', 'Steven Pressfield', 'Casa da Palavra'),
    ('A Ciência para Ficar Rico', 'Desenvolvimento Pessoal', 'Wallace D. Wattles', 'Saraiva'),
    ('A Arte da Felicidade', 'Desenvolvimento Pessoal/Espiritualidade', 'Dalai Lama e Howard Cutler', 'Martins Fontes'),
    ('O Monge e o Executivo', 'Liderança/Desenvolvimento Pessoal', 'James C. Hunter', 'Sextante'),
    ('Inteligência Emocional', 'Psicologia', 'Daniel Goleman', 'Objetiva'),
    ('A Lei do Triunfo', 'Desenvolvimento Pessoal', 'Napoleon Hill', 'Fundamento'),
    ('A Mente Organizada', 'Psicologia/Produtividade', 'Daniel J. Levitin', 'Objetiva')
]


cursor.executemany(livros_sql, livros)

cursor.execute('SELECT * FROM livraria.livros') 
print(' -------------  Livros:  -------------')
for livro in cursor.fetchall():
    print(livro[1])

conn.commit()

cursor.close()
conn.close()
