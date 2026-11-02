from database import db
from Ingredients import Ingredient

# Tabella Pivot: Collega la Scheda all'Ingrediente e salva i grammi
class PlanIngredient(db.Model):
    __tablename__ = 'planIngredients'
    
    # Chiavi esterne (Foreign Keys) che puntano alle due tabelle principali.
    # Insieme formano la chiave primaria composta della tabella pivot.
    plan_id = db.Column(db.Integer, db.ForeignKey('nutritionPlans.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    
    # quantità in grammi per questo specifico alimento nella scheda
    quantitaGrammi = db.Column(db.Float, nullable=False)
    
    # Relazione per accedere comodamente ai dati dell'ingrediente
    ingredient = db.relationship(Ingredient)
    

# Modello della Scheda Nutrizionale
class NutritionPlan(db.Model):
    __tablename__ = 'nutritionPlans'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Es. "High-Protein", "Ipocalorica Standard"
    is_preset = db.Column(db.Boolean, default=False)  # Indica se la scheda è preset o personalizzata
    
    # Relazione verso la tabella pivot (se elimino la scheda, elimino i collegamenti)
    ingredienti = db.relationship(
        'PlanIngredient',
        backref='nutritionPlan',
        lazy=True,
        cascade='all, delete-orphan'  # eliminando la scheda, elimina anche i suoi collegamenti
    )

    # calcola automaticamente i macro totali della scheda
    def to_dict(self):
        totale_proteine = 0
        totale_carboidrati = 0
        totale_grassi = 0
        totale_calorie = 0
        lista_alimenti = []
        
        for pi in self.ingredienti:
            ing = pi.ingredient
            q = pi.quantitaGrammi
            
            # Proporzione: (macro per 100g / 100) * grammi effettivi
            proteine_calc = (ing.protein / 100) * q
            carbo_calc = (ing.carbs / 100) * q
            grassi_calc = (ing.fats / 100) * q
            calorie_calc = (ing.calories / 100) * q 

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