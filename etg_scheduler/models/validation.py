from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ValidationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors
