const CACHE_PREFIX = 'songscroller';
let CACHE_NAME = null;

async function getCacheName() {
  if (CACHE_NAME) return CACHE_NAME;
  try {
    const res = await fetch('/api/version');
    const data = await res.json();
    CACHE_NAME = `${CACHE_PREFIX}-${data.version}`;
  } catch {
    CACHE_NAME = `${CACHE_PREFIX}-default`;
  }
  return CACHE_NAME;
}

const ASSETS_TO_CACHE = [
  '/manifest.json',
  '/icon.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    getCacheName().then(cacheName => {
      return caches.open(cacheName)
        .then(cache => cache.addAll(ASSETS_TO_CACHE))
        .then(() => self.skipWaiting());
    })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    getCacheName().then(cacheName => {
      return caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames.map(name => {
            if (name.startsWith(CACHE_PREFIX) && name !== cacheName) {
              return caches.delete(name);
            }
          })
        );
      }).then(() => self.clients.claim());
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    getCacheName().then(cacheName => {
      return caches.match(event.request)
        .then(response => {
          if (response) {
            return response;
          }

          const fetchRequest = event.request.clone();
          return fetch(fetchRequest).then(
            function(response) {
              if(!response || response.status !== 200 || response.type !== 'basic') {
                return response;
              }
              // Cache images on the fly
              if (event.request.url.includes('/img/')) {
                const responseToCache = response.clone();
                caches.open(cacheName)
                  .then(function(cache) {
                    cache.put(event.request, responseToCache);
                  });
              }
              return response;
            }
          );
        })
    })
  );
});
