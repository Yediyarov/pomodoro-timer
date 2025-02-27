from pydantic import BaseModel, ConfigDict, model_validator


class TaskSchema(BaseModel):
    id: int | None = None
    title: str | None = None
    pomodoro_count: int | None = None
    category_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_name(self):
        if self.title is None:
            raise ValueError("Title is required")
        return self


class TaskCreateSchema(BaseModel):
    title: str | None = None
    pomodoro_count: int | None = None
    category_id: int


class CategorySchema(BaseModel):
    id: int | None = None
    name: str | None = None
    type: str | None = None

    model_config = ConfigDict(from_attributes=True)
