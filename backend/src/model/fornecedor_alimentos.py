from pony.orm import Required
from src.config import db

class FornecedorAlimentos(db.Entity):
    nome = Required(str)
    cnpj = Required(str)

    produto = Required("Produto")
