"""
Wallet Store - JSON-based wallet and transaction storage
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, List
from .json_handler import JSONHandler
from config import get_config


class WalletStore:
    """Manages wallet balances and transactions in JSON files."""
    
    def __init__(self, config=None):
        self.config = config or get_config()
        self.wallets_dir = self.config.WALLETS_DIR
        self.transactions_dir = self.config.TRANSACTIONS_DIR
    
    def get_or_create_wallet(self, user_id: str, user_type: str) -> Dict:
        """Get wallet or create if doesn't exist."""
        handler = JSONHandler(self.wallets_dir / f"{user_id}.json")
        wallet = handler.read()
        
        if not wallet:
            wallet = {
                "user_id": user_id,
                "user_type": user_type,
                "balance": 0.0,
                "currency": "USD",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": 1
            }
            handler.write(wallet)
        
        return wallet
    
    def get_balance(self, user_id: str) -> float:
        """Get current balance."""
        wallet = self.get_or_create_wallet(user_id, 'patient')
        return wallet.get('balance', 0.0)
    
    def deposit(self, user_id: str, amount: float, description: str = "Deposit") -> Dict:
        """Add funds to wallet."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        handler = JSONHandler(self.wallets_dir / f"{user_id}.json")
        
        def do_deposit(wallet):
            wallet = wallet or self.get_or_create_wallet(user_id, 'patient')
            wallet['balance'] = round(wallet['balance'] + amount, 2)
            wallet['version'] += 1
            wallet['updated_at'] = datetime.now().isoformat()
            return wallet
        
        result = handler.update(do_deposit)
        self._record_transaction(user_id, 'deposit', amount, result['balance'], description)
        return result
    
    def debit(self, user_id: str, amount: float, description: str, 
              reference_id: str = None) -> Dict:
        """Deduct funds from wallet."""
        if amount <= 0:
            raise ValueError("Debit amount must be positive")
        
        handler = JSONHandler(self.wallets_dir / f"{user_id}.json")
        
        def do_debit(wallet):
            if not wallet or wallet['balance'] < amount:
                raise ValueError("Insufficient balance")
            wallet['balance'] = round(wallet['balance'] - amount, 2)
            wallet['version'] += 1
            wallet['updated_at'] = datetime.now().isoformat()
            return wallet
        
        result = handler.update(do_debit)
        self._record_transaction(user_id, 'debit', amount, result['balance'], 
                                description, reference_id)
        return result
    
    def credit(self, user_id: str, amount: float, description: str,
               reference_id: str = None) -> Dict:
        """Credit funds (for doctor earnings)."""
        if amount <= 0:
            raise ValueError("Credit amount must be positive")
        
        handler = JSONHandler(self.wallets_dir / f"{user_id}.json")
        
        def do_credit(wallet):
            wallet = wallet or self.get_or_create_wallet(user_id, 'doctor')
            wallet['balance'] = round(wallet['balance'] + amount, 2)
            wallet['version'] += 1
            wallet['updated_at'] = datetime.now().isoformat()
            return wallet
        
        result = handler.update(do_credit)
        self._record_transaction(user_id, 'credit', amount, result['balance'],
                                description, reference_id)
        return result
    
    def _record_transaction(self, user_id: str, txn_type: str, amount: float,
                           balance_after: float, description: str, 
                           reference_id: str = None):
        """Record transaction in user's transaction history."""
        txn = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "type": txn_type,
            "amount": amount,
            "balance_after": balance_after,
            "description": description,
            "reference_id": reference_id,
            "timestamp": datetime.now().isoformat()
        }
        
        # Store in daily transaction file
        date_str = datetime.now().strftime('%Y-%m-%d')
        handler = JSONHandler(self.transactions_dir / f"{date_str}.json")
        
        def append_txn(data):
            data = data or {"date": date_str, "transactions": []}
            data["transactions"].append(txn)
            return data
        
        handler.update(append_txn)
    
    def get_transactions(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's transaction history."""
        from .json_handler import list_json_files
        
        transactions = []
        for file_path in sorted(list_json_files(self.transactions_dir), reverse=True):
            data = JSONHandler(file_path).read()
            if data:
                for txn in data.get('transactions', []):
                    if txn.get('user_id') == user_id:
                        transactions.append(txn)
                        if len(transactions) >= limit:
                            return transactions
        return transactions
