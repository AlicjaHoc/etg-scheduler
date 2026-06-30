from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from etg_scheduler.models.enums import ResourceType


class Resource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    resource_type: ResourceType
    specialization: str | None = None
    cost_per_time_unit: float = Field(ge=0)
    speed_multiplier: float = Field(gt=0)

    @field_validator("id", "name")
    @classmethod
    def text_must_not_be_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be empty")
        return cleaned

    @field_validator("specialization")
    @classmethod
    def specialization_must_not_be_empty(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("specialization cannot be empty")
        return cleaned

    @model_validator(mode="after")
    def specialization_must_match_resource_type(self) -> "Resource":
        if self.resource_type == ResourceType.SPECIALIZED and not self.specialization:
            raise ValueError("specialized resources must define specialization")
        if self.resource_type == ResourceType.UNIVERSAL and self.specialization:
            raise ValueError("universal resources cannot define specialization")
        return self
