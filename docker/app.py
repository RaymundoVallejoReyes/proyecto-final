from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Aplicación DevOps</title>
        </head>
        <body>
            <h1>Aplicación Flask desplegada con Docker</h1>
            <p>Soluciones Tecnológicas del Futuro</p>
            <p>La aplicación está corriendo correctamente en el puerto 5000.</p>
        </body>
    </html>
    """

@app.route("/health")
def health():
    return {"status": "ok", "message": "Aplicación funcionando correctamente"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
