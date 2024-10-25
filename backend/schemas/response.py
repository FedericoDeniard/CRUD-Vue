from datetime import datetime

class Response:
    def __init__(self, status: str, status_code: int, data: dict = None, error: dict = None) -> None:
        self.status = status
        self.status_code = status_code
        self.data = data
        self.error = error
    
    def to_dict(self) -> dict:
        response = {
            "status": self.status,
            "status_code": self.status_code,
            "timestamp": datetime.now().timestamp(),
        }
        if self.data is not None:
            response["data"] = self.data
        if self.error is not None:
            response["error"] = self.error
        return response
