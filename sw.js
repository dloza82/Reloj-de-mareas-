const CACHE = 'san-lorenzo-v2';
self.addEventListener('install', e => {
  self.skipWaiting();
});
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k))))
  );
});
self.addEventListener('fetch', e => {
  // Siempre ir a la red, nunca cachear
  e.respondWith(fetch(e.request));
});
