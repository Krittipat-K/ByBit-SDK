from dataclasses import dataclass,field
from typing import Any,Optional
import json


from .helper import (
    get_timestamp,
    get_signature
)

from .types import (
    RESTData
)

@dataclass
class HTTPManager:
    api_key: Optional[str] = field(default=None)
    api_secret: Optional[str] = field(default=None)
    recv_window: int = field(default=5000)
    base_url: str = field(default="https://api.bybit.com")
    is_rsa: bool = field(default=False)
    
    def __post_init__(self):
        pass
    
    def prepare_payload(self,method:str, parameters:dict[str,Any])->str:
        def cast_values():
            string_params = [
                "qty",
                "price",
                "triggerPrice",
                "takeProfit",
                "stopLoss",
            ]
            integer_params = ["positionIdx"]
            for key, value in parameters.items():
                if key in string_params:
                    if type(value) != str:
                        parameters[key] = str(value)
                elif key in integer_params:
                    if type(value) != int:
                        parameters[key] = int(value)
        if method == "GET":
            payload = "&".join(
                [
                    str(k) + "=" + str(v)
                    for k, v in sorted(parameters.items())
                    if v is not None
                ]
            )
            return payload
        else:
            cast_values()
            return json.dumps(parameters)
        
    def _auth(self,
              payload:str,
              timestamp:int)->str:
        
        if self.api_key is None or self.api_secret is None:
            raise PermissionError("Authenticated endpoints require keys.")
        
        param_str = str(timestamp) + self.api_key + str(self.recv_window) + payload
        
        return get_signature(self.api_secret,param_str,self.is_rsa)
    
    def prepare_request(self,
                        method:str,
                        endpoint:str,
                        parameters:dict[str,Any],
                        is_auth:bool=False)->RESTData:
        
        for key, value in parameters.items():
            if isinstance(value, float) and value.is_integer():
                parameters[key] = int(value)
                
        payload = self.prepare_payload(method,parameters)
        headers:dict[str,Any] = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        if is_auth:
            # Prepare signature.
            timestamp = get_timestamp()
            signature = self._auth(
                payload=payload,
                timestamp=timestamp,
            )
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-BAPI-API-KEY": self.api_key,
                "X-BAPI-SIGN": signature,
                "X-BAPI-SIGN-TYPE": "2",
                "X-BAPI-TIMESTAMP": str(timestamp),
                "X-BAPI-RECV-WINDOW": str(self.recv_window),
            }
            
        if method == "GET":
            endpoint += "?" + payload
            payload = None
        return RESTData(method=method,url=self.base_url+endpoint,headers=headers,data=payload)