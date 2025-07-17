from typing import Dict, List, Set
from collections import defaultdict
from .node_reputation import ReputationEngine

class ShardRedistributor:
    def __init__(self, min_reputation=80, redundancy_factor=3):
        self.min_reputation = min_reputation
        self.redundancy = redundancy_factor
        self.reputation_engine = ReputationEngine()
    
    def redistribute(self, failed_node: str, shards: Set[str], 
                    node_capacities: Dict[str, int]) -> Dict[str, List[str]]:
        # Step 1: Identify candidate nodes
        candidates = [
            node for node, cap in node_capacities.items()
            if cap > 0 and self.reputation_engine.get_reputation(node) >= self.min_reputation
        ]
        
        # Step 2: Create load-aware distribution plan
        redistribution_plan = defaultdict(list)
        node_loads = {node: 0 for node in candidates}
        
        for shard in shards:
            # Select node with lowest current load
            target_node = min(candidates, key=lambda n: node_loads[n])
            redistribution_plan[target_node].append(shard)
            node_loads[target_node] += 1
            
            # Create replicas
            for _ in range(self.redundancy - 1):
                replica_node = min(
                    (n for n in candidates if n != target_node),
                    key=lambda n: node_loads[n]
                )
                redistribution_plan[replica_node].append(f"{shard}_replica")
                node_loads[replica_node] += 1
        
        # Step 3: Update metadata anchors
        metadata_updates = {}
        for node, assigned_shards in redistribution_plan.items():
            for shard in assigned_shards:
                metadata_updates[shard] = {
                    'location': node,
                    'timestamp': time.time_ns()
                }
        
        return redistribution_plan, metadata_updates
