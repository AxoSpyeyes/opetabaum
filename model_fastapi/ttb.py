from typing import List, Optional
from pydantic import BaseModel

class Konen (BaseModel):
    ko: str
    konen: List[str]

class Ttb(BaseModel):
    id: Optional[str] = None 
    fras: str
    zunaga: list[Konen]
    collection: str = "ttb"