# Migrate to TideLink

TideLink is OpenAI-compatible. In almost every tool, migration is **one line**: change the base URL and the API key.

## OpenAI Python SDK

```python
# before
from openai import OpenAI
client = OpenAI(api_key="sk-openai-...")

# after
from openai import OpenAI
client = OpenAI(
    base_url="https://tidelink.xyz/v1",
    api_key="sk_你的TideLink密钥",   # free at https://tidelink.xyz/dashboard.html
)
```

## OpenAI Node SDK

```js
// before
const client = new OpenAI({ apiKey: 'sk-openai-...' });
// after
const client = new OpenAI({ baseURL: 'https://tidelink.xyz/v1', apiKey: 'sk_你的TideLink密钥' });
```

## Cursor

Settings → Models → set **OpenAI Base URL** to `https://tidelink.xyz/v1` and **OpenAI API Key** to your TideLink key.

## Claude Code / Codex

```bash
export OPENAI_API_KEY="sk_你的TideLink密钥"
export OPENAI_BASE_URL="https://tidelink.xyz/v1"
claude      # or: codex
```

## Cline (VS Code)

API Provider → **OpenAI Compatible** · Base URL → `https://tidelink.xyz/v1` · API Key → your TideLink key · Model ID → `glm-4-flash`.

## Continue

```json
{
  "models": [{ "title": "TideLink", "provider": "openai", "model": "glm-4-flash",
               "apiBase": "https://tidelink.xyz/v1", "apiKey": "sk_你的TideLink密钥" }]
}
```

## Chatbox

Settings → Model Provider → **OpenAI** · API Host → `https://tidelink.xyz/v1` · API Key → your TideLink key · Model → `glm-4-flash`.

## Dify

Model Provider → Add → **OpenAI-API-compatible** · Base URL → `https://tidelink.xyz/v1` · API Key → your TideLink key · Model → `glm-4-flash`.

## About the `model` field

TideLink auto-selects the best available model and fails over across providers, so the `model` value sent by a client is treated as compatible but not used for routing. If a tool requires a "real-looking" model name to send a request, use `glm-4-flash` (or any placeholder such as `gpt-4o-mini`); TideLink picks the optimal backend regardless.

Full integrations guide: https://tidelink.xyz/docs/integrations.html
