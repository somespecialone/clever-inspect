from pydantic import BaseModel, HttpUrl


class Case(BaseModel):
    id: int

    name: str
    image: HttpUrl
