from typing import (
    NamedTuple,
    Any,
    Optional
)

class RESTData(NamedTuple):
    method:str
    url:str
    headers:dict[str,Any]
    data:Optional[str]=None