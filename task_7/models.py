from datetime import datetime
from typing import List, Optional, Literal

from sqlalchemy import func, ForeignKey, Column, false, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, Relationship

from task_7.db import Base
from task_7.const import ProjectStatus

class Project(Base):
    __tablename__ = "project"

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    project_manager_id: Mapped[int] = mapped_column(ForeignKey("resource.id"), nullable=False)
    start_at: Mapped[datetime]
    end_at: Mapped[datetime | None]
    status: Mapped[ProjectStatus] = mapped_column(server_default=Enum(ProjectStatus).enums[0])
    hard_deadline: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    soft_deadline: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None]

    # Relationships
    resources: Mapped[List["ProjectResourceLink"]] = relationship(back_populates="project", lazy="joined")

    # project_manager: Mapped["ResourceLink"] = relationship("ResourceLink", lazy='joined')
    # resources: Mapped[List["ResourceLink"]] = relationship("ResourceLink", secondary="project_resource_association", back_populates="project_data", lazy='joined')

    def __repr__(self) -> str:
        return f"Project(id={self.id})"

class Resource(Base):
    __tablename__ = "resource"

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    on_bench: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None]

    # Relationships
    projects: Mapped[List["ProjectResourceLink"]] = relationship(back_populates="resource", lazy="joined")

    # projects: Mapped[List["Project"]] = relationship("Project", secondary="project_resource_association", lazy='joined')

    def __repr__(self) -> str:
        return f"Resource(id={self.id})"

class ProjectResourceLink(Base):
    __tablename__ = "project_resource_association"

    # Columns
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), primary_key=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resource.id"), primary_key=True)
    on_board: Mapped[datetime]
    off_board: Mapped[datetime | None]

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="resources", lazy='joined')
    resource: Mapped["Resource"] = relationship(back_populates="projects", lazy='joined')