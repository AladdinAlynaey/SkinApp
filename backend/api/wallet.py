"""
Wallet API Endpoints
"""

from flask import Blueprint, request, jsonify, g
from storage import WalletStore
from utils.security import require_auth
from utils.helpers import format_error
from config import get_config


wallet_bp = Blueprint('wallet', __name__)
wallet_store = WalletStore()
config = get_config()


@wallet_bp.route('/balance', methods=['GET'])
@require_auth()
def get_balance():
    """Get current wallet balance."""
    wallet = wallet_store.get_or_create_wallet(g.user_id, g.user_type)
    
    return jsonify({
        "balance": wallet['balance'],
        "currency": wallet['currency']
    })


@wallet_bp.route('/deposit', methods=['POST'])
@require_auth()
def deposit():
    """Add funds to wallet."""
    data = request.get_json()
    amount = data.get('amount', 0)
    
    # Get pricing config
    from storage.json_handler import safe_read
    pricing = safe_read(config.CONFIG_DIR / 'pricing.json', {})
    wallet_config = pricing.get('wallet', {})
    
    min_deposit = wallet_config.get('min_deposit', 10)
    max_deposit = wallet_config.get('max_deposit', 1000)
    
    if amount < min_deposit:
        return jsonify(format_error(f"Minimum deposit: ${min_deposit}")), 400
    
    if amount > max_deposit:
        return jsonify(format_error(f"Maximum deposit: ${max_deposit}")), 400
    
    try:
        # In production, integrate with payment gateway here
        wallet = wallet_store.deposit(g.user_id, amount, "Wallet deposit")
        
        return jsonify({
            "message": "Deposit successful",
            "new_balance": wallet['balance'],
            "amount_deposited": amount
        })
        
    except ValueError as e:
        return jsonify(format_error(str(e))), 400


@wallet_bp.route('/transactions', methods=['GET'])
@require_auth()
def get_transactions():
    """Get transaction history."""
    limit = request.args.get('limit', 50, type=int)
    
    transactions = wallet_store.get_transactions(g.user_id, limit=limit)
    
    return jsonify({
        "transactions": transactions,
        "total": len(transactions)
    })


@wallet_bp.route('/withdraw', methods=['POST'])
@require_auth(['doctor'])
def withdraw():
    """Withdraw earnings (doctors only)."""
    data = request.get_json()
    amount = data.get('amount', 0)
    
    wallet = wallet_store.get_or_create_wallet(g.user_id, 'doctor')
    
    if amount <= 0:
        return jsonify(format_error("Invalid withdrawal amount")), 400
    
    if amount > wallet['balance']:
        return jsonify(format_error("Insufficient balance")), 400
    
    try:
        # In production, process bank transfer here
        updated = wallet_store.debit(
            g.user_id, amount, 
            "Withdrawal to bank account"
        )
        
        return jsonify({
            "message": "Withdrawal initiated",
            "amount": amount,
            "new_balance": updated['balance']
        })
        
    except ValueError as e:
        return jsonify(format_error(str(e))), 400
