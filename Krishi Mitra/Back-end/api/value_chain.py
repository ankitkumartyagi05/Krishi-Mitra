from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from services.value_chain_service import ValueChainService

value_chain_bp = Blueprint('value_chain', __name__)

@value_chain_bp.route('/buyers', methods=['GET'])
@jwt_required()
def get_buyers():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get parameters
    crop = request.args.get('crop', 'wheat')
    state = request.args.get('state', user.location or 'Delhi')
    district = request.args.get('district')
    
    # Get value chain service
    value_chain_service = ValueChainService()
    
    # Get buyers
    buyers = value_chain_service.get_buyers(crop, state, district)
    
    return jsonify(buyers)

@value_chain_bp.route('/suppliers', methods=['GET'])
@jwt_required()
def get_suppliers():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get parameters
    crop = request.args.get('crop', 'wheat')
    state = request.args.get('state', user.location or 'Delhi')
    district = request.args.get('district')
    
    # Get value chain service
    value_chain_service = ValueChainService()
    
    # Get suppliers
    suppliers = value_chain_service.get_input_suppliers(crop, state, district)
    
    return jsonify(suppliers)

@value_chain_bp.route('/logistics', methods=['GET'])
@jwt_required()
def get_logistics():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get parameters
    state = request.args.get('state', user.location or 'Delhi')
    district = request.args.get('district')
    
    # Get value chain service
    value_chain_service = ValueChainService()
    
    # Get logistics providers
    logistics = value_chain_service.get_logistics_providers(state, district)
    
    return jsonify(logistics)

@value_chain_bp.route('/listings', methods=['GET', 'POST'])
@jwt_required()
def market_listings():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if request.method == 'POST':
        # Create new listing
        data = request.get_json()
        crop = data.get('crop', 'wheat')
        quantity = data.get('quantity', 0)
        price = data.get('price', 0)
        
        value_chain_service = ValueChainService()
        listing = value_chain_service.create_market_listing(user, crop, quantity, price)
        
        return jsonify(listing)
    else:
        # Get listings
        crop = request.args.get('crop')
        state = request.args.get('state')
        
        value_chain_service = ValueChainService()
        listings = value_chain_service.get_market_listings(crop, state)
        
        return jsonify(listings)

@value_chain_bp.route('/connect', methods=['POST'])
@jwt_required()
def connect_with_buyer():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    listing_id = data.get('listing_id')
    buyer_id = data.get('buyer_id')
    
    value_chain_service = ValueChainService()
    connection = value_chain_service.connect_with_buyer(listing_id, buyer_id, user)
    
    return jsonify(connection)

@value_chain_bp.route('/group-procurement', methods=['GET', 'POST'])
@jwt_required()
def group_procurement():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if request.method == 'POST':
        # Create new group procurement
        data = request.get_json()
        crop = data.get('crop', 'fertilizer')
        quantity = data.get('quantity', 0)
        
        value_chain_service = ValueChainService()
        group = value_chain_service.create_group_procurement(user, crop, quantity)
        
        return jsonify(group)
    else:
        # Get group procurements
        crop = request.args.get('crop')
        state = request.args.get('state')
        
        value_chain_service = ValueChainService()
        groups = value_chain_service.get_group_procurements(crop, state)
        
        return jsonify(groups)

@value_chain_bp.route('/join-group', methods=['POST'])
@jwt_required()
def join_group():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    group_id = data.get('group_id')
    
    value_chain_service = ValueChainService()
    result = value_chain_service.join_group_procurement(group_id, user)
    
    return jsonify(result)