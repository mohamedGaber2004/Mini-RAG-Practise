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

