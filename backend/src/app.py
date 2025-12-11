# ajuste para importar pastas corretamente
import os,sys
currDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.abspath(os.path.join(currDir, '..'))
if rootDir not in sys.path: # add parent dir to paths
    sys.path.append(rootDir)

from flask import jsonify, request
from pony.orm import db_session, commit
from src.config import db, app

from src.model.produto import Produto
from src.model.fornecedor_alimentos import FornecedorAlimentos
from src.model.animal import Animal
from src.model.registro import Registro
from src.model.zoologico import Zoologico


# -------------------------
# BANCO E MAPEAMENTO
# -------------------------

db.generate_mapping(create_tables=True)


# -------------------------
# ROTA INICIAL
# -------------------------

@app.route('/')
def home():
    return "<h1>API do Zoológico funcionando 🐾</h1>"


# =========================================================
# 🔥 ROTAS CRUD — ANIMAIS
# =========================================================

@app.route('/animais', methods=['GET'])
@db_session
def listar_animais():
    animais = [a.to_dict(with_lazy=True, with_collections=True) for a in Animal.select()]
    return jsonify({"status": "sucesso", "dados": animais}), 200


@app.route('/animais', methods=['POST'])
@db_session
def criar_animal():
    data = request.json
    animal = Animal(
        nome=data["nome"],
        especie=data["especie"],
        habitat=data["habitat"],
        localidade=data["localidade"],
        alimentacao=data["alimentacao"]
    )
    commit()
    return jsonify(animal.to_dict()), 201


@app.route('/animais/<int:id>', methods=['PUT'])
@db_session
def atualizar_animal(id):
    data = request.json
    animal = Animal.get(id=id)

    if not animal:
        return jsonify({"erro": "Animal não encontrado"}), 404

    animal.set(
        nome=data["nome"],
        especie=data["especie"],
        habitat=data["habitat"],
        localidade=data["localidade"],
        alimentacao=data["alimentacao"]
    )
    commit()
    return jsonify(animal.to_dict()), 200


@app.route('/animais/<int:id>', methods=['DELETE'])
@db_session
def excluir_animal(id):
    animal = Animal.get(id=id)
    if not animal:
        return jsonify({"erro": "Animal não encontrado"}), 404

    animal.delete()
    commit()
    return jsonify({"mensagem": "Animal excluído"}), 200



# =========================================================
# 🔥 ROTAS CRUD — PRODUTOS
# =========================================================

@app.route('/produtos', methods=['GET'])
@db_session
def listar_produtos():
    produtos = [p.to_dict() for p in Produto.select()]
    return jsonify({"dados": produtos}), 200


@app.route('/produtos', methods=['POST'])
@db_session
def criar_produto():
    data = request.json
    produto = Produto(
        nome=data["nome"],
        tipo=data["tipo"],
        quantidade=data["quantidade"]
    )
    commit()
    return jsonify(produto.to_dict()), 201


@app.route('/produtos/<int:id>', methods=['PUT'])
@db_session
def atualizar_produto(id):
    data = request.json
    produto = Produto.get(id=id)

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    produto.set(
        nome=data["nome"],
        tipo=data["tipo"],
        quantidade=data["quantidade"]
    )
    commit()
    return jsonify(produto.to_dict()), 200


@app.route('/produtos/<int:id>', methods=['DELETE'])
@db_session
def excluir_produto(id):
    produto = Produto.get(id=id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    produto.delete()
    commit()
    return jsonify({"mensagem": "Produto excluído"}), 200



# =========================================================
# 🔥 ROTAS CRUD — FORNECEDORES
# =========================================================

@app.route('/fornecedores', methods=['GET'])
@db_session
def listar_fornecedores():
    fornecedores = [
        f.to_dict(with_lazy=True, with_collections=True)
        for f in FornecedorAlimentos.select()
    ]
    return jsonify({"dados": fornecedores}), 200


@app.route('/fornecedores', methods=['POST'])
@db_session
def criar_fornecedor():
    data = request.json
    produto = Produto.get(id=data["produto"])

    fornecedor = FornecedorAlimentos(
        nome=data["nome"],
        cnpj=data["cnpj"],
        produto=produto
    )
    commit()
    return jsonify(fornecedor.to_dict()), 201


@app.route('/fornecedores/<int:id>', methods=['GET'])
@db_session
def obter_fornecedor(id):
    forn = FornecedorAlimentos.get(id=id)
    if not forn:
        return jsonify({"erro": "Fornecedor não encontrado"}), 404
    return jsonify(forn.to_dict(with_lazy=True)), 200


@app.route('/fornecedores/<int:id>', methods=['PUT'])
@db_session
def atualizar_fornecedor(id):
    data = request.json
    forn = FornecedorAlimentos.get(id=id)

    if not forn:
        return jsonify({"erro": "Fornecedor não encontrado"}), 404

    produto = Produto.get(id=data["produto"])

    forn.set(
        nome=data["nome"],
        cnpj=data["cnpj"],
        produto=produto
    )
    commit()
    return jsonify(forn.to_dict()), 200


@app.route('/fornecedores/<int:id>', methods=['DELETE'])
@db_session
def excluir_fornecedor(id):
    forn = FornecedorAlimentos.get(id=id)
    if not forn:
        return jsonify({"erro": "Fornecedor não encontrado"}), 404

    forn.delete()
    commit()
    return jsonify({"mensagem": "Fornecedor excluído"}), 200



# =========================================================
# 🔥 ROTAS CRUD — ZOOLÓGICOS (BLOCO COMPLETO E CORRIGIDO)
# =========================================================

@app.route('/zoologicos', methods=['GET'])
@db_session
def listar_zoologicos():
    zoo = [z.to_dict() for z in Zoologico.select()]
    return jsonify({"dados": zoo}), 200


@app.route('/zoologicos', methods=['POST'])
@db_session
def criar_zoologico():
    data = request.json
    print("=== RECEBIDO DO FRONT ===")
    print(data)

    try:
        capacidade_num = int(data.get("capacidade", 0) or 0)
        print("Capacidade convertida:", capacidade_num)

        z = Zoologico(
            nome=data.get("nome", "").strip(),
            cidade=data.get("cidade", "").strip(),
            estado=data.get("estado", "").strip(),
            capacidade=capacidade_num
        )

        commit()
        print("=== ZOO CRIADO COM SUCESSO ===")
        print(z.to_dict())
        return jsonify(z.to_dict()), 201

    except Exception as e:
        print("=== ERRO DETALHADO ===")
        import traceback
        traceback.print_exc()  # <-- imprime erro completo no terminal!
        return jsonify({"erro": "Erro ao criar zoológico", "detalhes": str(e)}), 500


@app.route('/zoologicos/<int:id>', methods=['PUT'])
@db_session
def atualizar_zoologico(id):
    data = request.json
    z = Zoologico.get(id=id)

    if not z:
        return jsonify({"erro": "Zoológico não encontrado"}), 404

    try:
        capacidade_num = int(data.get("capacidade", 0) or 0)

        z.set(
            nome=data.get("nome", "").strip(),
            cidade=data.get("cidade", "").strip(),
            estado=data.get("estado", "").strip(),
            capacidade=capacidade_num
        )

        commit()
        return jsonify(z.to_dict()), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao atualizar zoológico",
            "detalhes": str(e)
        }), 500


@app.route('/zoologicos/<int:id>', methods=['DELETE'])
@db_session
def excluir_zoologico(id):
    z = Zoologico.get(id=id)

    if not z:
        return jsonify({"erro": "Zoológico não encontrado"}), 404

    z.delete()
    commit()
    return jsonify({"mensagem": "Zoológico excluído com sucesso"}), 200


# =========================================================
# 🔥 ROTAS CRUD — REGISTROS
# =========================================================

@app.route('/registros', methods=['GET'])
@db_session
def listar_registros():
    registros = [
        r.to_dict(with_lazy=True, with_collections=True)
        for r in Registro.select()
    ]
    return jsonify({"dados": registros}), 200


@app.route('/registros', methods=['POST'])
@db_session
def criar_registro():
    data = request.json

    animal = Animal.get(id=data["animal"])
    zoologico = Zoologico.get(id=data["zoologico"])

    registro = Registro(
        descricao=data["descricao"],
        data=data["data"],
        animal=animal,
        zoologico=zoologico
    )
    commit()
    return jsonify(registro.to_dict()), 201


@app.route('/registros/<int:id>', methods=['DELETE'])
@db_session
def excluir_registro(id):
    r = Registro.get(id=id)
    if not r:
        return jsonify({"erro": "Registro não encontrado"}), 404

    r.delete()
    commit()
    return jsonify({"mensagem": "Registro excluído"}), 200



# -------------------------
# EXECUTAR APP
# -------------------------

if __name__ == '__main__':
    app.run(debug=True)
