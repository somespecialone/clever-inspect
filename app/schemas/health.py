from pydantic import BaseModel


class Health(BaseModel):
    online: int
    total: int
    concurrency: int
