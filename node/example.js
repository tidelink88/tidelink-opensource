// Example: one-shot chat with TideLink (Node).
const { TideLink } = require('./tidelink');

const key = process.env.TIDELINK_API_KEY || 'sk_你的TideLink密钥';
const tl = new TideLink(key);

tl.chat([{ role: 'user', content: '用一句话介绍太原' }], { model: 'glm-4-flash' })
  .then((r) => {
    console.log(r.choices[0].message.content);
    console.log('billing:', r._billing);
  })
  .catch((e) => console.error('TideLink error:', e.message));
