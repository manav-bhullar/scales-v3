"""Configuration loader — YAML settings + environment variables."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# scales_v3/ project root (parent of the `scales` package)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SETTINGS_PATH = PROJECT_ROOT / "config" / "settings.yaml"


class LLMConfig(BaseModel):
    cera_model: str = "gemini/gemini-2.0-flash"
    cgr_model: str = "gemini/gemini-2.0-flash"
    stability_model: str = "gemini/gemini-2.0-flash"
    temperature: float = 0.1
    max_retries: int = 3
    retry_delay_seconds: float = 2.0
    max_concurrent_calls: int = 10


class NLIConfig(BaseModel):
    model_name: str = "cross-encoder/nli-deberta-v3-base"
    device: str = "cpu"
    batch_size: int = 32


class CBTETier3Weights(BaseModel):
    nli: float = 0.4
    stability: float = 0.3
    keyword: float = 0.3


class CBTEConfig(BaseModel):
    tier1_keyword_threshold: float = 0.3
    tier2_nli_threshold: float = 0.7
    tier3_weights: CBTETier3Weights = Field(default_factory=CBTETier3Weights)
    tau: float = 0.5
    tau_source: str = "manual"
    enable_tier3: bool = False


class ConformalConfig(BaseModel):
    alpha: float = 0.10
    calibration_data_path: str = "data/calibration/"
    auto_adjust: bool = True


class GradingConfig(BaseModel):
    allowed_marks_fractions: list[float] = Field(default_factory=lambda: [0.0, 0.5, 1.0])


class PathsConfig(BaseModel):
    database: str = "data/scales.db"
    data_dir: str = "data/"
    exams_dir: str = "data/exams/"
    prompts_dir: str = "config/prompts/"
    logs_dir: str = "logs/"


class LoggingConfig(BaseModel):
    level: str = "INFO"
    log_llm_responses: bool = True
    log_nli_scores: bool = True


class AppSettings(BaseModel):
    """Typed view of config/settings.yaml."""

    llm: LLMConfig = Field(default_factory=LLMConfig)
    nli: NLIConfig = Field(default_factory=NLIConfig)
    cbte: CBTEConfig = Field(default_factory=CBTEConfig)
    conformal: ConformalConfig = Field(default_factory=ConformalConfig)
    grading: GradingConfig = Field(default_factory=GradingConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


class EnvSecrets(BaseSettings):
    """API keys and secrets from .env / environment."""

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Single key (backward compatible) + optional pool for Gemini rate-limit rotation
    google_api_key: str | None = None
    google_api_keys: str | None = None  # comma-separated
    google_api_key_1: str | None = None
    google_api_key_2: str | None = None
    google_api_key_3: str | None = None
    google_api_key_4: str | None = None
    google_api_key_5: str | None = None

    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    groq_api_key: str | None = None
    # LiteLLM expects OPENROUTER_API_KEY; also accept open_router_api_key from .env
    openrouter_api_key: str | None = None
    open_router_api_key: str | None = None
    # LiteLLM: CEREBRAS_API_KEY + model prefix cerebras/...
    cerebras_api_key: str | None = None
    # LiteLLM / OpenAI-compatible shim for z.ai GLM (https://z.ai/manage-apikey/apikey-list)
    zai_api_key: str | None = None
    z_ai_api_key: str | None = None  # alias
    # Optional override; default https://api.z.ai/api/paas/v4
    # Coding Plan keys often need https://api.z.ai/api/coding/paas/v4
    zai_api_base: str | None = None
    # LiteLLM: MISTRAL_API_KEY + model prefix mistral/...
    mistral_api_key: str | None = None

    def gemini_api_keys(self) -> list[str]:
        """Ordered unique Gemini / Google AI Studio keys for rotation."""
        found: list[str] = []
        seen: set[str] = set()

        def add(raw: str | None) -> None:
            if not raw:
                return
            for part in raw.replace(";", ",").split(","):
                key = part.strip()
                if key and key not in seen and "your-google" not in key.lower():
                    seen.add(key)
                    found.append(key)

        add(self.google_api_key)
        add(self.google_api_keys)
        add(self.google_api_key_1)
        add(self.google_api_key_2)
        add(self.google_api_key_3)
        add(self.google_api_key_4)
        add(self.google_api_key_5)
        return found


def load_yaml_settings(path: Path | None = None) -> dict[str, Any]:
    settings_path = path or DEFAULT_SETTINGS_PATH
    if not settings_path.exists():
        raise FileNotFoundError(f"Settings file not found: {settings_path}")
    with settings_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Settings file must be a mapping: {settings_path}")
    return data


@lru_cache(maxsize=1)
def get_settings(settings_path: str | None = None) -> AppSettings:
    """Load and cache application settings."""
    path = Path(settings_path) if settings_path else DEFAULT_SETTINGS_PATH
    raw = load_yaml_settings(path)
    return AppSettings.model_validate(raw)


def get_secrets() -> EnvSecrets:
    return EnvSecrets()


def resolve_path(relative: str) -> Path:
    """Resolve a path from settings relative to the project root."""
    candidate = Path(relative)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate


def prompt_path(filename: str) -> Path:
    settings = get_settings()
    return resolve_path(settings.paths.prompts_dir) / filename
