from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

import task_7.const

# for creating resource
class ResourceRequest(BaseModel):
    name: str
    on_bench: bool = False

# for sending resource
class ResourceResponse(BaseModel):
    id: int
    name: str
    on_bench: bool

# for resource link Response
class ProjectResourceLinkResponse(BaseModel):
    # project_id: int
    resource_id: int
    on_board: datetime
    off_board: Optional[datetime] = None

class ProjectRequest(BaseModel):
    title: str
    start_at: Optional[datetime]
    project_manager: ProjectResourceLinkResponse
    resources: List[ProjectResourceLinkResponse] = []
    end_at: Optional[datetime] = None
    soft_deadline: Optional[datetime] = None
    hard_deadline: Optional[datetime] = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    start_at: datetime
    end_at: Optional[datetime]
    project_manager_id: int
    # project_manager: ProjectResourceLinkResponse
    status: task_7.const.ProjectStatus
    resources: List[ProjectResourceLinkResponse]
    end_at: Optional[datetime]
    soft_deadline: Optional[datetime]
    hard_deadline: Optional[datetime]

class ListResourceResponse(BaseModel):
    count: int
    resources: List[ResourceResponse]

class ListProjectResponse(BaseModel):
    count: int
    projects: List[ProjectRequest]

class ListOfResources(BaseModel):
    resources: List[int]