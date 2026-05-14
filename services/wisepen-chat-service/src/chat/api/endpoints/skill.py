from fastapi import APIRouter, Query, HTTPException

from chat.domain.entities.skill import Skill
from chat.api.schemas.skill import (
    SkillListItem,
    SkillDetailItem,
    SkillVersionItem,
    SkillListResponse,
)
from common.core.domain import R, PageResult

router = APIRouter()


def _doc_to_item(doc: Skill) -> SkillListItem:
    return SkillListItem(
        skill_id=doc.skill_id,
        display_name=doc.display_name,
        description=doc.description,
        status="ACTIVE" if doc.enabled else "INACTIVE",
        current_active_version_id=doc.version or None,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
    )


def _doc_to_detail(doc: Skill) -> SkillDetailItem:
    version = SkillVersionItem(
        version_id=doc.version,
        version_number=1,
        version_kind="RELEASE",
        publish_status="PUBLISHED",
        created_at=doc.created_at,
    )
    return SkillDetailItem(
        skill_id=doc.skill_id,
        display_name=doc.display_name,
        description=doc.description,
        status="ACTIVE" if doc.enabled else "INACTIVE",
        current_active_version_id=doc.version or None,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        versions=[version],
    )


@router.get("/listSkills", response_model=R[SkillListResponse])
async def list_skills():
    docs = await Skill.find(Skill.enabled == True).to_list()
    items = [_doc_to_item(d) for d in docs]
    total = len(items)
    size = max(total, 1)
    return R.success(data=SkillListResponse(
        list=items,
        total=total,
        page=1,
        size=size,
        total_page=1,
    ))


@router.get("/getSkillDetail", response_model=R[SkillDetailItem])
async def get_skill_detail(skill_id: str = Query(..., description="Skill 唯一标识")):
    doc = await Skill.find_one(Skill.skill_id == skill_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")
    return R.success(data=_doc_to_detail(doc))
