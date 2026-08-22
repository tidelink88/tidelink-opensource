# TideLink SDK & Drop-in Helper

Official developer toolkit for [TideLink](https://tidelink.app) — an **OpenAI-compatible API gateway** to China's best LLMs (GLM, Qwen, DeepSeek, Hunyuan, Doubao) with automatic failover.

> One endpoint. Every model. No vendor lock-in.

TideLink speaks the OpenAI protocol, so in most cases you don't need this SDK at all — just point your existing OpenAI client at `https://tidelink.app/v1`. This repo exists for three reasons:
1. A tiny zero-dependency client when you don't want to pull in the `openai` package.
2. Copy-paste **migration snippets** from OpenAI / other gateways.
3. A reference the community can extend (PRs welcome).

## Install

```bash
pip install requests        # python, only if not using the openai SDK
npm install                 # node
```

## 30-second start (OpenAI SDK — recommended)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://tidelink.app/v1",
    api_key="sk_你的TideLink密钥",   # get one free at https://tidelink.app/dashboard.html
)

resp = client.chat.completions.create(
    model="glm-4-flash",
    messages=[{"role": "user", "content": "Hello"}],
)
print(resp.choices[0].message.content)
```

That's it. The `model` field is treated as compatible but TideLink auto-selects the best available backend and fails over across providers — you don't manage provider keys.

## Using the bundled thin client

```python
from tidelink import TideLink

tl = TideLink("sk_你的TideLink密钥")
out = tl.chat([{"role": "user", "content": "用一句话介绍太原"}], model="glm-4-flash")
print(out["choices"][0]["message"]["content"])
```

Node:

```js
const { TideLink } = require('./tidelink');
const tl = new TideLink('sk_你的TideLink密钥');
tl.chat([{ role: 'user', content: 'Hi' }]).then(r => console.log(r.choices[0].message.content));
```

## Migrate from OpenAI

1. Change `base_url` / `OPENAI_BASE_URL` to `https://tidelink.app/v1`.
2. Replace your OpenAI key with your TideLink key.
3. (Optional) set `model` to any placeholder like `glm-4-flash` — TideLink routes automatically.

See [MIGRATION.md](./MIGRATION.md) for Cursor, Claude Code, Cline, Continue, Dify, Chatbox and more.

## Docs

- API Reference & Quickstart: https://tidelink.app/docs/
- Integrations: https://tidelink.app/docs/integrations.html
- Live stats: https://tidelink.app/stats/

## License

MIT — see [LICENSE](./LICENSE).
