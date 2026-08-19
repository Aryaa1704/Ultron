from collections.abc import AsyncIterator, Sequence
from dataclasses import dataclass
import logging

from google.api_core import exceptions as google_exceptions
import google.generativeai as genai

from backend.models import Message
from config.settings import get_settings

logger = logging.getLogger(__name__)

ULTRON_SYSTEM_PROMPT = """
You are ULTRON, a production-quality AI assistant platform inspired by JARVIS-style operating systems.
Be helpful, proactive, professional, and context-aware. Explain clearly, adapt to the user's skill level,
and protect the user's safety and privacy. If you are uncertain, say so and suggest a practical next step.
Do not claim to perform actions outside the current system capabilities.
""".strip()


class AIBrainError(Exception):
    """Base controlled AI provider error."""

    status_code = 502
    detail = "AI brain is temporarily unavailable"


class AIBrainConfigurationError(AIBrainError):
    status_code = 503
    detail = "AI brain is not configured"


class AIBrainRateLimitError(AIBrainError):
    status_code = 429
    detail = "AI brain is rate limited; please try again soon"


class AIBrainContextOverflowError(AIBrainError):
    status_code = 400
    detail = "Conversation context is too large; please start a new conversation"


@dataclass(slots=True)
class TokenUsage:
    input_tokens: int | None = None
    output_tokens: int | None = None

    @property
    def total_tokens(self) -> int | None:
        if self.input_tokens is None and self.output_tokens is None:
            return None
        return (self.input_tokens or 0) + (self.output_tokens or 0)

    def as_dict(self) -> dict[str, int | None]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
        }


@dataclass(slots=True)
class BrainResponse:
    content: str
    model: str
    usage: TokenUsage


class ClaudeBrain:
    def __init__(self) -> None:
        settings = get_settings()
        self.model = "gemini-2.0-flash"
        self.max_tokens = settings.anthropic_max_tokens
        self.context_window = settings.chat_context_message_window
        self.timeout = settings.anthropic_timeout_seconds
        self._client = None
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self._client = genai.GenerativeModel(
                model_name=self.model,
                system_instruction=ULTRON_SYSTEM_PROMPT,
                generation_config={"max_output_tokens": self.max_tokens},
            )

    def _ensure_client(self) -> genai.GenerativeModel:
        if self._client is None:
            raise AIBrainConfigurationError()
        return self._client

    def build_messages(self, history: Sequence[Message], latest_user_message: str) -> list[dict[str, str]]:
        recent = list(history)[-self.context_window :]
        messages = [
            {"role": "model" if item.role == "assistant" else item.role, "parts": [item.content]}
            for item in recent
            if item.role in {"user", "assistant"} and item.content
        ]
        messages.append({"role": "user", "parts": [latest_user_message]})
        return messages

    def _extract_usage(self, response) -> TokenUsage:
        usage_metadata = getattr(response, "usage_metadata", None)
        if usage_metadata is None:
            return TokenUsage()
        return TokenUsage(
            input_tokens=getattr(usage_metadata, "prompt_token_count", None),
            output_tokens=getattr(usage_metadata, "candidates_token_count", None),
        )

    async def complete(self, history: Sequence[Message], latest_user_message: str) -> BrainResponse:
        try:
            response = await self._ensure_client().generate_content_async(
                self.build_messages(history, latest_user_message),
                request_options={"timeout": self.timeout},
            )
            text = getattr(response, "text", "").strip()
            if not text:
                raise AIBrainError()
            return BrainResponse(content=text, model=self.model, usage=self._extract_usage(response))
        except google_exceptions.ResourceExhausted as exc:
            logger.warning("Gemini rate limit", exc_info=exc)
            raise AIBrainRateLimitError() from exc
        except google_exceptions.InvalidArgument as exc:
            logger.warning("Gemini context or request error", exc_info=exc)
            raise AIBrainContextOverflowError() from exc
        except (
            google_exceptions.DeadlineExceeded,
            google_exceptions.ServiceUnavailable,
            google_exceptions.GoogleAPIError,
        ) as exc:
            logger.warning("Gemini API error", exc_info=exc)
            raise AIBrainError() from exc

    async def stream(self, history: Sequence[Message], latest_user_message: str) -> AsyncIterator[str]:
        try:
            response = await self._ensure_client().generate_content_async(
                self.build_messages(history, latest_user_message),
                stream=True,
                request_options={"timeout": self.timeout},
            )
            async for chunk in response:
                text = getattr(chunk, "text", "")
                if text:
                    yield text
        except google_exceptions.ResourceExhausted as exc:
            raise AIBrainRateLimitError() from exc
        except google_exceptions.InvalidArgument as exc:
            raise AIBrainContextOverflowError() from exc
        except (
            google_exceptions.DeadlineExceeded,
            google_exceptions.ServiceUnavailable,
            google_exceptions.GoogleAPIError,
        ) as exc:
            raise AIBrainError() from exc


def get_ai_brain() -> ClaudeBrain:
    return ClaudeBrain()
