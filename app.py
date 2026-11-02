import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy # importa la libreria SQLAlchemy per la gestione del database

# Inizializzo l'app Flask
app = Flask(__name__)

# Configurazione del database PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql+psycopg2://admin:password123@db:5432/fit_recipes'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inizializzo l'ORM (SQLAlchemy) con l'app Flask
db = SQLAlchemy(app)

# Classe che rappresenta la tabella "ingredienti" nel database in PostgreSQL
class Ingredient(db.Model):
    __tablename__ = 'ingredienti'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    protein = db.Column(db.Float, nullable=False) # Proteine per 100 grammi di prodotto
    carbs = db.Column(db.Float, nullable=False) # Carboidrati per 100 grammi di prodotto
    fats = db.Column(db.Float, nullable=False) # Grassi per 100 grammi di prodotto
    calories = db.Column(db.Float, nullable=False) # Calorie per 100 grammi di prodotto
    
    # Funzione che serve a convertire l'oggetto "Ingredient" in un dizionario per poterlo restituire come JSON
    def to_dict(self): 
        return {
            'id': self.id,
            'name': self.name,
            "Macronutrienti per 100 grammi": {
                'protein': self.protein,
                'carbs': self.carbs,
                'fats': self.fats,
                'calories': self.calories
            }
        }

# Inizializzazione della Struttura del Database 
with app.app_context():
    db.create_all()  # Crea le tabelle nel database se non esistono già
    
    # Se la lista è vuota, aggiunge i seguenti ingredienti:
    if Ingredient.calories.query.count() == 0: # lista vuota
        ingredients = [
            Ingredient(name="Avena Istantanea", protein=11.0, carbs=61.0, fats=7.7, calories=388),
            Ingredient(name="Proteine del Siero del Latte (Whey)", protein=82.0, carbs=4.0, fats=7.5, calories=412),
            Ingredient(name="Burro di Arachidi", protein=30.0, carbs=12.0, fats=46.0, calories=579),
            Ingredient(name="Yogurt Greco 0%", protein=10.3, carbs=4.0, fats=0.0, calories=57),
            Ingredient(name="Cacao Amaro in Polvere", protein=20.0, carbs=11.0, fats=21.0, calories=320),
            Ingredient(name="Farina di Cocco", protein=18.0, carbs=18.0, fats=16.0, calories=320)
        ]
        db.session.bulk_save_objects(ingredients)  # Aggiunge gli ingredienti al database
        db.session.commit()  # Salva le modifiche nel database
        print("Database initialized with ingredients!.")
        
# Endpoint REST per "ottenere" la lista degli ingredienti
@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all() # ottiene tutti gli ingredienti dal database
    return jsonify([ingredient.to_dict() for ingredient in ingredients]) # restituisce la lista degli ingredienti come JSON


# Avvio dell'app Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)