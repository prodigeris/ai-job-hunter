from pydantic import BaseModel, HttpUrl
from datetime import datetime, UTC
from hashlib import md5

class JobListing(BaseModel):
    id: int | None = None
    url: HttpUrl
    content: str
    _checksum: str = ""
    published_at: datetime = datetime.now(UTC)
    created_at: datetime = datetime.now(UTC)
    salary_min: float | None = None
    salary_max: float | None = None
    location: str | None = None
    title: str | None = None

    @property
    def checksum(self) -> str:
        if self._checksum:  # use stored checksum if exists
            return self._checksum
        if self.content:
            return md5(self.content.encode("utf-8")).hexdigest()
        return ""  # fallback, though ideally content should never be missing
