"""TideLink — tiny zero-dependency client for the OpenAI-compatible gateway.

TideLink (https://tidelink.app) is an OpenAI-compatible API gateway to China's
best LLMs with automatic failover. If you already use the official `openai`
package, you don't need this file — just set base_url="https://tidelink.app/v1".
This module is for when you want a minimal requests-based client without the
heavier SDK.

The `model` field is treated as compatible but TideLink auto-selects the best
available backend, so any placeholder (e.g. "glm-4-flash") works.
"""

import requests

DEFAULT_BASE = "https://tidelink.app/v1"


class TideLinkError(Exception):
    pass


class TideLink:
    def __init__(self, api_key, base_url=DEFAULT_BASE):
        self.base = base_url.rstrip("/")
        self.api_key = api_key

    def chat(self, messages, model="glm-4-flash", stream=False, timeout=30, **kwargs):
        """Call /v1/chat/completions. Returns parsed JSON, or the raw streaming
        Response object when stream=True (iterate `for line in resp.iter_lines()`)."""
        payload = {"model": model, "messages": messages, "stream": stream, **kwargs}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(
            f"{self.base}/chat/completions",
            headers=headers,
            json=payload,
            stream=stream,
            timeout=timeout,
        )
        if resp.status_code != 200:
            raise TideLinkError(f"{resp.status_code} {resp.text[:300]}")
        if stream:
            return resp
        return resp.json()

    def usage(self):
        """Return your balance / usage snapshot."""
        resp = requests.get(
            f"{self.base}/usage",
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=15,
        )
        if resp.status_code != 200:
            raise TideLinkError(f"{resp.status_code} {resp.text[:300]}")
        return resp.json()


if __name__ == "__main__":
    import os
    key = os.environ.get("TIDELINK_API_KEY", "sk_你的TideLink密钥")
    tl = TideLink(key)
    out = tl.chat([{"role": "user", "content": "用一句话介绍太原"}], model="glm-4-flash")
    print(out["choices"][0]["message"]["content"])
    print("billing:", out.get("_billing"))
