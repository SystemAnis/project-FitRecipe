from flask import Blueprint, jsonify
from Ingredients import Ingredient

# Creiamo il Blueprint per gli ingredienti
api_ingredienti = Blueprint('api_ingredienti', __name__)

@api_ingredienti.route('/api/ingredients', methods=['GET'])
def ottieni_ingredienti():
    ingredienti = Ingredient.query.all()
    return jsonify([ing.to_dict() for ing in ingredienti])