from flask import Flask, render_template
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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)