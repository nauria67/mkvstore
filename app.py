from flask import Flask

from core.mkv_controller import mkv_blueprint

app = Flask(__name__)
app.register_blueprint(mkv_blueprint, url_prefix="/mkv")

if __name__ == "__main__":
    app.run(debug=True)
