import hashlib
from enum import Enum


class SigningAlgorithm(str, Enum):
    HS256 = "HS256"
    HS384 = "HS384"

    def get_hash_function(self):
        hash_map = {
            SigningAlgorithm.HS256: hashlib.sha256,
            SigningAlgorithm.HS384: hashlib.sha384,
        }
        return hash_map[self]
