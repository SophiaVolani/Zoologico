from pony.orm import Required, Set
from src.config import db

class Animal(db.Entity):
    nome = Required(str)
    especie = Required(str)
    habitat = Required(str)
    localidade = Required(str)
    alimentacao = Required(str)

    registros = Set("Registro")
