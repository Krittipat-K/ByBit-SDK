import time
import hmac
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

def get_timestamp()->int:
    return int(time.time() * 1000)  

def get_signature(api_secret:str,params:str,is_rsa:bool=False)->str:
    def generate_hmac()->str:
        return str(hmac.new(
            api_secret.encode("utf-8"),
            params.encode("utf-8"),
            "sha256"
        ).hexdigest()
        )

    def generate_rsa()->str:
        hash = SHA256.new(params.encode("utf-8")) # type: ignore
        encoded_signature = base64.b64encode(
            PKCS1_v1_5.new(RSA.importKey(api_secret)).sign( # type: ignore
                hash
            ) 
        ) 
        return encoded_signature.decode()
    
    return generate_rsa() if is_rsa else generate_hmac()
