"""Example: streaming chat with TideLink + parsing SSE lines."""
import os
from tidelink import TideLink


def main():
    key = os.environ.get("TIDELINK_API_KEY", "sk_你的TideLink密钥")
    tl = TideLink(key)
    resp = tl.chat(
        [{"role": "user", "content": "数到 5，每个数一行"}],
        model="glm-4-flash",
        stream=True,
    )
    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue
        if line.startswith("data:"):
            data = line[len("data:"):].strip()
            if data == "[DONE]":
                break
            try:
                import json
                chunk = json.loads(data)
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    print(delta, end="", flush=True)
            except Exception:
                pass
    print()


if __name__ == "__main__":
    main()
