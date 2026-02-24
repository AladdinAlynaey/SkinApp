"""
AI Assistant API Endpoints (RAG)
"""

from flask import Blueprint, request, jsonify, g
from storage.json_handler import JSONHandler
from utils.security import require_auth
from utils.helpers import format_error, now_iso, generate_id
from config import get_config


assistant_bp = Blueprint('assistant', __name__)
config = get_config()


def get_assistant_memory(user_id: str) -> dict:
    """Get or create assistant memory for user."""
    path = config.ASSISTANT_DIR / f"{user_id}.json"
    handler = JSONHandler(path)
    memory = handler.read()
    
    if not memory:
        memory = {
            "user_id": user_id,
            "created_at": now_iso(),
            "conversations": [],
            "context": {}
        }
        handler.write(memory)
    
    return memory


def save_assistant_memory(user_id: str, memory: dict):
    """Save assistant memory."""
    path = config.ASSISTANT_DIR / f"{user_id}.json"
    handler = JSONHandler(path)
    handler.write(memory)


@assistant_bp.route('/chat', methods=['POST'])
@require_auth()
def chat():
    """Send message to AI assistant."""
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify(format_error("Message required")), 400
    
    # Get user memory
    memory = get_assistant_memory(g.user_id)
    
    # Add user message
    user_msg = {
        "id": generate_id(),
        "role": "user",
        "content": message,
        "timestamp": now_iso()
    }
    memory['conversations'].append(user_msg)
    
    # Generate response using AI service
    try:
        from services.assistant_service import generate_response
        response_text = generate_response(
            message=message,
            user_id=g.user_id,
            user_type=g.user_type,
            conversation_history=memory['conversations'][-10:]  # Last 10 messages
        )
    except Exception as e:
        response_text = "I apologize, but I'm currently unable to process your request. Please try again later."
    
    # Add assistant response
    assistant_msg = {
        "id": generate_id(),
        "role": "assistant",
        "content": response_text,
        "timestamp": now_iso()
    }
    memory['conversations'].append(assistant_msg)
    
    # Keep only last 100 messages
    if len(memory['conversations']) > 100:
        memory['conversations'] = memory['conversations'][-100:]
    
    save_assistant_memory(g.user_id, memory)
    
    return jsonify({
        "response": response_text,
        "message_id": assistant_msg['id']
    })


@assistant_bp.route('/history', methods=['GET'])
@require_auth()
def get_history():
    """Get conversation history."""
    limit = request.args.get('limit', 50, type=int)
    
    memory = get_assistant_memory(g.user_id)
    conversations = memory.get('conversations', [])[-limit:]
    
    return jsonify({
        "messages": conversations,
        "total": len(conversations)
    })


@assistant_bp.route('/clear', methods=['POST'])
@require_auth()
def clear_history():
    """Clear conversation history."""
    memory = get_assistant_memory(g.user_id)
    memory['conversations'] = []
    memory['context'] = {}
    save_assistant_memory(g.user_id, memory)
    
    return jsonify({"message": "Conversation history cleared"})
