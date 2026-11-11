/* Kasi-Logistics service worker
   Offline strategy:
   - App shell (/, /index.html, manifest): network-first, cache fallback.
   - Local CSS, icon fonts and Leaflet are pre-cached with the app shell.
   - Optional remote CDN requests: stale-while-revalidate.
   - Map tiles: cache-first ONLY for tiles the user actually viewed (standard
     HTTP caching behaviour - no pre-seeding or bulk fetching, per the
     OpenStreetMap tile usage policy).
   - OSRM route API: network-first, keep last good responses so a planned
     route survives a signal drop. */
'use strict';

const SHELL_CACHE = 'kasi-shell-v3';
const CDN_CACHE = 'kasi-cdn-v1';
const TILE_CACHE = 'kasi-tiles-v1';
const ROUTE_CACHE = 'kasi-routes-v1';

const SHELL_URLS = ['/', '/index.html', '/manifest.webmanifest', '/vendor/tailwind.css', '/icons/icon-180.png', '/icons/icon-192.png', '/icons/icon-512.png', '/vendor/leaflet/leaflet.css', '/vendor/leaflet/leaflet.js', '/vendor/leaflet/images/layers-2x.png', '/vendor/leaflet/images/marker-shadow.png', '/vendor/leaflet/images/marker-icon-2x.png', '/vendor/leaflet/images/marker-icon.png', '/vendor/leaflet/images/layers.png', '/vendor/fontawesome/css/all.min.css', '/vendor/fontawesome/webfonts/fa-brands-400.woff2', '/vendor/fontawesome/webfonts/fa-regular-400.woff2', '/vendor/fontawesome/webfonts/fa-v4compatibility.woff2', '/vendor/fontawesome/webfonts/fa-solid-900.woff2'];

const CDN_HOSTS = ['cdn.tailwindcss.com', 'cdnjs.cloudflare.com', 'unpkg.com', 'raw.githubusercontent.com'];
const TILE_HOSTS = ['tile.openstreetmap.org', 'a.tile.openstreetmap.org', 'b.tile.openstreetmap.org', 'c.tile.openstreetmap.org', 'server.arcgisonline.com'];
const ROUTE_HOSTS = ['router.project-osrm.org'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then((cache) => cache.addAll(SHELL_URLS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => ![SHELL_CACHE, CDN_CACHE, TILE_CACHE, ROUTE_CACHE].includes(k)).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

function isHost(url, hosts) { return hosts.includes(url.hostname); }

async function networkFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  try {
    const fresh = await fetch(request);
    if (fresh && (fresh.status === 200 || fresh.type === 'opaque')) cache.put(request, fresh.clone());
    return fresh;
  } catch (err) {
    const cached = await cache.match(request);
    if (cached) return cached;
    throw err;
  }
}

async function cacheFirst(request, cacheName, maxEntries) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  if (cached) return cached;
  const fresh = await fetch(request);
  if (fresh && (fresh.status === 200 || fresh.type === 'opaque')) {
    cache.put(request, fresh.clone());
    if (maxEntries) {
      cache.keys().then((keys) => {
        if (keys.length > maxEntries) cache.delete(keys[0]);
      });
    }
  }
  return fresh;
}

async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const freshPromise = fetch(request).then((fresh) => {
    if (fresh && (fresh.status === 200 || fresh.type === 'opaque')) cache.put(request, fresh.clone());
    return fresh;
  }).catch(() => null);
  return cached || (await freshPromise) || Response.error();
}

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);

  if (isHost(url, ROUTE_HOSTS)) {
    event.respondWith(networkFirst(request, ROUTE_CACHE));
    return;
  }
  if (isHost(url, TILE_HOSTS)) {
    event.respondWith(cacheFirst(request, TILE_CACHE, 1500));
    return;
  }
  if (isHost(url, CDN_HOSTS)) {
    event.respondWith(staleWhileRevalidate(request, CDN_CACHE));
    return;
  }
  if (request.mode === 'navigate' || SHELL_URLS.includes(url.pathname)) {
    event.respondWith(networkFirst(request, SHELL_CACHE));
    return;
  }
  if (url.origin === self.location.origin) {
    event.respondWith(cacheFirst(request, SHELL_CACHE));
    return;
  }
});
