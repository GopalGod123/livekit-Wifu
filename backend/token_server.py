from livekit import api
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import threading
import signal
import sys

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow frontend connections

# Track per-session agent processes: key = (room, identity)
AGENT_PROCS = {}

def _proc_key(room: str, identity: str) -> tuple:
    return (room or "", identity or "")

def start_agent(room: str, identity: str) -> bool:
    key = _proc_key(room, identity)
    # Already running?
    proc = AGENT_PROCS.get(key)
    if proc and proc.poll() is None:
        return True
    # Spawn agent in connect mode targeting the participant
    cmd = [
        sys.executable or "python",
        "-u",
        "agent.py",
        "connect",
        "--room",
        room,
        "--participant-identity",
        identity,
    ]
    env = os.environ.copy()
    # Avoid port clash with web server: force agent to use AGENT_PORT (default 9000)
    env["PORT"] = os.getenv("AGENT_PORT", "9000")
    p = subprocess.Popen(cmd, cwd=os.path.dirname(__file__), env=env)
    AGENT_PROCS[key] = p
    return True

def stop_agent(room: str, identity: str) -> bool:
    key = _proc_key(room, identity)
    proc = AGENT_PROCS.get(key)
    if not proc:
        return False
    if proc.poll() is None:
        try:
            # Graceful terminate, then kill if needed
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
        except Exception:
            pass
    AGENT_PROCS.pop(key, None)
    return True

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

@app.route('/agent/start', methods=['POST'])
def agent_start():
    try:
        data = request.json or {}
        user_name = data.get('userName')
        room_name = data.get('roomName')
        if not user_name or not room_name:
            return jsonify({'error': 'userName and roomName required'}), 400
        started = start_agent(room_name, user_name)
        return jsonify({'started': started})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/agent/stop', methods=['POST'])
def agent_stop():
    try:
        data = request.json or {}
        user_name = data.get('userName')
        room_name = data.get('roomName')
        if not user_name or not room_name:
            return jsonify({'error': 'userName and roomName required'}), 400
        stopped = stop_agent(room_name, user_name)
        return jsonify({'stopped': stopped})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug, port=port, host='0.0.0.0')
