# 🌊 TideLink

> **One API key. Every Chinese LLM.**

TideLink is an **OpenAI-compatible LLM gateway** that unifies China's best
large language models — **GLM, Qwen, DeepSeek, Hunyuan, Doubao** — behind a
single `/v1/chat/completions` endpoint, with **automatic failover** handled on
the gateway side.

- 🔌 **Drop-in for OpenAI** — point your existing code at TideLink, keep it as-is.
- 🔀 **Automatic failover** — if one provider is down, the gateway routes to the next.
- 🔑 **BYOK-friendly** — bring your own upstream keys; we never touch your upstream bill.
- 💸 **Free to start** — get a free API key, no credit card required.

---

## Why TideLink

If you build with Chinese LLMs today, you juggle a handful of vendor SDKs,
auth schemes, and outage windows. TideLink collapses that into one OpenAI-style
endpoint:

```python
# before: per-vendor SDKs, per-vendor error handling
# after:  one client, one shape
```

Failover, model routing, and key management live on the gateway. Your code
stays OpenAI-shaped, so swapping in or out is a one-line change.

---

## Install

### Python

```bash
pip install "git+https://github.com/tidelink88/tidelink-opensource.git#subdirectory=python"
```

```python
from tidelink import TideLink

tl = TideLink()  # reads TIDELINK_API_KEY from the environment
r = tl.chat([{"role": "user", "content": "Explain failover in one sentence."}],
            model="glm-4-flash")
print(r["choices"][0]["message"]["content"])
```

A `tidelink-cli` command is also installed for quick terminal chats:

```bash
export TIDELINK_API_KEY=YOUR_KEY
tidelink-cli "Explain failover in one sentence."
```

### Node.js

Zero dependencies — clone and require:

```bash
git clone https://github.com/tidelink88/tidelink-opensource
cd tidelink-opensource/node
# nothing to install — tidelink.js is dependency-free
```

```js
const { TideLink } = require('./tidelink.js');

const tl = new TideLink();  // reads TIDELINK_API_KEY
tl.chat([{ role: 'user', content: 'Explain failover in one sentence.' }],
        { model: 'glm-4-flash' })
  .then(r => console.log(r.choices[0].message.content));
```

*(Once published to npm you'll be able to `npm install tidelink-sdk` and
`require('tidelink-sdk')` instead.)*

---

## Get a free API key

👉 **https://tidelink.xyz/dashboard.html?cid=gh**

No credit card. Free tier included — enough to ship a prototype today.

---

## Bring your own key (BYOK)

Prefer to use your own upstream provider keys? Register a BYOK key and
TideLink routes through your account — **you pay your provider directly, we
never see your upstream bill.** This is the cheapest way to run TideLink at
scale.

👉 **https://tidelink.xyz/v1/byok/keys?cid=gh**

---

## Available models

`glm-4-flash`, `qwen-plus`, `deepseek-chat`, `hunyuan-pro`, `doubao-pro`, and
more. See the live list programmatically:

```python
print([m["id"] for m in tl.models()["data"]])
```

or hit the public endpoint:

```bash
curl https://tidelink.xyz/v1/models
```

---

## ⭐ Why a star helps

This repo is the fastest way to point your existing OpenAI code at China's
best LLMs with automatic failover. If it saves you a key or two, a star helps
other developers find it — and tells us which examples to build next.

👉 **Get a free API key:** https://tidelink.xyz/dashboard.html?cid=gh

---

## License

[MIT](LICENSE) © 2026 TideLink
