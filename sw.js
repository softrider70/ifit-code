/* Service Worker fuer "iFit Code".
 * Legt die Seite samt Symbol im Cache ab, damit sie ohne Netz startet.
 * Voraussetzung: https (GitHub Pages) oder localhost.
 */

var CACHE = "ifit-code-v2";
var DATEIEN = [
  "./index.html",
  "./ifit-icon.png",
  "./manifest.json"
];

self.addEventListener("install", function (ereignis) {
  ereignis.waitUntil(
    caches.open(CACHE)
      .then(function (speicher) { return speicher.addAll(DATEIEN); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (ereignis) {
  ereignis.waitUntil(
    caches.keys()
      .then(function (namen) {
        return Promise.all(namen.map(function (name) {
          if (name !== CACHE) { return caches.delete(name); }
        }));
      })
      .then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (ereignis) {
  if (ereignis.request.method !== "GET") { return; }

  ereignis.respondWith(
    caches.match(ereignis.request).then(function (treffer) {
      if (treffer) { return treffer; }
      return fetch(ereignis.request).then(function (antwort) {
        var kopie = antwort.clone();
        caches.open(CACHE).then(function (speicher) {
          speicher.put(ereignis.request, kopie);
        });
        return antwort;
      }).catch(function () {
        return caches.match("./index.html");
      });
    })
  );
});
