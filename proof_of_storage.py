import hmac
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Optional

class StorageAuditor:
    def __init__(self, token_symbol="STORJ"):
        self.token_symbol = token_symbol
        self.node_reputations = {}
        self.stake_balances = {}

    def generate_challenge(self, shard: bytes) -> bytes:
        nonce = hashlib.sha256(str(id(shard)).digest()
        return hmac.new(
            key=nonce,
            msg=shard,
            digestmod=hashlib.sha256
        ).digest()

    def verify_response(self, shard: bytes, response: bytes, 
                       original_hash: bytes) -> bool:
        expected = self.generate_challenge(shard)
        return hmac.compare_digest(expected, response)

    def process_audit(self, node_id: str, failures: int) -> float:
        reputation = self.node_reputations.get(node_id, 100)
        slash_percent = 0.1 if reputation < 50 else 0
        
        if failures > 0:
            new_reputation = 0.7 * reputation + 0.3 * (0.8 * (1 - failures) + 0.2)
            self.node_reputations[node_id] = max(new_reputation, 0)
        
        slashed = self.stake_balances.get(node_id, 100) * slash_percent
        self.stake_balances[node_id] -= slashed
        return slashed

    def derive_audit_key(self, passphrase: str, salt: bytes, 
                        iterations=100000) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=iterations
        )
        return kdf.derive(passphrase.encode())
