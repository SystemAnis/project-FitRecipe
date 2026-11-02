from flask import Blueprint, jsonify
from Tabs_Pivot import NutritionPlan

# Creiamo il Blueprint per le schede
api_schede = Blueprint('api_schede', __name__)

# Endpoint REST per ottenere le schede nutrizionali
@api_schede.route('/api/plans', methods=['GET'])
def ottieni_schede():
    schede = NutritionPlan.query.all() # Ottiene tutte le schede nutrizionali dal database
    return jsonify([s.to_dict() for s in schede]) # Restituisce la lista delle schede nutrizionali come JSON
