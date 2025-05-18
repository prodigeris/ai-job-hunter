from datetime import datetime, UTC
from pydantic import BaseModel, HttpUrl

class AnalyzedJob(BaseModel):
    job_listing_id: int
    url: HttpUrl
    salary_from: str | None = None
    salary_to: str | None = None
    is_remote_score: float = 0.0  # 0-1 score indicating confidence of remote work
    is_applicable_score: float = 0.0  # 0-1 score indicating if job matches user criteria
    is_european_score: float = 0.0  # 0-1 score indicating if job can be done in Europe
    analyzed_at: datetime = datetime.now(UTC)


