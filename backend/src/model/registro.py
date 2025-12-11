from pony.orm import Required, Optional
from src.config import db

class Registro(db.Entity):
    descricao = Required(str)
    data = Required(str)

    animal = Required("Animal")
    produto = Optional("Produto")
    zoologico = Required("Zoologico")
