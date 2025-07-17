import time
import numpy as np
from typing import Dict

class ReputationEngine:
    def __init__(self, w1=0.8, w2=0.2, decay_rate=0.01):
        self.w1 = w1  # Audit weight
        self.w2 = w2  # Latency weight
        self.decay_rate = decay_rate  # Per hour
        self.node_states = {}  # {node_id: (reputation, last_update)}
    
    def update_reputation(self, node_id: str, audit_pass: bool, 
                         latency_ms: float) -> float:
        now = time.time()
        old_rep, last_update = self.node_states.get(node_id, (100, now))
        
        # Apply time decay
        hours_elapsed = (now - last_update) / 3600
        decayed_rep = old_rep * np.exp(-self.decay_rate * hours_elapsed)
        
        # Calculate new components
        audit_score = 1.0 if audit_pass else 0.0
        latency_score = 1.0 / max(latency_ms, 1.0)  # Avoid division by zero
        
        # Weighted update
        new_rep = 0.7 * decayed_rep + 0.3 * (
            self.w1 * audit_score + self.w2 * latency_score
        )
        self.node_states[node_id] = (new_rep, now)
        return new_rep
    
    def get_reputation(self, node_id: str) -> float:
        return self.node_states.get(node_id, (100, time.time()))[0]
    
    def blacklist_check(self, node_id: str) -> bool:
        return self.get_reputation(node_id) < 50
    
    def reward_multiplier(self, node_id: str) -> float:
        rep = self.get_reputation(node_id)
        return 1.15 if rep >= 90 else 1.0
