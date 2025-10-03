from flask import Blueprint

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/test')
def test():
    return "Chat API works"