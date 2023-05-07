from passlib.context import CryptContext
import hashlib

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return PASSWORD_CONTEXT.hash(password)


def password_verify(plain_password: str, hashed_password: str):
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def url_shorter(user, url):
    """
    Shorten the given URL using a simple hash function
    """
    hash_user = hashlib.sha256(str(user).encode())
    hash_obj = hashlib.sha256(url.encode())
    return hash_user.hexdigest()[:3] + hash_obj.hexdigest()[:8]
