from flask import Blueprint, request, jsonify, make_response
from models.alternativa import Alternativa
from utils.db import db
from schemas.alternativa_schema import alternativa_schema, alternativas_schema

alternativas = Blueprint('alternativas', __name__)

@alternativas.route('/alternativas/get', methods=['GET'])
def get_alternativas():
    alternativas = Alternativa.query.all()
    result = alternativas_schema.dump(alternativas)
    
    data = {
        'message': 'Lista generada con éxito',
        'status': 200,
        'alternativas': result
    }

    return make_response(jsonify(data), 200)

@alternativas.route('/alternativas/insert', methods=['POST'])
def insert():
    data = request.get_json()
    id_pregunta = data.get('id_pregunta')
    texto = data.get('texto')
    puntaje = data.get('puntaje')
    
    if not id_pregunta or not texto or not puntaje:
        data = {
            'message': 'Faltan datos',
            'status': 400
        }
        
        return make_response(jsonify(data), 400)
    
    alternativa = Alternativa(id_pregunta, texto, puntaje)
    db.session.add(alternativa)
    db.session.commit()
    
    result = alternativa_schema.dump(alternativa)
    
    data = {
        'message': 'Alternativa creada con éxito',
        'status': 201,
        'data': result
    }
    
    return make_response(jsonify(result), 201)

@alternativas.route('/alternativas/update/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    alternativa = Alternativa.query.get(id)
    
    if alternativa:
        alternativa.id_pregunta = data.get('id_pregunta')
        alternativa.texto = data.get('texto')
        alternativa.puntaje = data.get('puntaje')
        db.session.commit()
        
        result = alternativa_schema.dump(alternativa)
        
        data = {
            'message': 'Alternativa actualizada con éxito',
            'status': 200,
            'data': result
        }
        
        return make_response(jsonify(data), 200)
    
    data = {
        'message': 'Alternativa no encontrada',
        'status': 404
    }
    
    return make_response(jsonify(data), 404)

@alternativas.route('/alternativas/delete/<int:id>', methods=['DELETE'])
def delete(id):
    alternativa = Alternativa.query.get(id)
    
    if alternativa:
        db.session.delete(alternativa)
        db.session.commit()
        
        data = {
            'message': 'Alternativa eliminada con éxito',
            'status': 200
        }
        
        return make_response(jsonify(data), 200)
    
    data = {
        'message': 'Alternativa no encontrada',
        'status': 404
    }
    
    return make_response(jsonify(data), 404)