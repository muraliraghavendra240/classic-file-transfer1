import socket
import hashlib
import os

CHUNK_SIZE = 1024  # Fixed chunk size

def calculate_checksum(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

def start_client(file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 12345))

    # Send file name and size
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    client_socket.send(file_name.encode())
    client_socket.send(str(file_size).encode())

    # Send file data
    with open(file_path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            client_socket.send(chunk)
    print("File sent to server.")

    # Receive checksum and chunks
    checksum = client_socket.recv(1024).decode()
    print(f"Received checksum: {checksum}")

    chunks = {}
    while True:
        data = client_socket.recv(CHUNK_SIZE + 10)  # Extra bytes for sequence number
        if not data:
            break
        seq_num = int(data.split(b":")[0].decode())
        chunk_data = data.split(b":")[1]
        chunks[seq_num] = chunk_data
    print(f"Received {len(chunks)} chunks.")

    # Check for missing or corrupted chunks
    missing_chunks = set(range(len(chunks))) - set(chunks.keys())
    corrupted_chunks = [seq_num for seq_num, chunk in chunks.items() if chunk == b"corrupted_data"]

    if missing_chunks or corrupted_chunks:
        print(f"Missing chunks: {missing_chunks}")
        print(f"Corrupted chunks: {corrupted_chunks}")
        print("Requesting retransmission...")

        # Request retransmission of missing/corrupted chunks
        client_socket.send("retransmit".encode())
        client_socket.send(str(list(missing_chunks) + corrupted_chunks).encode())

        # Receive retransmitted chunks
        while True:
            data = client_socket.recv(CHUNK_SIZE + 10)
            if not data:
                break
            seq_num = int(data.split(b":")[0].decode())
            chunk_data = data.split(b":")[1]
            chunks[seq_num] = chunk_data
        print("Retransmission complete.")

    # Reassemble file
    reassembled_file = b""
    for i in range(len(chunks)):
        reassembled_file += chunks[i]
    with open(f"reassembled_{file_name}", "wb") as f:
        f.write(reassembled_file)
    print("File reassembled.")

    # Verify checksum
    new_checksum = calculate_checksum(f"reassembled_{file_name}")
    if new_checksum == checksum:
        print("Checksum verified. Transfer successful!")
    else:
        print("Checksum mismatch. Transfer failed.")

    client_socket.close()

if __name__ == "__main__":
    file_path = input("Enter file path: ")
    start_client(file_path)