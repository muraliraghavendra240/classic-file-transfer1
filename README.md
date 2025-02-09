Classic File Transfer

A Python-based client-server system for real-time file transfer with checksum verification. This project demonstrates how to transfer files over a network while ensuring data integrity using SHA256 checksums. It also includes error simulation (packet loss, corruption, and out-of-order delivery) and retransmission logic.

---

## Features

- **File Transfer**: Transfers files from a client to a server over a TCP connection.
- **Chunking**: Splits files into fixed-size chunks (e.g., 1024 bytes) for efficient transmission.
- **Checksum Verification**: Uses SHA256 to verify file integrity after transfer.
- **Error Simulation**:
  - Simulates packet loss by randomly dropping chunks.
  - Simulates packet corruption by modifying chunk data.
  - Simulates out-of-order delivery by shuffling chunks.
- **Retransmission**: Automatically requests missing or corrupted chunks from the server.
- **Unit Tests**: Includes unit tests to validate the functionality.

---

## Requirements

- Python 3.x
- Libraries: `hashlib`, `socket`, `os`, `random`, `unittest`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/classic-file-transfer.git
Navigate to the project directory:


cd classic-file-transfer
Usage
Running the Server
Start the server:
python server/server.py
The server will listen on localhost:12345 for incoming connections.

Running the Client
Run the client and provide the file path:
python client/client.py
When prompted, enter the path to the file you want to transfer (e.g., data.txt).

Example Workflow
The client uploads the file to the server.

The server splits the file into chunks, calculates the checksum, and sends the chunks to the client.

The client reassembles the file, verifies the checksum, and confirms the transfer status.
outputs
![{B4728ED1-9B3B-40B4-9BFA-905F14B5427F}](https://github.com/user-attachments/assets/362dc843-6345-4ff5-b5bd-5764ea63e9b2)
![{182285A7-99AF-49AD-B37D-20D7604F13D3}](https://github.com/user-attachments/assets/470dd91b-cb1b-41bb-8add-7f7d87e046f3)



