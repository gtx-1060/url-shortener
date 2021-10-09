from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, exception: str):
        self.status_code = status_code
        self.detail = {'exception': exception, 'exception_type': type(self).__name__}
        print(str(self.detail))


class ItemNotFoundException(BaseHTTPException):
    def __init__(self, itype: str):
        super().__init__(404, f"item of type {itype} not found")
