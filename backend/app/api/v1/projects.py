from typing import List

from fastapi import APIRouter, Response, status

from ...schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from ...services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])
service = ProjectService()


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate):
    return service.create_project(payload)


@router.get("", response_model=List[ProjectOut])
def list_projects():
    return service.list_projects()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: str):
    return service.get_project(project_id)


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(project_id: str, payload: ProjectUpdate):
    return service.update_project(project_id, payload)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str):
    service.delete_project(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
