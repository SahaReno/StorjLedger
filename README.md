# StorjLedger

**StorjLedger** is an innovative framework that integrates Storj’s decentralized storage network with a Proof-of-Storage (PoS) blockchain consensus mechanism to address the blockchain trilemma of scalability, security, and decentralization. StorjLedger partitions data into erasure‑coded shards, distributes them across a global network of storage nodes, and anchors minimal metadata on-chain for efficient, secure, and transparent data storage.

## Features

- **Erasure‑Coded Sharding**  
  - Reed‑Solomon encoding (29 data + 55 parity shards)  
  - 256‑byte shard size for fine‑grained distribution  
- **Proof‑of‑Storage Consensus**  
  - Periodic HMAC‑SHA256 audits for shard availability  
  - Token‑staking and slashing for misbehaving nodes  
- **End‑to‑End Encryption**  
  - Client‑side AES‑256‑GCM encryption  
  - Shamir’s Secret Sharing for key management (3/5 threshold)  
- **Dynamic Reputation System**  
  - Hourly reputation updates based on audit performance and latency  
  - Blacklisting for low‑reputation nodes  
- **Byzantine‑Resilient Retrieval**  
  - Sparse Merkle Trees with BLAKE2b‑256  
  - Quorum‑based shard retrieval for fault tolerance  
- **Network Layer & Gossip Protocol**  
  - Kademlia DHT with UDP hole punching  
  - Bloom filter‑backed metadata propagation  

## Architecture

Refer to the [project report](docs/report.pdf) for detailed diagrams. The core components include:

1. **Client CLI / SDK**  
2. **Shard Manager**  
3. **Audit & Consensus Module**  
4. **Key Management Nodes (KMNs)**  
5. **Storage Nodes (Storj DSN gateways)**  

## Getting Started

### Prerequisites

- **Docker** & **Docker Compose**  
- **Go** (>= 1.18) for core services  
- **Node.js** (>= 16) for CLI/SDK  
- **Storj Account** & API credentials  

### Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/SahaReno/StorjLedger.git
   cd StorjLedger
   ```

2. **Configure Environment**  
   Copy the sample `.env.example` and fill in your credentials:  
   ```bash
   cp .env.example .env
   # Edit .env with your Storj API credentials and blockchain node endpoints
   ```

3. **Launch Dependencies**  
   ```bash
   docker-compose up -d
   ```

4. **Build Services**  
   ```bash
   make build
   ```

## Usage

### Start the Client

```bash
./bin/cli upload --file ./data/sample.txt
./bin/cli download --id <file‑anchor>
```

### Run a Local Testnet

```bash
./scripts/run_testnet.sh
```

## Configuration

- **Shard & Audit Parameters**  
  Adjust shard count, audit interval, and staking thresholds in `config/config.yaml`.

- **Key Management**  
  KMN details and VRF settings in `config/keys.yaml`.

## Contributing

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/fooBar`)  
3. Commit your changes (`git commit -am 'Add some fooBar'`)  
4. Push to the branch (`git push origin feature/fooBar`)  
5. Open a Pull Request

Please follow the [Contributor Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Contact

- **Authors**: Saha Reno (<reno.saha39@gmail.com>), Koushik Roy (<rkoushik755@gmail.com>)  
- **GitHub**: https://github.com/SahaReno/StorjLedger  
- **Report**: Will be available soon.  
