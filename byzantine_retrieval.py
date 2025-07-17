import hashlib
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ShardProof:
    shard_id: str
    content: bytes
    merkle_path: List[bytes]

class ByzantineRetriever:
    def __init__(self, quorum_size=3, hash_algo="blake2b"):
        self.quorum_size = quorum_size
        self.hash_algo = hash_algo
        self.merkle_trees = {}

    def compute_merkle_root(self, shards: List[bytes]) -> bytes:
        if self.hash_algo == "blake2b":
            hasher = lambda d: hashlib.blake2b(d, digest_size=32).digest()
        
        leaf_hashes = [hasher(shard) for shard in shards]
        while len(leaf_hashes) > 1:
            new_level = []
            for i in range(0, len(leaf_hashes), 2):
                combined = leaf_hashes[i] + (leaf_hashes[i+1] if i+1 < len(leaf_hashes) else b'')
                new_level.append(hasher(combined))
            leaf_hashes = new_level
        return leaf_hashes[0]

    def validate_proof(self, root: bytes, proof: ShardProof) -> bool:
        current_hash = hashlib.blake2b(proof.content, digest_size=32).digest()
        for sibling in proof.merkle_path:
            current_hash = hashlib.blake2b(
                current_hash + sibling, digest_size=32
            ).digest()
        return current_hash == root

    def retrieve_shard(self, shard_id: str, nodes: Dict[str, ShardProof]) -> Optional[bytes]:
        valid_proofs = []
        for node_id, proof in nodes.items():
            if proof.shard_id == shard_id and self.validate_proof(
                self.merkle_trees[shard_id], proof
            ):
                valid_proofs.append(proof.content)
        
        if len(valid_proofs) >= self.quorum_size - 1:  # Byzantine tolerance
            return max(set(valid_proofs), key=valid_proofs.count)  # Majority consensus
        return None
