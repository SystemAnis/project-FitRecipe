import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. Configurazione del Database (legge l'URL dal docker-compose)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://admin:password123@db:5432/fit_recipes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inizializza l'ORM
db = SQLAlchemy(app)

# 2. Definizione del Modello (Rappresenta la tabella 'ingredients' in PostgreSQL)
class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    protein = db.Column(db.Float, nullable=False)    # Macro per 100g
    carbs = db.Column(db.Float, nullable=False)      # Macro per 100g
    fats = db.Column(db.Float, nullable=False)       # Macro per 100g
    calories = db.Column(db.Integer, nullable=False) # Calorie per 100g

    # Metodo di utilità per convertire l'oggetto in JSON
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "macros_per_100g": {
                "protein": self.protein,
                "carbs": self.carbs,
                "fats": self.fats,
                "calories": self.calories
            }
        }

# 3. Inizializzazione Automatica del Database
with app.app_context():
    db.create_all() # Crea le tabelle se non esistono
    
    # Se la tabella è vuota, inserisce i dati di base
    if Ingredient.query.count() == 0:
        alimenti_base = [
            Ingredient(name="Avena Istantanea Myprotein", protein=11.0, carbs=61.0, fats=7.7, calories=388),
            Ingredient(name="Impact Whey Protein", protein=82.0, carbs=4.0, fats=7.5, calories=412),
            Ingredient(name="Burro di Arachidi", protein=30.0, carbs=12.0, fats=46.0, calories=579),
            Ingredient(name="Yogurt Greco 0%", protein=10.3, carbs=4.0, fats=0.0, calories=57),
            Ingredient(name="Cacao Amaro in Polvere", protein=20.0, carbs=11.0, fats=21.0, calories=320),
            Ingredient(name="Farina di Cocco", protein=18.0, carbs=18.0, fats=16.0, calories=320)
        ]
        db.session.bulk_save_objects(alimenti_base)
        db.session.commit()
        print("Database PostgreSQL popolato con gli ingredienti base!")

# 4. Endpoint REST per interrogare il DB
@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all() # Tradotto dall'ORM in: SELECT * FROM ingredients;
    return jsonify([i.to_dict() for i in ingredients])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)