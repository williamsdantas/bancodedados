from bson import ObjectId
from flask import Flask, jsonify, request
from config.config import bd, pedidos_collection

from routes.clientes import clientes_bp
from routes.produtos import produtos_bp
from routes.pedidos import pedidos_bp

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World."

# Registrar os blueprints
app.register_blueprint(clientes_bp)
app.register_blueprint(produtos_bp)
app.register_blueprint(pedidos_bp)

if __name__ == "__main__":
    app.run(debug=True)