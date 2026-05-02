from datetime import datetime, timezone
from typing import Dict, List
from uuid import uuid4

from fastapi import HTTPException, status

from ..schemas.project import ProjectCreate, ProjectUpdate
from ..storage import store


class ProjectService:
    def list_projects(self) -> List[Dict]:
        return sorted(store.all("projects"), key=lambda item: item["updated_at"], reverse=True)

    def create_project(self, payload: ProjectCreate) -> Dict:
        now = _now()
        project = {
            "id": str(uuid4()),
            "name": payload.name,
            "description": payload.description,
            "tech_stack": payload.tech_stack,
            "status": payload.status,
            "created_at": now,
            "updated_at": now,
        }
        return store.insert("projects", project)

    def get_project(self, project_id: str) -> Dict:
        project = store.get("projects", project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    def update_project(self, project_id: str, payload: ProjectUpdate) -> Dict:
        project = self.get_project(project_id)
        updates = payload.dict(exclude_unset=True)
        project.update(updates)
        project["updated_at"] = _now()
        return store.replace("projects", project_id, project) or project

    def delete_project(self, project_id: str) -> None:
        self.get_project(project_id)
        store.delete("projects", project_id)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
