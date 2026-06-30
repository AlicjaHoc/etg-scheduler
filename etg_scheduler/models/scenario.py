from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from etg_scheduler.models.enums import OptimizationMode
from etg_scheduler.models.resource import Resource
from etg_scheduler.models.task import Task


class Scenario(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
    tasks: list[Task] = Field(min_length=1)
    resources: list[Resource] = Field(min_length=1)
    default_optimization_mode: OptimizationMode = OptimizationMode.BALANCED

    @field_validator("name", "description")
    @classmethod
    def text_must_not_be_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be empty")
        return cleaned
