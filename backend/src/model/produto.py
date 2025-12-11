from pony.orm import Required, Set
from src.config import db

class Produto(db.Entity):
    nome = Required(str)
    tipo = Required(str)
    quantidade = Required(int)

    fornecedores = Set("FornecedorAlimentos")
    registros = Set("Registro")
