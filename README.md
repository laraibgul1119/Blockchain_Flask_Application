# Blockchain Flask Application

This project implements a simple blockchain using Python and Flask. It provides a RESTful API for mining blocks, adding transactions, registering nodes, and achieving consensus across a decentralized network.

---

## Table of Contents

- Overview
- Class: Blockchain
  - Attributes
  - Methods
- Flask API Endpoints
- How to Run
- Dependencies
- Example Usage

---

## Overview

The application simulates a basic blockchain with the following features:

- Block mining with proof-of-work
- Transaction recording
- Node registration for a decentralized network
- Consensus algorithm to resolve conflicts

---

## Class: Blockchain

### Attributes

- `chain`: List of all blocks in the blockchain.
- `current_transactions`: List of transactions to be added to the next block.
- `nodes`: Set of network node addresses.

### Methods

- `__init__()`: Initializes the blockchain with a genesis block.
- `valid_chain(chain)`: Checks if a given blockchain is valid.
- `resolve_conflict()`: Consensus algorithm to resolve conflicts by replacing the chain with the longest valid one in the network.
- `register_node(address)`: Adds a new node to the network.
- `proof_of_work(last_proof)`: Simple proof-of-work algorithm.
- `valid_proof(last_proof, proof)`: Validates the proof.
- `new_block(proof, previous_hash=None)`: Creates a new block and adds it to the chain.
- `new_transaction(sender, recipient, amount)`: Adds a new transaction to the list.
- `hash(block)`: Creates a SHA-256 hash of a block.
- `last_block`: Returns the last block in the chain.

---

## Flask API Endpoints

### `GET /mine`

Mines a new block, adds a reward transaction, and returns the new block's details.

### `POST /transactions/new`

Adds a new transaction to the list. Requires JSON body with `sender`, `recipient`, and `amount`.

### `GET /chain`

Returns the full blockchain and its length.

### `POST /nodes/register`

Registers new nodes to the network. Requires JSON body with a list of node addresses.

### `GET /nodes/resolve`

Runs the consensus algorithm to resolve conflicts and ensure the node has the authoritative chain.

---

## How to Run

1. Install dependencies:
   ```
   pip install flask requests
   ```
2. Run the application:
   ```
   python app.py
   ```
3. The API will be available at `http://localhost:5000/`.

---

## Dependencies

- Flask
- Requests
- Python Standard Library (hashlib, json, time, uuid, urllib)

---

## Example Usage

- **Mine a block:**  
  `GET http://localhost:5000/mine`

- **Add a transaction:**  
  `POST http://localhost:5000/transactions/new`  
  ```json
  {
    "sender": "address1",
    "recipient": "address2",
    "amount": 5
  }
  ```

- **Register nodes:**  
  `POST http://localhost:5000/nodes/register`  
  ```json
  {
    "nodes": ["http://127.0.0.1:5001"]
  }
  ```

- **Resolve conflicts:**  
  `GET http://localhost:5000/nodes/resolve`

---
- **Images And Gifs:**
<img width="1920" height="1200" alt="newTransaction" src="https://github.com/user-attachments/assets/2a3fea04-bbc3-47a1-9036-765e7a10519c" />





<img width="1920" height="1200" alt="Rename" src="https://github.com/user-attachments/assets/4b34eeee-655a-415e-a417-d9858473cdbd" />





---

This documentation provides an overview of the code and its usage. For more details, refer to the code comments.
