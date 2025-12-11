from pony.orm import db_session, select
from src.config import db

# Importa os modelos
from animal import Animal
from fornecedor_alimentos import FornecedorAlimentos
from produto import Produto
from registro import Registro
from zoologico import Zoologico

# 🔹 Configura o banco (SQLite em memória só para testes)
db.bind(provider="sqlite", filename=":memory:", create_db=True)
db.generate_mapping(create_tables=True)

@db_session
def popular_dados():
    # Criar Zoológico
    zoo = Zoologico(nome="Zoo de São Paulo", cep="04301-000")

    # Criar Animais
    tigre = Animal(especie="Tigre", habitat="Selva", localidade="Índia", alimentacao="Carnívoro")
    arara = Animal(especie="Arara", habitat="Floresta", localidade="Amazônia", alimentacao="Frutas")

    # Criar Produtos
    racao = Produto(data_validade="2025-12-31", nome="Ração Premium", tipo="Ração")
    frutas = Produto(data_validade="2025-10-20", nome="Frutas Tropicais", tipo="Natural")

    # Criar Fornecedores vinculados a produtos
    forn1 = FornecedorAlimentos(nome="PetFood LTDA", cnpj="12.345.678/0001-99", produto=racao)
    forn2 = FornecedorAlimentos(nome="Frutaria Brasil", cnpj="98.765.432/0001-11", produto=frutas)

    # Criar Registros de entrada no zoológico
    Registro(data_entrada="2025-10-01", animal=tigre, zoologico=zoo)
    Registro(data_entrada="2025-10-01", animal=arara, zoologico=zoo)

    print("✅ Dados populados com sucesso!")

@db_session
def listar_dados():
    print("\n📌 Zoológicos:")
    for z in Zoologico.select():
        print(f"- {z.nome} ({z.cep})")

    print("\n📌 Animais:")
    for a in Animal.select():
        print(f"- {a.especie}, habitat: {a.habitat}, local: {a.localidade}, alimentação: {a.alimentacao}")

    print("\n📌 Produtos e Fornecedores:")
    for p in Produto.select():
        fornecedores = [f.nome for f in p.fornecedor]
        print(f"- {p.nome} ({p.tipo}), validade {p.data_validade} | Fornecedores: {', '.join(fornecedores)}")

    print("\n📌 Registros:")
    for r in Registro.select():
        print(f"- {r.data_entrada}: {r.animal.especie} no {r.zoologico.nome}")


if __name__ == "__main__":
    popular_dados()
    listar_dados()
