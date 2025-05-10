from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

import task_7.const

from task_7.db import get_async_db_session
from task_7.models import *
from task_7.schemas import *

router = APIRouter()

@router.get("/resource", response_model=ListResourceResponse, status_code=status.HTTP_200_OK)
async def get_all_resources(
        db: Annotated[AsyncSession, Depends(get_async_db_session)],
        on_bench: bool = None
):
    count_stmt = select(
        func.count(Resource.id)
    ).where(Resource.deleted_at.is_(None))

    stmt = select(
        Resource.id,
        Resource.name,
        Resource.on_bench,
        Resource.created_at,
        Resource.updated_at
    ).where(Resource.deleted_at.is_(None))

    if on_bench is not None:
        count_stmt = count_stmt.where(Resource.on_bench == on_bench)
        stmt = stmt.where(Resource.on_bench == on_bench)

    result_count = (await db.execute(count_stmt)).scalar() or 0

    result_rows = (await db.execute(stmt)).all()

    return ListResourceResponse(
        count=result_count,
        resources=[
            ResourceResponse(
                id=row.id,
                name=row.name,
                on_bench=row.on_bench,
            )
            for row in result_rows
        ]
    )

@router.post("/resource", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    request_data: ResourceRequest,
):
    resource = Resource(**request_data.model_dump())
    db.add(resource)
    await db.commit()
    await db.refresh(resource)

    return resource


@router.delete("/resource/{resource_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_resource(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    resource_id
):
    delete_stmt = (update(Resource).where(Resource.id == int(resource_id),
                                         Resource.on_bench == True,
                                         Resource.deleted_at.is_(None))
                   .values(deleted_at=func.now()))

    resource = (await db.execute(delete_stmt))

    if resource is None:
        raise HTTPException(status_code=404, detail="resource cannot be delete!")

    await db.commit()
    await db.refresh(resource)
    return {"deleted": resource}


@router.post("/project/{project_id}/allocate_resource")
async def allocate_resources(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    project_id: int,
    request_data: ListOfResources
):
    stmt = select(Project).where(Project.id == project_id,
                                 Project.deleted_at.is_(None),
                                 Project.status != ProjectStatus.COMPLETED)
    project = (await  db.execute(stmt)).scalar_one_or_none()

    if project is None:
        raise HTTPException(status_code=404, detail="Cannot add resources to specified project!")

    for resource_id in request_data.resources:
        association = ProjectResourceLink(project_id=project_id, resource_id=resource_id, on_board=func.now())
        stmt = update(Resource).where(Resource.id == resource_id).values(on_bench=False)
        await db.execute(stmt)
        db.add(association)

    await db.commit()
    await db.refresh(project)

    return {
        "message": "resources are allocated successfully to the project",
        "project": project
    }


@router.put("project/{project_id}/completed")
async def deallocate_resources(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    project_id: int
):
    complete_stmt = (update(Project)
                     .where(Project.id == project_id, Project.status == ProjectStatus.ON_GOING)
                     .values(status=ProjectStatus.COMPLETED))
    updated_project = await db.execute(complete_stmt)

    if updated_project.rowcount == 0:
        raise HTTPException(status_code=400, detail="Project is already completed/not started or does not exist!")

    update_stmt = (
        update(ProjectResourceLink)
        .where(ProjectResourceLink.project_id == project_id)
        .values(off_board=func.now())
    )
    await db.execute(update_stmt)
    await db.commit()

    stmt = (
            select(ProjectResourceLink.resource_id)
            .where(ProjectResourceLink.project_id == project_id)
    )

    associated_resources = (await db.execute(stmt)).scalars().unique()

    if associated_resources:
        update_on_bench_stmt = (update(Resource)
                                .where(Resource.id.in_(associated_resources),
                                       ~Resource.projects.any(ProjectResourceLink.off_board.is_(None))
                                       )).values(on_bench=True)
        await db.execute(update_on_bench_stmt)

    await db.commit()

    stmt = (
        select(Project)
        .options(joinedload(Project.resources))
        .where(Project.id == project_id)
    )
    updated_project_data = (await db.execute(stmt)).scalar()

    return {
        "message": "Project is marked as completed",
        "project": {
            "id": updated_project_data.id,
            "title": updated_project_data.title,
            "status": updated_project_data.status,
            "resources": [
                {"resource_id": res.resource_id, "off_board": res.off_board}
                for res in updated_project_data.resources
            ],
        }
    }


@router.get("/resource")


@router.get("/project", response_model=dict, status_code=status.HTTP_200_OK)
async def get_all_projects(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
):
    count_stmt = select(
        func.count(Project.id)
    ).where(Project.deleted_at.is_(None))

    result_count = (await db.execute(count_stmt)).scalar() or 0

    stmt = (
        select(Project)
        .options(joinedload(Project.resources).joinedload(ProjectResourceLink.resource))
        .where(Project.deleted_at.is_(None))
    )


    result_rows = (await db.execute(stmt)).scalars().unique()
    return {"count": result_count,
            "projects": [
        ProjectResponse(id=res.id,
                        title=res.title,
                        start_at=res.start_at,
                        end_at=res.end_at,
                        status=res.status,
                        project_manager_id=res.project_manager_id,
                        hard_deadline=res.hard_deadline,
                        soft_deadline=res.soft_deadline,
                        resources= [ ProjectResourceLinkResponse(
                            resource_id=r.resource_id,
                            on_board=r.on_board,
                            off_board=r.off_board)
                            for r in res.resources
                        ]
                        )
        for res in result_rows
    ]}

@router.post("/project", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
        db: Annotated[AsyncSession, Depends(get_async_db_session)],
        request_data: ProjectRequest
):
    project = Project(
        title=request_data.title,
        start_at=request_data.start_at,
        # end_at=request_data.end_at,
        # resources=[ res.resource_id for res in request_data.resources ],
        project_manager_id=request_data.project_manager.resource_id,
        soft_deadline=request_data.soft_deadline,
        hard_deadline=request_data.hard_deadline,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)

    for resource in request_data.resources:
        association = (
            ProjectResourceLink(project_id=project.id,
                                          resource_id=resource.resource_id,
                                          on_board=resource.on_board
                                          ))
        db.add(association)
    association = (
        ProjectResourceLink(project_id=project.id,
                                      resource_id=request_data.project_manager.resource_id,
                                      on_board=request_data.project_manager.on_board
                                      ))
    db.add(association)

    await db.commit()
    await db.refresh(project)

    return project