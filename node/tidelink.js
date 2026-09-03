'use strict';

// TideLink — tiny zero-dependency Node client for the TideLink
// OpenAI-compatible LLM gateway (GLM, Qwen, DeepSeek, Hunyuan, Doubao)
// with automatic failover handled on the gateway side.
//
// Free key: https://tidelink.xyz/dashboard.html?cid=gh

const DEFAULT_BASE_URL = 'https://tidelink.xyz/v1';
const FREE_KEY_URL = 'https://tidelink.xyz/dashboard.html?cid=gh';

class TideLink {
  constructor(apiKey, opts = {}) {
    this.apiKey = apiKey || process.env.TIDELINK_API_KEY;
    if (!this.apiKey) {
      throw new Error(
        'TideLink api_key is required. Pass it explicitly or set ' +
        'TIDELINK_API_KEY. Get a free key at ' + FREE_KEY_URL
      );
    }
    this.baseUrl = (opts.baseUrl || DEFAULT_BASE_URL).replace(/\/$/, '');
    this.timeout = opts.timeout || 60000;
  }

  async chat(messages, opts = {}) {
    const payload = {
      model: opts.model || 'glm-4-flash',
      messages,
      temperature: opts.temperature != null ? opts.temperature : 0.7,
    };
    if (opts.maxTokens != null) payload.max_tokens = opts.maxTokens;
    if (opts.stream) payload.stream = true;

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeout);
    let res;
    try {
      res = await fetch(`${this.baseUrl}/chat/completions`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
    } finally {
      clearTimeout(timer);
    }
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`TideLink ${res.status}: ${text}`);
    }
    return res.json();
  }

  async models() {
    const res = await fetch(`${this.baseUrl}/models`, {
      headers: { Authorization: `Bearer ${this.apiKey}` },
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`TideLink ${res.status}: ${text}`);
    }
    return res.json();
  }
}

module.exports = { TideLink };
