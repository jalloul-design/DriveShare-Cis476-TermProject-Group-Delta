from flask import Flask
from auth.database import init_db
from auth.routes import auth_bp

app = Flask(__name__)
app.secret_key = ''
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
