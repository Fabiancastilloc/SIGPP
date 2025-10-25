from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "password123"
hashed = pwd_context.hash(password)

print(f"Contraseña: {password}")
print(f"Hash: {hashed}")
print(f"Longitud del hash: {len(hashed)}")