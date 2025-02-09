# import unittest
# import os
# import hashlib

# class TestFileTransfer(unittest.TestCase):
#     def test_file_transfer(self):
#         # Test file path
#         file_path = "C:/Users/Murali Raghavendra/OneDrive/Documents/bigendian/data.txt"
#         with open(file_path, "wb") as f:
#             f.write(b"This is a test file for file transfer.")

#         # Simulate client-server interaction
#         # (In a real test, you'd run the server and client in separate threads/processes)
#         server_checksum = hashlib.sha256(open(file_path, "rb").read()).hexdigest()

#         # Simulate client receiving chunks
#         chunks = []
#         with open(file_path, "rb") as f:
#             while chunk := f.read(1024):
#                 chunks.append(chunk)

#         # Simulate reassembly
#         reassembled_file = b"".join(chunks)
#         with open("reassembled_test_file.txt", "wb") as f:
#             f.write(reassembled_file)

#         # Verify checksum
#         client_checksum = hashlib.sha256(reassembled_file).hexdigest()
#         self.assertEqual(server_checksum, client_checksum, "Checksum mismatch.")

#     def tearDown(self):
#         # Clean up test files
#         if os.path.exists("test_file.txt"):
#             os.remove("test_file.txt")
#         if os.path.exists("reassembled_test_file.txt"):
#             os.remove("reassembled_test_file.txt")

# if __name__ == "__main__":
#     unittest.main()

import unittest
import os
import hashlib

class TestFileTransfer(unittest.TestCase):
    def test_file_transfer(self):
        # Test file path
        file_path = "C:/Users/Murali Raghavendra/OneDrive/Documents/bigendian/data.txt"
        with open(file_path, "wb") as f:
            f.write(b"This is a test file for file transfer.")

        # Simulate client-server interaction
        # Calculate server checksum
        with open(file_path, "rb") as f:
            server_checksum = hashlib.sha256(f.read()).hexdigest()

        # Simulate client receiving chunks
        chunks = []
        with open(file_path, "rb") as f:
            while chunk := f.read(1024):
                chunks.append(chunk)

        # Simulate reassembly
        reassembled_file = b"".join(chunks)
        with open("reassembled_test_file.txt", "wb") as f:
            f.write(reassembled_file)

        # Verify checksum
        with open("reassembled_test_file.txt", "rb") as f:
            client_checksum = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(server_checksum, client_checksum, "Checksum mismatch.")

    def tearDown(self):
        # Clean up test files
        if os.path.exists("test_file.txt"):
            os.remove("test_file.txt")
        if os.path.exists("reassembled_test_file.txt"):
            os.remove("reassembled_test_file.txt")

if __name__ == "__main__":
    unittest.main()