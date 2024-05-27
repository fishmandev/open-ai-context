from openai import OpenAI
from .models import Dialog
from django.db.models import Sum
from django.db.models import F, Window
import tiktoken

MODEL_NAME = "gpt-3.5-turbo"
MAX_TOKENS_IN_RESPONSE = 1024
TOTAL_TOKENS_AVAILABLE = 16384
RESERVE_TOKENS = 512


def __get_tokens_count(string: str, model: str) -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(string))


def __get_available_tokens() -> int:
    return TOTAL_TOKENS_AVAILABLE - MAX_TOKENS_IN_RESPONSE - RESERVE_TOKENS


def send_request(dialog: Dialog, req: str) -> str:
    client = OpenAI()
    msg = [
        {
            "role": "system",
            "content": dialog.description,
        }
    ]
    total_tokens = 0
    content = [{"role": "user", "content": req}]
    for item in dialog.query_set.annotate(
        tokens=Window(Sum("total_tokens"), order_by=F("id").desc())
    ).filter(
        tokens__lte=__get_available_tokens() - __get_tokens_count(req, MODEL_NAME)
    ):
        total_tokens += item.total_tokens
        content.append({"role": "assistant", "content": item.res})
        content.append({"role": "user", "content": item.req})
    msg += list(reversed(content))

    completion = client.chat.completions.create(
        model=MODEL_NAME, messages=(msg), max_tokens=MAX_TOKENS_IN_RESPONSE
    )

    return (
        completion.usage.total_tokens - total_tokens,
        completion.choices[0].message.content,
    )
