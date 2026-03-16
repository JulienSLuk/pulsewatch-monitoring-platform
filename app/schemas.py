from pydantic import BaseModel

class ServiceCreate(BaseModel):

    name: str
    url: str


class ServiceResponse(BaseModel):

    id: int
    name: str
    url: str
    status: str
    response_time: float | None

    class Config:
        orm_mode = True