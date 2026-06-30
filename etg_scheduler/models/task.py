from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from etg_scheduler.models.enums import TaskType


class Task(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    task_type: TaskType
    duration: float = Field(gt=0)
    dependencies: list[str] = Field(default_factory=list)
    required_specializations: list[str] = Field(default_factory=list)
    required_resource_count: int = Field(default=1, ge=1)
    base_cost: float = Field(default=0, ge=0)
    description: str | None = None

    @field_validator("id", "name")
    @classmethod
    def text_must_not_be_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be empty")
        return cleaned

    @field_validator("dependencies", "required_specializations")
    @classmethod
    def string_lists_must_not_contain_empty_values(cls, values: list[str]) -> list[str]:
        cleaned = [value.strip() for value in values]
        if any(not value for value in cleaned):
            raise ValueError("list values cannot be empty")
        return cleaned
