from typing import List, Optional
from pydantic import BaseModel

class Ko(BaseModel):
    id: Optional[str] = None 
    namai: str
    kofal: str
    kakutro: list[str]
    collection: str = "ko"