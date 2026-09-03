"""
TideLink — tiny zero-dependency client for the TideLink OpenAI-compatible
LLM gateway. One endpoint for China's best LLMs (GLM, Qwen, DeepSeek,
Hunyuan, Doubao) with automatic failover handled on the gateway side.

Quick start:
    export TIDELINK_API_KEY=YOUR_KEY   # free key: https://tidelink.xyz/dashboard.html?cid=gh
    from tidelink import TideLink
    tl = TideLink()
    r = tl.chat([{"role": "user", "content": "Hi!"}], model="glm-4-flash")
    print(r["choices"][0]["message"]["content"])
"""
import os
import requests

DEFAULT_BASE_URL = "https://tidelink.xyz/v1"
FREE_KEY_URL = "https://tidelink.xyz/dashboard.html?cid=gh"


class TideLinkError(Exception):
    """Raised when the TideLink API returns an error."""


class TideLink:
    def __init__(self, api_key=None, base_url=DEFAULT_BASE_URL, timeout=60):
        self.api_key = api_key or os.environ.get("TIDELINK_API_KEY")
        if not self.api_key:
            raise ValueError(
                "TideLink api_key is required. Pass it explicitly or set the "
                "TIDELINK_API_KEY environment variable. Get a free key at "
                + FREE_KEY_URL
            )
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def chat(self, messages, model="glm-4-flash", temperature=0.7,
             max_tokens=None, stream=False, **kwargs):
        """Send a chat completion request.

        Returns the full OpenAI-format dict. With ``stream=True`` returns a
        generator that yields raw SSE payload strings (after the ``data:`` prefix).
        Failover between providers is handled by the gateway, not the client.
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
            **kwargs,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        url = f"{self.base_url}/chat/completions"
        if stream:
            return self._stream(url, payload)

        resp = requests.post(url, json=payload, headers=self._headers(),
                             timeout=self.timeout)
        if resp.status_code >= 400:
            raise TideLinkError(f"{resp.status_code}: {resp.text}")
        return resp.json()

    def _stream(self, url, payload):
        resp = requests.post(url, json=payload, headers=self._headers(),
                             timeout=self.timeout, stream=True)
        if resp.status_code >= 400:
            raise TideLinkError(f"{resp.status_code}: {resp.text}")
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            if line.startswith("data:"):
                yield line[len("data:"):].strip()

    def models(self):
        """List available models (passes through the gateway's /v1/models)."""
        resp = requests.get(f"{self.base_url}/models", headers=self._headers(),
                            timeout=self.timeout)
        if resp.status_code >= 400:
            raise TideLinkError(f"{resp.status_code}: {resp.text}")
        return resp.json()
