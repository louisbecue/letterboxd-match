from flask import Flask
from .routes.compare import compare_bp
from .routes.recommendations import recommendations_bp
import sys
import os

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config

app.config.from_object(Config)

app.register_blueprint(compare_bp)
app.register_blueprint(recommendations_bp)

@app.route('/')
def index():
    return "Welcome to the Letterboxd Comparison App!"

if __name__ == '__main__':
    app.run(debug=True)