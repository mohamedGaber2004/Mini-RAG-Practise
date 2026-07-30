from src.controllers import BaseController
from src.controllers import ProjectController
from src.models import ProceesingEnums
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os 


class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    # return file extension such as ".txt" or ".pdf"
    def get_file_extenstion(self, file_id: str):
        return os.path.splitext(file_id)[-1]

    # return file loader for .txt files or .pdf files
    def get_file_loader(self,file_id: str):
        file_ext = self.get_file_extenstion(file_id=file_id)
        file_path = os.path.join(
            self.project_path,
            file_id
        )

        if file_ext == ProceesingEnums.TXT.value : 
            return TextLoader(file_path, encoding="utf-8")

        if file_ext == ProceesingEnums.PDF.value : 
            return PyMuPDFLoader(file_path)

        return None
    
    # return file content in type of Document (langchain)
    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id=file_id)
        return loader.load()

    # return chunks of the document
    def process_file_content(self, file_content: list, file_id: str, chunk_size: int=100, overlap_size: int=20):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        file_content_text = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata 
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_text,
            metadatas=file_content_metadata
        )

        return chunks