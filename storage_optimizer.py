import hashlib
import math
from typing import Tuple

class StorageOptimizer:
    def __init__(self, anchor_size=64, merkle_hash="blake2b"):
        self.anchor_size = anchor_size
        self.merkle_hash = merkle_hash
    
    def create_metadata_anchor(self, shard_ids: List[str], 
                              merkle_root: bytes) -> bytes:
        concatenated = b''.join([sid.encode() for sid in shard_ids]) + merkle_root
        if self.merkle_hash == "blake2b":
            return hashlib.blake2b(concatenated, digest_size=self.anchor_size).digest()
        else:
            return hashlib.sha3_512(concatenated).digest()[:self.anchor_size]
    
    def merkle_proof_size(self, total_shards: int) -> int:
        tree_depth = math.ceil(math.log2(total_shards))
        if self.merkle_hash == "blake2b":
            return tree_depth * 32  # 256-bit hashes
        else:
            return tree_depth * 64  # 512-bit fallback
    
    def storage_savings(self, original_size: int, 
                       optimized_size: int) -> Tuple[float, float]:
        reduction = original_size - optimized_size
        return reduction, reduction / original_size * 100
    
    def sharding_overhead(self, data_shards: int, parity_shards: int) -> float:
        return (data_shards + parity_shards) / data_shards
