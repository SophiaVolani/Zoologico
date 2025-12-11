from src.config import db

# 🔹 Importa todos os modelos antes de gerar o mapeamento
from src.model.animal import Animal
from src.model.fornecedor_alimentos import FornecedorAlimentos
from src.model.produto import Produto
from src.model.registro import Registro
from src.model.zoologico import Zoologico

# 🔹 Gera as tabelas no banco (agora que todas as entidades foram importadas)
db.generate_mapping(create_tables=True)

from pony.orm import db_session

@db_session
def popular_dados():
    zoo = Zoologico(nome="Zoo de São Paulo", cep="04301-000")
    racao = Produto(data_validade="2025-12-31", nome="Ração Premium", tipo="Ração")
    fornecedor = FornecedorAlimentos(nome="NutriPet Ltda", cnpj="12.345.678/0001-90", produto=racao)
    animal = Animal(especie="Leão", habitat="Savana", localidade="África", alimentacao="Carnívoro")
    registro = Registro(data_entrada="2025-10-13", animal=animal, zoologico=zoo)
    print("Banco populado com sucesso!")

if __name__ == "__main__":
    popular_dados()
