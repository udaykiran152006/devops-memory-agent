from pydantic import BaseModel
from typing import Optional


class PipelineInput(BaseModel):
    run_id: str
    pipeline: dict
    status: str
    stage: str
    logs: dict


class Analysis(BaseModel):
    failure_type: str
    root_cause: str
    recommendation: str
    confidence: float
