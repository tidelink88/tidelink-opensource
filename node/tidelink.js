// TideLink — tiny zero-dependency Node client for the OpenAI-compatible gateway.
// https://tidelink.app  ·  base_url: https://tidelink.app/v1
// The `model` field is treated as compatible; TideLink auto-selects the best
// available backend and fails over across providers.

const DEFAULT_BASE = 'https://tidelink.app/v1';

class TideLink {
  constructor(apiKey, baseUrl = DEFAULT_BASE) {
    this.base = baseUrl.replace(/\/+$/, '');
    this.apiKey = apiKey;
  }

  async chat(messages, opts = {}) {
    const model = opts.model || 'glm-4-flash';
    const stream = !!opts.stream;
    const body = { model, messages, stream, ...opts.extra };
    const res = await fetch(`${this.base}/chat/completions`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`${res.status} ${text.slice(0, 300)}`);
    }
    if (stream) return res; // caller iterates res.body (SSE)
    return res.json();
  }

  async usage() {
    const res = await fetch(`${this.base}/usage`, {
      headers: { Authorization: `Bearer ${this.apiKey}` },
    });
    if (!res.ok) throw new Error(`${res.status} ${await res.text().slice(0, 300)}`);
    return res.json();
  }
}

module.exports = { TideLink };
