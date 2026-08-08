from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Memory:
    id: str
    tenant_id: str
    memory_type: str
    content: str
    importance: float
    confidence: float
    created_at: datetime
    source: str
    deleted: bool = False
    expires_at: Optional[datetime] = None