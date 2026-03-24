import json
import urllib.error
import urllib.request

payload = {
    "query": "What is purpose of life?",
    "top_k": 4,
    "temperature": 0.3,
    "return_sources": True,
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/v1/chat/sync",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=25) as resp:
        body = resp.read().decode("utf-8")
        print(f"status={resp.status}")
        print(body[:2000])
except urllib.error.HTTPError as exc:
    print(f"HTTP_ERROR status={exc.code}")
    try:
        print(exc.read().decode("utf-8")[:2000])
    except Exception:
        print(repr(exc))
except Exception as exc:
    print(f"ERROR={exc!r}")
