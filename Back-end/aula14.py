from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

#CONEXÃO COM O BANCO DE DADOS
DB_CONFIG = {
    'host' : 'localhost',
    'user' : "root",
    'password' : 'senai',
    'database' : 'Papelaria'
}
def conecta_bd():
    conexaoDB = mysql.connector.connect(**DB_CONFIG)
    cursorDB = conexaoDB.cursor()
    return conexaoDB, cursorDB


#FUNCAO FECHAR CONEXAO DB
def close_db(conexaoDB, cursorDB):
    cursorDB.close()
    conexaoDB.close()


#Listar produtos
@app.route('/produto', methods=['GET'])
def listar_produtos():
    try:
        comandoSQL = "SELECT * FROM Produto"
        conexaoDB, cursorDB = conecta_bd()
        cursorDB.execute(comandoSQL)
        produtos = cursorDB.fetchall()
        if not produtos:
            return jsonify({'mensagem':'Não há produtos'}),200
        
        produtosjson = []
        for produto in produtos:
            produto_dic = {"idproduto":produto[0], "nome":produto[1], "descricao":produto[2], 
        "preco":produto[3], "quantidade":produto[4]}
            produtosjson.append(produto_dic)
        
        return jsonify(produtos), 200
    except Error as erro:
        return jsonify({'erro': f'{erro}'}),500
    finally:
        close_db(conexaoDB, cursorDB)
    

#Retorna um produto
@app.route('/produto/<int:id_produto>', methods=['GET'])
def get_produto(id_produto):
    try:
        comandoSQL = 'SELECT * FROM Produto WHERE idProduto = %s'
        conexaoDB, cursorDB = conecta_bd()
        cursorDB.execute(comandoSQL,(id_produto,))
        produto = cursorDB.fetchone()
        
        if not produto:
            return jsonify({'mensagem': 'Produto não encontrado'}),200
        
        produtojson = {"idproduto":produto[0], "nome":produto[1], "descricao":produto[2], 
        "preco":produto[3], "quantidade":produto[4]}
        
        return jsonify(produtojson),200
    except Error as erro:
        return jsonify({'erro': f'{erro}'}),500
    finally:
        close_db(conexaoDB, cursorDB)


#Exclui um produto
@app.route('/produto', methods=['DELETE'])
def delete_produto():
    try:
        dados = request.json
        id_produto = dados.get('idproduto')
        conexaoDB, cursorDB = conecta_bd()
        comandoSQL = 'DELETE FROM Produto WHERE idProduto = %s'
        cursorDB.execute(comandoSQL,(id_produto,))
        conexaoDB.commit()
        return jsonify({'mensagem':'Produto excluído'}),200
    except Error as erro:
        return jsonify({'erro': f'{erro}'}),500
    except KeyError:
        return jsonify({'erro':'Faltando informação'}),500
    finally:
        close_db(conexaoDB, cursorDB)
    
#Cadastro de produtos
@app.route('/produto', methods=['POST'])
def cadastro_produto():
    try:
        dados = request.json
        nome = dados.get('nome')
        descricao = dados.get('descricao')
        preco = dados.get('preco')
        quantidade = dados.get('quantidade')
        if not all([nome, descricao, preco, quantidade]):
            return jsonify({'Error':'Há campos vazios'}),400
        
        conexaoDB, cursorDB = conecta_bd()
        comandoSQL = 'INSERT INTO Produto (nome,descricao,preco,quantidade) VALUES (%s,%s,%s,%s)'
        cursorDB.execute(comandoSQL, (nome,descricao,preco,quantidade))
        conexaoDB.commit()
        return jsonify({'mensagem':'Cadastro realizado'}),201
    except Error as erro:
        return jsonify({'erro': f'{erro}'}),500
    except KeyError:
         return jsonify({'erro': 'Faltando campos!'}),500 
    finally:
        close_db(conexaoDB, cursorDB)  
    
#Atualizar um produto
@app.route('/produto', methods=['PUT'])
def update_produto():
    try:
        dados = request.json
        idproduto = dados.get('idproduto')
        nome = dados.get('nome')
        descricao = dados.get('descricao')
        preco = dados.get('preco')
        quantidade = dados.get('quantidade')

        if not all([idproduto,nome, descricao, preco, quantidade]):
            return jsonify({'Erro':'Dados incompletos'}),400
        comandoSQL = f'UPDATE Produto SET nome = %s, descricao = %s, preco = %s, quantidade = %s WHERE idproduto = %s'
        conexaoDB, cursorDB = conecta_bd()
        cursorDB.execute(comandoSQL, (nome,descricao,preco,quantidade,idproduto))
        conexaoDB.commit()
        return jsonify({'mensagem':'Alteração realizada'}),200
    except Error as erro:
        return jsonify({'erro': f'{erro}'}),500
    except KeyError:
         return jsonify({'erro': 'Faltando campos!'}),500
    finally:
        close_db(conexaoDB, cursorDB)

#ERRO 404
@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return jsonify({'erro':'Página não encontrada'}), 404   


#ERRO 405
@app.errorhandler(405)
def metodo_invalido(erro):
    return jsonify({'erro':'Método HTTP inválido'}), 405


#ERRO 500
@app.errorhandler(500)
def erro_servidor(erro):
    return jsonify({'erro':'Erro interno no servidor'}), 500   

# ROTA DA PÁGINA DE BUSCA
@app.route("/busca", methods=["POST"])
def busca():
    try:
        busca = request.form['buscar']
        conexaoDB, cursorDB = conecta_bd()
        comandoSQL = 'SELECT * FROM Produto WHERE nome LIKE %s'
        cursorDB.execute(comandoSQL, ("%" + busca + "%",))
        produtos = cursorDB.fetchall()

        produtosjson = []
        for produto in produtos:
            produto_dic = {"idproduto": produto[0], "nome": produto[1], "descricao": produto[2], 
                           "preco": produto[3], "quantidade": produto[4]}
            produtosjson.append(produto_dic)

        return jsonify(produtosjson), 200
    except Error as erro:
        return jsonify({'erro': f'{erro}'}), 500
    finally:
        close_db(conexaoDB, cursorDB)







#ultimas linhas
if __name__ == '__main__':
  app.run(debug=True)