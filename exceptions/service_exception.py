from typing import Dict, List
from http import HTTPStatus


class ServiceException(Exception):

    def __init__(self, message: str, status: HTTPStatus, errors: Dict[str, List[str]] = None):
        super().__init__(message)
        self.status = status
        self.errors = errors

    def get_message(self) -> str:
        return str(self)

    def get_status(self) -> HTTPStatus:
        return self.status

    def get_errors(self) -> Dict[str, List[str]]:
        return self.errors
