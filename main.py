import os
from flask import Flask
from database import db

# Importo le rotte dei blueprint
from TabsRoute import api_schede
from IngredientsRoute import api_ingredienti

# Importo la funzione per popolare il database
from db_Population import inizializza_dati_base

# Inizializzo l'app Flask
app = Flask(__name__)

# Configurazione del database PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'postgresql+psycopg2://admin:password123@db:5432/fit_recipes'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Collego l'app Flask all'istanza di SQLAlchemy
db.init_app(app)

# Registro le rotte dei Blueprint
app.register_blueprint(api_schede)
app.register_blueprint(api_ingredienti)

# Al primo avvio popola i dati di base
with app.app_context():
    inizializza_dati_base()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)