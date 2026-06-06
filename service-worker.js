// fab.games Service Worker
// Smart caching — assets only, NEVER game logic or auth pages

const CACHE_NAME = 'fabgames-v1';
const CACHE_VERSION = '1.0.0';

// Only cache static assets — fonts, CSS, images
// NEVER cache auth-sensitive pages
const STATIC_ASSETS = [
  '/',
  '/about',
  '/icon-192.png',
  '/icon-512.png',
];

// Pages that MUST always hit the server — never serve from cache
const NEVER_CACHE = [
  '/play',
  '/join',
  '/login',
  '/success',
  '/api/',
  '/veggies',
];

// ── INSTALL ──────────────────────────────────────
self.addEventListener('install', event => {
  console.log('[fab.games SW] Installing v' + CACHE_VERSION);
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// ── ACTIVATE ─────────────────────────────────────
self.addEventListener('activate', event => {
  console.log('[fab.games SW] Activating');
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => {
            console.log('[fab.games SW] Deleting old cache:', key);
            return caches.delete(key);
          })
      );
    })
  );
  self.clients.claim();
});

// ── FETCH ─────────────────────────────────────────
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Always go to network for auth-sensitive pages
  const neverCache = NEVER_CACHE.some(path => url.pathname.startsWith(path));
  if(neverCache){
    event.respondWith(
      fetch(event.request).catch(() => {
        // If offline and trying to access game — show offline page
        return new Response(
          `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>fab.games — Offline</title>
          <style>
            *{margin:0;padding:0;box-sizing:border-box;}
            body{background:#070708;color:#f0efe8;font-family:Inter,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;text-align:center;padding:20px;}
            .wrap{max-width:320px;}
            .logo{font-size:28px;letter-spacing:4px;color:#c9a84c;margin-bottom:24px;font-weight:300;}
            h1{font-size:18px;font-weight:300;letter-spacing:2px;margin-bottom:12px;}
            p{font-size:13px;color:rgba(240,239,232,0.5);line-height:1.7;margin-bottom:24px;}
            a{display:inline-block;padding:12px 24px;border:1px solid rgba(201,168,76,0.4);color:#c9a84c;text-decoration:none;font-size:11px;letter-spacing:3px;text-transform:uppercase;}
          </style></head>
          <body><div class="wrap">
            <div class="logo">fab.games</div>
            <h1>You are offline</h1>
            <p>fab.games needs an internet connection to verify your subscription and load games.<br><br>Connect to the internet and try again!!</p>
            <a href="/play">Try Again</a>
          </div></body></html>`,
          { headers: { 'Content-Type': 'text/html' } }
        );
      })
    );
    return;
  }

  // For everything else — network first, cache fallback
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Cache successful GET responses for static assets
        if(event.request.method === 'GET' && response.status === 200){
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        return caches.match(event.request);
      })
  );
});
