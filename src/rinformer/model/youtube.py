from dataclasses import dataclass

from .service import Service, register_service

@register_service
@dataclass(frozen=True, kw_only=True, slots=True)
class YouTube(Service):
    google_api_key: str | None
    air_quality_api_key: str | None


    def query(self) -> dict[str, str]: pass