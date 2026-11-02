from database import db
from Ingredients import Ingredient
from Tabs_Pivot import NutritionPlan, PlanIngredient

# Inizializzazione della Struttura del Database 
def inizializza_dati_base():
    # Crea le tabelle
    db.create_all()
    
    # Se la lista è vuota, aggiunge i seguenti ingredienti:
    if Ingredient.query.count() == 0: # lista vuota
        alimenti_base = [
            Ingredient(name="Avena Istantanea", protein=11.0, carbs=61.0, fats=7.7, calories=388),
            Ingredient(name="Proteine del Siero del Latte (Whey)", protein=82.0, carbs=4.0, fats=7.5, calories=412),
            Ingredient(name="Burro di Arachidi", protein=30.0, carbs=12.0, fats=46.0, calories=579),
            Ingredient(name="Yogurt Greco 0%", protein=10.3, carbs=4.0, fats=0.0, calories=57),
            Ingredient(name="Cacao Amaro in Polvere", protein=20.0, carbs=11.0, fats=21.0, calories=320),
            Ingredient(name="Farina di Cocco", protein=18.0, carbs=18.0, fats=16.0, calories=320)
        ]
        db.session.bulk_save_objects(alimenti_base) # Aggiunge gli ingredienti al database
        db.session.commit() # Salva le modifiche nel database
        print("Database initialized with ingredients!")

    # Se la lista è vuota, aggiunge i seguenti ingredienti:
    if NutritionPlan.query.count() == 0:
        whey = Ingredient.query.filter_by(name="Proteine del Siero del Latte (Whey)").first()
        avena = Ingredient.query.filter_by(name="Avena Istantanea").first()
        yogurt = Ingredient.query.filter_by(name="Yogurt Greco 0%").first()

        if whey and avena and yogurt:
            scheda_high_protein = NutritionPlan(nome="Colazione Ricomposizione", tipo="High-Protein", is_preset=True)
            scheda_high_protein.ingredienti.append(PlanIngredient(ingredient=whey, quantitaGrammi=40))
            scheda_high_protein.ingredienti.append(PlanIngredient(ingredient=avena, quantitaGrammi=60))
            scheda_high_protein.ingredienti.append(PlanIngredient(ingredient=yogurt, quantitaGrammi=150))

            db.session.add(scheda_high_protein) # Aggiunge gli ingredienti al database
            db.session.commit() # Salva le modifiche nel database
            print("Scheda preset 'High-Protein' generata!")