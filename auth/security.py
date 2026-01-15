from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from jose import jwt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import uuid


# --------------------------
# Password hashing
# --------------------------
def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed)

# --------------------------
# JWT token creation
# --------------------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    to_encode["jti"] = str(uuid.uuid4())  # Add unique JWT ID
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
