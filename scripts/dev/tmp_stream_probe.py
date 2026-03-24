import json
import time
import urllib.request

payload = {
    "query": "brief answer about patience",
    "top_k": 3,
    "temperature": 0.3,
    "return_sources": True,
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/v1/chat",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST",
)

start = time.time()
try:
    with urllib.request.urlopen(req, timeout=40) as resp:
        print(f"status={resp.status}")
        first_chunk = resp.read(200)
        elapsed = time.time() - start
        print(f"first_chunk_after={elapsed:.2f}s")
        print(first_chunk.decode("utf-8", errors="replace"))
except Exception as exc:
    print(f"ERROR={exc!r}")
