import time
import random
from tqdm import tqdm
from .erasure_coding import ErasureCoder
from .proof_of_storage import StorageAuditor
from .byzantine_retrieval import ByzantineRetriever

class SystemSimulator:
    def __init__(self, node_count=480, malicious_ratio=0.35):
        self.nodes = [f"node_{i}" for i in range(node_count)]
        self.malicious_nodes = set(random.sample(
            self.nodes, int(node_count * malicious_ratio)
        ))
        self.erasure_coder = ErasureCoder()
        self.auditor = StorageAuditor()
        self.retriever = ByzantineRetriever()
    
    def run_throughput_test(self, data_size=1_000_000, 
                           shards_per_block=250) -> float:
        test_data = os.urandom(data_size)
        start_time = time.perf_counter()
        
        for _ in tqdm(range(shards_per_block)):
            shards = self.erasure_coder.encode(test_data)
            for node in self.nodes:
                if node not in self.malicious_nodes:
                    self.auditor.generate_challenge(random.choice(shards))
        
        duration = time.perf_counter() - start_time
        return shards_per_block / duration  # TPS
    
    def run_byzantine_test(self, data_size=10_000) -> float:
        test_data = os.urandom(data_size)
        shards = self.erasure_coder.encode(test_data)
        shard_id = "test_shard_0"
        
        # Store across nodes
        proofs = {}
        for i, node in enumerate(self.nodes[:len(shards)]):
            proofs[node] = self._create_proof(
                shard_id, shards[i], 
                is_malicious=(node in self.malicious_nodes)
            )
        
        # Attempt retrieval
        success_count = 0
        for _ in range(100):
            if self.retriever.retrieve_shard(shard_id, proofs) is not None:
                success_count += 1
        
        return success_count / 100  # Success rate
    
    def _create_proof(self, shard_id: str, shard: bytes, 
                     is_malicious: bool) -> ShardProof:
        if is_malicious and random.random() > 0.3:  # 70% chance to alter
            corrupted = bytearray(shard)
            corrupted[random.randint(0, len(shard)-1)] ^= 0xFF
            shard = bytes(corrupted)
        return ShardProof(
            shard_id=shard_id,
            content=shard,
            merkle_path=[]  # Simplified for simulation
        )
