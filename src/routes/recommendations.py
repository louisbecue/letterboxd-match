from flask import Blueprint, request, jsonify

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    user_id = data.get('user_id')
    compatibility_score = data.get('compatibility_score')

    if not user_id or compatibility_score is None:
        return jsonify({'error': 'Invalid input'}), 400

    recommendation_engine = RecommendationEngine()
    recommendations = recommendation_engine.generate_recommendations(user_id, compatibility_score)

    return jsonify(recommendations)

@recommendations_bp.route('/recommendations')
def recommendations():
    return "Recommendations route"