from src.models.BaseDataModel import BaseDataModel
from src.models.db_schemas import Project
from src.models.enums.DataBaseEnums import DataBaseEnum
from sqlalchemy.future import select
from sqlalchemy import func

class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client=db_client)
        return instance

    async def create_project(self, project: Project):
        async with self.db_client() as session:
            async with session.begin():
                session.add(project)
            await session.commit()
            await session.refresh(project)
        return project

    async def get_project_or_create_one(self, project_id: str):
        async with self.db_client() as session:
            async with session.begin():
                query = select(Project).where(Project.project_id == project_id)
                result = await session.execute(query)
                project_record = result.scalar_one_or_none()
                if project_record is None:
                    project = Project(
                        project_id = project_id
                    )
                    project_record = await self.create_project(project=project)
                    return project_record
                else :
                    return project_record

    async def get_all_projects(self, page: int=1, page_size: int=10):
        async with self.db_client() as session:
            async with session.begin():
                total_documents = await session.execute(select(
                    func.count(Project.project_id)
                )).scalar_one()
                total_pages = total_documents // page_size
                if total_documents % page_size > 0:
                    total_pages+=1

                query = select(Project).offset((page-1)*page_size).limit(page_size)
                projects = await session.execute(query).scalars().all()

                return projects, total_pages