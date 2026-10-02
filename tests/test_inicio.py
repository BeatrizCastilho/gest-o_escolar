from app import app

cliente = app.test_client()


def test_inicio():

    resposta = cliente.get('/')

    assert resposta.status_code == 200


def test_inicio_message():

    resposta = cliente.get('/')

    assert resposta.data.decode() == "Sistema de Gerenciamento Escolar"


@app.route('/test')
def test():
    return "Rota de teste"


if __name__ == '__main__':
    app.run(debug=True)