/* Service Worker para Coloquio Parcial 1 - Cachea todo para uso offline */
const CACHE_NAME = 'coloquio-p1-v1';
const ASSETS = [
  './',
  './index.html',
  './app.js',
  './styles.css',
  './tracks.js',
  './manifest.webmanifest',
  // Audios - se cachean bajo demanda (abajo)
];

// Instalación: cachea assets estáticos
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

// Activación: limpia caches viejos
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: network-first para HTML/JS/CSS, cache-first para audios
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  const isAudio = url.pathname.startsWith('/audio/') || url.pathname.endsWith('.mp3');
  const isAsset = ASSETS.some((a) => url.pathname.endsWith(a.replace('./', '')));

  if (isAudio) {
    // Cache-first para audios (son grandes y no cambian)
    event.respondWith(
      caches.match(event.request).then((cached) => {
        if (cached) return cached;
        return fetch(event.request).then((response) => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        }).catch(() => cached);
      })
    );
    return;
  }

  // Network-first para todo lo demás (permite actualizaciones)
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});

// Mensaje para forzar actualización
self.addEventListener('message', (event) => {
  if (event.data === 'skipWaiting') self.skipWaiting();
});