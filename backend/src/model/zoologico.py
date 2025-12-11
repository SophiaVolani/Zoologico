from pony.orm import Required, Set
from src.config import db

class Zoologico(db.Entity):
    nome = Required(str)
    cidade = Required(str)
    estado = Required(str)
    capacidade = Required(int)

    registros = Set("Registro")