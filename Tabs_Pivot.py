from database import db
from Ingredients import Ingredient

# classe che relazione tabelle e ingredienti per i piani nutrizionali in postgreSQL
class PlanIngredient(db.Model):
    __tablename__ = 'planIngredients'
    
    plan_id = db.Column(db.Integer, db.ForeignKey('nutritionPlans.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    
    quantitaGrammi = db.Column(db.Float, nullable=False)
    ingredient = db.relationship(Ingredient)
    

# classe per il piano nutrizionale in PostgreSQL
class NutritionPlan(db.Model):
    __tablename__ = 'nutritionPlans'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Esempio: "High-Protein", "Low-Carb", ecc.
    is_preset = db.Column(db.Boolean, default=False)  # Indica se la scheda è preset o personalizzata
    
    ingredienti = db.relationship('PlanIngredient', backref='nutritionPlan', lazy=True)

    def to_dict(self):
        totale_proteine = 0
        totale_carboidrati = 0
        totale_grassi = 0
        totale_calorie = 0
        lista_alimenti = []
        
        for pi in self.ingredienti: 
            ing = pi.ingredient
            q = pi.quantitaGrammi
            
            proteine_calc = ing.proteine * q / 100
            carbo_calc = ing.carboidrati * q / 100
            grassi_calc = ing.grassi * q / 100
            calorie_calc = ing.calorie * q / 100

            totale_proteine += proteine_calc
            totale_carboidrati += carbo_calc
            totale_grassi += grassi_calc
            totale_calorie += calorie_calc

            # aggiunge i dettagli degli alimenti alla lista 
            lista_alimenti.append({
                "nome_alimento": ing.name,
                "quantita_g": q,
                "macro_parziali": {
                    "proteine": round(proteine_calc, 1),
                    "carboidrati": round(carbo_calc, 1),
                    "grassi": round(grassi_calc, 1),
                    "calorie": round(calorie_calc)
                }
            })

        # Funzione che serve a convertire l'oggetto "NutritionPlan" in un dizionario per poterlo restituire come JSON
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo,
            "is_preset": self.is_preset,
            "macro_totali": {
                "proteine": round(totale_proteine, 1), # arrotonda a 1 decimale
                "carboidrati": round(totale_carboidrati, 1),
                "grassi": round(totale_grassi, 1),
                "calorie": round(totale_calorie)
            },
            "dettaglio_alimenti": lista_alimenti
        }