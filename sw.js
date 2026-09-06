// CareerTracker Service Worker for PWA Shortcut & Offline Caching (v4)
const CACHE_NAME = 'careertracker-v4';
const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json?v=4',
  './favicon.ico?v=4',
  './apple-touch-icon.png?v=4',
  './apple-touch-icon-precomposed.png?v=4',
  './icon-192.png?v=4',
  './icon-512.png?v=4',
  './assets/images/logo.svg?v=4',
  './assets/images/apple-touch-icon.png?v=4',
  './assets/images/icon-maskable-192.png?v=4',
  './assets/images/icon-maskable-512.png?v=4',
  './assets/images/favicon-32.png?v=4',
  './assets/images/favicon-16.png?v=4',
  './assets/images/favicon.png?v=4'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('SW cache.addAll notice:', err);
      });
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      const fetchPromise = fetch(event.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseToCache);
            });
          }
          return networkResponse;
        })
        .catch(() => cachedResponse);

      return cachedResponse || fetchPromise;
    })
  );
});
