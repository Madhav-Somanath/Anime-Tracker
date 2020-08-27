from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = "asdf"


from routes import *

if __name__ == '__main__':
    app.run(debug=True)
