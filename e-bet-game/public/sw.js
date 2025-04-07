const CACHE_NAME = 'ebet-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/favicon.ico',
  '/logo.png',
  '/icon-192x192.png',
  '/icon-512x512.png',
  '/manifest.json'
];

self.addEventListener('install', event => {
  console.log('✅ Service Worker installé !');

  event.waitUntil(
    caches.open(CACHE_NAME).then(async cache => {
      console.log('📦 Tentative de mise en cache des fichiers...');

      // Essaye chaque fichier individuellement
      for (const url of urlsToCache) {
        try {
          await cache.add(url);
          console.log(`✅ Mis en cache : ${url}`);
        } catch (error) {
          console.warn(`⚠️ Échec du cache pour ${url} :`, error);
        }
      }
    })
  );
});

self.addEventListener('activate', event => {
  console.log('🔄 Service Worker activé !');
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
