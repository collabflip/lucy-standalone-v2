import json
import urllib.request

URL = "http://127.0.0.1:8767/v1/chat/completions"

def chat(prompt: str) -> str:
    body = {
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read().decode())

    return data["choices"][0]["message"]["content"]
