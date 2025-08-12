from livekit import api
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow frontend connections

@app.route('/get-token', methods=['POST'])
def get_token():
    """Generate LiveKit token for frontend"""
    try:
        data = request.json
        user_name = data.get('userName', 'राजेश जी')
        room_name = data.get('roomName', 'meera-health-room')
        
        # Your LiveKit credentials
        api_key = os.getenv('LIVEKIT_API_KEY')
        api_secret = os.getenv('LIVEKIT_API_SECRET')
        
        if not api_key or not api_secret:
            return jsonify({'error': 'LiveKit credentials not configured'}), 500
        
        # Generate token
        token = api.AccessToken(api_key, api_secret) \
            .with_identity(user_name) \
            .with_name(user_name) \
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True
            )).to_jwt()
        
        return jsonify({
            'token': token,
            'url': os.getenv('LIVEKIT_URL', 'wss://mywifu-vvk52760.livekit.cloud')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Meera token server is running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug, port=port, host='0.0.0.0')
