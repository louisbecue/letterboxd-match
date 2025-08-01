from flask import Blueprint, request, jsonify

compare_bp = Blueprint('compare', __name__)

@compare_bp.route('/compare', methods=['POST'])
def compare_users():
    data = request.json
    user1_id = data.get('user1_id')
    user2_id = data.get('user2_id')

    user1_data = fetch_user_data(user1_id)
    user2_data = fetch_user_data(user2_id)

    if not user1_data or not user2_data:
        return jsonify({'error': 'User data not found'}), 404

    compatibility_calculator = CompatibilityCalculator()
    score = compatibility_calculator.calculate_score(user1_data['watched_movies'], user2_data['watched_movies'])

    recommendation_engine = RecommendationEngine()
    recommendations = recommendation_engine.generate_recommendations(user1_data, user2_data)

    return jsonify({
        'compatibility_score': score,
        'recommendations': recommendations
    })

@compare_bp.route('/compare')
def compare():
    return "Compare route"