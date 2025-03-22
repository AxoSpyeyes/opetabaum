from typing import List, Optional
from pydantic import BaseModel

class Brukdjin(BaseModel):
    id: Optional[str] = None 
    namai: str
    sjirujena_ko: List[str]
    collection: str = "brukdjin"