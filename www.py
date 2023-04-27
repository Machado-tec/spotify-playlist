from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    # Aqui você pode adicionar o código para processar o código de autorização recebido
    return "Received authorization code: " + code

if __name__ == '__main__':
    app.run(port=8000)
