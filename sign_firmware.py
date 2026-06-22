from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

with open("firmware.bin", "rb") as f:
    firmware = f.read()

signature = private_key.sign(
    firmware,
    padding.PKCS1v15(),
    hashes.SHA256()
)

with open("firmware.sig", "wb") as f:
    f.write(signature)

print("Firmware signed successfully.")