from pydantic import BaseModel
from typing import Optional


class Nouvelle_transaction(BaseModel):
    "Ceci est une nouvelle transaction et on souhaite à savoir si elle est fraduleuse"
    purchase_value: float
    sex: bool
    age: int
    lead_time: float
    source_Ads: bool
    source_Direct: bool
    source_SEO: bool
    browser_Chrome: bool
    browser_FireFox: bool
    browser_IE: bool
    browser_Opera: bool
    browser_Safari: bool
