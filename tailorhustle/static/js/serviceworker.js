// var staticCacheName = 'tailorhustle-v1';
//
// self.addEventListener('install', function(event) {
//   event.waitUntil(
//     caches.open(staticCacheName).then(function(cache) {
//       return cache.addAll([
//         '',
//       ]);
//     })
//   );
// });
//
// self.addEventListener('fetch', function(event) {
//   var requestUrl = new URL(event.request.url);
//     if (requestUrl.origin === location.origin) {
//       if ((requestUrl.pathname === '/')) {
//         event.respondWith(caches.match(''));
//         return;
//       }
//     }
//     event.respondWith(
//       caches.match(event.request).then(function(response) {
//         return response || fetch(event.request);
//       })
//     );
// });

// var staticCacheName = 'tailorhustle-v1';
//
// self.addEventListener('install', function (event) {
//     event.waitUntil(
//         caches.open(staticCacheName).then(function (cache) {
//             return cache.addAll([
//                 '',
//                 '/',
//                 '/store_dashboard/',
//             ]);
//         })
//     );
// });
//
// self.addAllEventListener('fetch', function (event) {
//     var requestUrl = new URL(event.request.url);
//     if (requestUrl.origin === location.origin) {
//         if ((requestUrl.pathname === '/')) {
//             event.respondWith(caches.match(''));
//             return;
//         }
//     }
//     event.respondWith(
//         caches.match(event.request).then(function (response) {
//             return response || fetch(event.request);
//         })
//     );
// });

// // Outer code
// var staticCacheName = 'tailorhustle-v1';
//
// self.addEventListener("install", event => {
//     this.skipWaiting();
//     event.waitUntil(
//         caches.open(staticCacheName)
//             .then(cache => {
//                 return cache.addAll([
//                     '',
//                     '/',
//                     '/search_posts/',
//                     '/mobile_notifications/',
//                 ]);
//             })
//     )
// });
//
// // Clear cache on activate
// self.addEventListener('activate', event => {
//     event.waitUntil(
//         caches.keys().then(cacheNames => {
//             return Promise.all(
//                 cacheNames
//                     .filter(cacheName => (cacheName.startsWith("django-pwa-")))
//                     .filter(cacheName => (cacheName !== staticCacheName))
//                     .map(cacheName => caches.delete(cacheName))
//             );
//         })
//     );
// });
//
// // Serve from Cache
// self.addEventListener("fetch", event => {
//     event.respondWith(
//         caches.match(event.request)
//             .then(response => {
//                 return response || fetch(event.request);
//             })
//             .catch(() => {
//                 return caches.match('offline');
//             })
//     )
// });

//Outer - 3
var staticCacheName = 'djangopwa-v1';

self.oninstall = function (evt) {
    evt.waitUntil(caches.open(staticCacheName).then(function (cache) {
        return Promise.all(['/', 'mobile_notifications/', 'search_posts/', 'post/new/'].map(function (url) {
            return fetch(new Request(url, { redirect: 'manual' })).then(function (res) {
                return cache.put(url, res);
            });
        }));
    }));
};
// self.onfetch = function (evt) {
//     var url = new URL(evt.request.url);
//     if (url.pathname != '/' && url.pathname != 'main/feed.html') return;
//     evt.respondWith(caches.match(evt.request, { cacheName: staticCacheName }));
// };

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});
// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('offline');
            })
    )
});