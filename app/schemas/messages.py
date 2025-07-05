from pydantic import BaseModel


class ManagerMesssages(BaseModel):
    message : str
    send_number: str
    push_name: str