# tidelink (Python client)

Tiny zero-dependency client for the TideLink OpenAI-compatible LLM gateway.

See the [project README](https://github.com/tidelink88/tidelink-opensource#readme)
for full documentation and examples.

## Install

```bash
pip install "git+https://github.com/tidelink88/tidelink-opensource.git#subdirectory=python"
```

## Usage

```python
from tidelink import TideLink

tl = TideLink()  # reads TIDELINK_API_KEY from the environment
print(tl.chat([{"role": "user", "content": "Hi"}],
              model="glm-4-flash")["choices"][0]["message"]["content"])
```

Get a free API key (no card required): https://tidelink.xyz/dashboard.html?cid=gh
