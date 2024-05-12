from openai import OpenAI
from .models import Dialog


def send_request(dialog: Dialog, req: str) -> str:
    client = OpenAI()
    msg = [
        {
            "role": "system",
            "content": dialog.description,
        }
    ]
    for item in dialog.query_set.all():
        msg.append({"role": "user", "content": item.req})
        msg.append({"role": "assistant", "content": item.res})
    msg.append({"role": "user", "content": req})
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=(msg))
    return completion.choices[0].message.content
