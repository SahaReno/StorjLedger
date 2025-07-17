import numpy as np
from typing import List, Tuple
from galois import GF, ReedSolomon

class ErasureCoder:
    def __init__(self, data_shards=29, parity_shards=55):
        self.gf = GF(2**8)
        self.rs = ReedSolomon(data_shards, parity_shards, field=self.gf)
        self.shard_size = 256  # bytes

    def encode(self, data: bytes) -> List[bytes]:
        padded_data = data + b'\0' * (self.shard_size - (len(data) % self.shard_size))
        data_blocks = [padded_data[i:i+self.shard_size] 
                      for i in range(0, len(padded_data), self.shard_size)]
        
        encoded_shards = []
        for block in data_blocks:
            int_array = np.frombuffer(block, dtype=np.uint8)
            encoded_block = self.rs.encode(int_array)
            encoded_shards.append(encoded_block.tobytes())
        
        return encoded_shards

    def decode(self, shards: List[bytes]) -> bytes:
        valid_shards = [s for s in shards if s is not None]
        if len(valid_shards) < self.rs.k:
            raise ValueError("Insufficient shards for reconstruction")
        
        decoded_blocks = []
        for i in range(0, len(valid_shards[0]), self.shard_size):
            block_shards = [s[i:i+self.shard_size] for s in valid_shards]
            int_arrays = [np.frombuffer(s, dtype=np.uint8) for s in block_shards]
            decoded_block = self.rs.decode(int_arrays[:self.rs.k])
            decoded_blocks.append(decoded_block.tobytes())
        
        return b''.join(decoded_blocks).rstrip(b'\0')

    def durability_probability(self, total_nodes=84, failure_rate=0.01) -> float:
        lambda_param = total_nodes * failure_rate / (self.rs.k + self.rs.m)
        p_loss = np.exp(-lambda_param) * sum(
            lambda_param**i / np.math.factorial(i) 
            for i in range(self.rs.k)
        )
        return 1 - p_loss
