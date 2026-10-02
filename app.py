from database import conectar_banco, criar_tabelas
from flask import Flask, jsonify, request

app = Flask(__name__)

# Garante que as tabelas do banco estejam criadas ao iniciar
criar_tabelas()


@app.route("/")
def inicio():
  return jsonify({"mensagem": "Sistema de Gerenciamento Escolar"})


@app.route("/alunos", methods=["GET", "POST"])
def gerenciar_alunos():
  conexao = conectar_banco()

  # Caso seja um envio de dados (POST)
  if request.method == "POST":
    dados = request.get_json(silent=True) or request.form
    nome = dados.get("nome")
    email = dados.get("email")
    idade = dados.get("idade")

    try:
      cursor = conexao.cursor()
      cursor.execute(
          """
                INSERT INTO alunos (nome, email, idade)
                VALUES (?, ?, ?)
            """,
          (nome, email, idade),
      )
      conexao.commit()
      id_aluno = cursor.lastrowid
      conexao.close()

      return (
          jsonify({
              "sucesso": True,
              "mensagem": "Aluno cadastrado com sucesso!",
              "id": id_aluno,
          }),
          201,
      )

    except Exception as e:
      conexao.close()
      return (
          jsonify({
              "sucesso": False,
              "mensagem": "Erro ao cadastrar aluno",
              "detalhe": str(e),
          }),
          400,
      )

  # Requisição GET: Retorna diretamente os alunos cadastrados
  cursor = conexao.execute("SELECT * FROM alunos ORDER BY id DESC")
  registros = cursor.fetchall()
  conexao.close()

  # Converte os registros do SQLite (sqlite3.Row) para dicionários Python
  alunos = [dict(aluno) for aluno in registros]

  return jsonify(alunos)


if __name__ == "__main__":
  app.run(debug=True)