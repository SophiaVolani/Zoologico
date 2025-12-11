from flask import Flask
from pony.orm import Database
from flask_cors import CORS

# Instância do banco (Pony ORM)
db = Database()

# Instância principal do Flask
app = Flask(__name__)

# Libera requisições do React (localhost:3000 → localhost:5000)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuração do banco SQLite (arquivo salvo na pasta raiz)
import os
this_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(this_path, 'zoologico.db')

db.bind(
    provider='sqlite',
    filename=file_path,
    create_db=True
)

