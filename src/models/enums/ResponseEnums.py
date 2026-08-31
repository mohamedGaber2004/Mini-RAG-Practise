from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "Filed Validate Successfully"
    FILE_TYPE_NOT_SUPPORTED = "File Type not supported"
    FILE_SIZE_EXCEEDED = "File Size Exceeded"
    FILE_UPLOAD_SUCEES = "File Uploaded Success"
    FILE_UPLOADED_FAILED = "File Uploaded Failed"
    FILE_ID_ERROR = "No File Found With This ID"
    PROCESSING_FAILED = "Failed Processing"
    PROCESSING_SUCCESS = "Success Processing"
    NO_FILES_ERROR = "Not Found Files"
    PROJECT_NOT_FOUND_ERROR = "Project not found"
    INSERTED_INTO_VECTORDB_ERROR = "Insert into vector db error"
    INSERTED_INTO_VECTORDB_SUCCESS = "Insert into vector db success"
    VECTORDB_COLLECTION_RETRIEVED = "Vector db collection retrieved"
    VECTORDB_SEARCH_ERROR = "Vector db search error"
    VECTORDB_SEARCH_SUCCESS = "Vector db search success"
    RAG_ANSWER_SUCCESS = "RAG Answer Success"
    RAG_ANSWER_ERROR = "RAG Answer Error"
