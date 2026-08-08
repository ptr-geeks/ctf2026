/**
 * OrbitBoard — Security Officer bot.
 * Logs in as Officer Vega and visits any path it is asked to review.
 * Internal-only service — never expose PORT through the public proxy.
 */

import http from 'node:http';
import { chromium } from 'playwright';

const SITE_URL        = (process.env.SITE_URL ?? 'http://localhost:5000').replace(/\/$/, '');
const PORT            = Number(process.env.PORT ?? 3001);
const MAX_CONCURRENCY = Number(process.env.MAX_CONCURRENCY ?? 4);
const DEFAULT_WAIT_MS = Number(process.env.DEFAULT_WAIT_MS ?? 4000);
const BOT_USERNAME    = process.env.BOT_USERNAME ?? 'officer_vega';
const BOT_PASSWORD    = process.env.BOT_PASSWORD ?? '';

let browser;
async function getBrowser() {
  if (!browser) {
    browser = await chromium.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding',
        '--disable-backgrounding-occluded-windows',
        '--disable-features=CalculateNativeWinOcclusion',
      ],
    });
  }
  return browser;
}

let active = 0;
const queue = [];

function schedule(job) {
  return new Promise((resolve, reject) => {
    queue.push({ job, resolve, reject });
    pump();
  });
}

function pump() {
  if (active >= MAX_CONCURRENCY) return;
  const next = queue.shift();
  if (!next) return;
  active++;
  next.job()
    .then(next.resolve, next.reject)
    .finally(() => { active--; pump(); });
}

async function visit({ path, waitMs }) {
  if (typeof path !== 'string' || !path.startsWith('/')) {
    throw new Error('bad path');
  }
  const url = SITE_URL + path;
  const b   = await getBrowser();
  const ctx = await b.newContext();
  const page = await ctx.newPage();
  try {
    // Log in as Officer Vega so the session cookie (and thus csrf_token)
    // is present when the post page is rendered.
    if (BOT_PASSWORD) {
      await ctx.request
        .post(`${SITE_URL}/login`, {
          form: {
            action:   'login',
            username: BOT_USERNAME,
            password: BOT_PASSWORD,
          },
        })
        .catch((e) => console.error('[login] failed:', e.message));
    }

    await page.goto(url, { waitUntil: 'load', timeout: 15000 });
    await page.waitForTimeout(Number(waitMs ?? DEFAULT_WAIT_MS));
  } finally {
    await ctx.close();
  }
}

// ── HTTP server ───────────────────────────────────────────────────────────────

const server = http.createServer((req, res) => {
  if (req.method === 'GET' && req.url === '/healthz') {
    res.writeHead(200).end('ok');
    return;
  }

  if (req.method === 'POST' && req.url === '/visit') {
    let body = '';
    req.on('data', (chunk) => {
      body += chunk;
      if (body.length > 1e6) req.destroy();
    });
    req.on('end', async () => {
      let payload;
      try {
        payload = JSON.parse(body);
      } catch {
        res.writeHead(400).end('bad json');
        return;
      }

      schedule(() => visit(payload))
        .then(() => res.writeHead(200).end('ok'))
        .catch((e) => {
          console.error('[visit] error:', e.message);
          res.writeHead(500).end('error');
        });
    });
    return;
  }

  res.writeHead(404).end();
});

server.listen(PORT, () => console.log(`[bot] listening on :${PORT}`));
