from pydantic import BaseModel, ConfigDict


class comment_interface(BaseModel):
    comment_str: str


class comment_opt(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
    )
    id: int
    user_id: int
    good_id: int
    comment_str: str
