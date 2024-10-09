from flask import request

def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object("config.localDev")

    from flask_restful import Api
    api = Api(app)

    from flask_cors import CORS
    CORS(app)

    return app, api

app, api_handler = create_app()


@app.route("/hello_worldo")
def hello_world():
    return "Hello Worldo!"

from routes.testooo import test0  
api_handler.add_resource(test0, "/testo")

if __name__ == "__main__":
    app.run(port=8008, debug=True)