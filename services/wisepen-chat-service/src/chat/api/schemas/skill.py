from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class SkillVersionItem(BaseModel):
    version_id: str
    version_number: int
    version_kind: str
    publish_status: str
    created_at: datetime


class SkillListItem(BaseModel):
    skill_id: str
    display_name: str
    description: str
    icon: Optional[str] = None
    visibility: str = "PUBLIC"
    status: str
    current_active_version_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class SkillDetailItem(SkillListItem):
    versions: List[SkillVersionItem] = []


class SkillListResponse(BaseModel):
    list: List[SkillListItem]
    total: int
    page: int
    size: int
    total_page: int
