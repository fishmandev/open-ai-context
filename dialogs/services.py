from openai import OpenAI, APIResponse
from .models import Dialog


def send_request(dialog: Dialog, req: str) -> str:
    client = OpenAI()
    msg = [
        {
            "role": "system",
            "content": dialog.description,
        }
    ]
    for item in dialog.query_set.filter(is_active=True):
        msg.append({"role": "user", "content": item.req})
        msg.append({"role": "assistant", "content": item.res})
    msg.append({"role": "user", "content": req})
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=(msg)
        )
    except Exception as e:
        if e.code == "context_length_exceeded":
            query = dialog.query_set.filter(is_active=True).first()
            query.is_active = False
            query.save()
            return send_request(dialog, req)                   
        
    return completion.choices[0].message.content
