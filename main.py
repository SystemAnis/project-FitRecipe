import os
import time
from flask import Flask
from sqlalchemy.exc import OperationalError
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

# Al primo avvio popola i dati di base.
# Se PostgreSQL non è ancora pronto, riprova invece di far crashare l'app.
with app.app_context():
    for tentativo in range(10):
        try:
            inizializza_dati_base()
            break
        except OperationalError:
            db.session.rollback()
            if tentativo == 9:
                raise  # dopo 10 tentativi l'errore è reale: fermati
            print("Database non ancora pronto, riprovo tra 2 secondi...")
            time.sleep(2)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)