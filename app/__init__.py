from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')  # Ensure you have this line to load configurations

db = SQLAlchemy(app)



from app import routes, models  # Import models after initializing db
