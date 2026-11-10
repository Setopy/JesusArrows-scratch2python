// Offline support for the From Scratch to Python site.
// No version bump is needed when the book changes: every time the page is opened
// online, the saved copies (including the PDF) are re-checked and replaced if newer.
const CACHE = 'scratch2python-v2';
const FILES = [
  './',
  'index.html',
  'manifest.webmanifest',
  'scratch-to-python-workbook.pdf',
  'icons/icon-192.png',
  'icons/icon-512.png',
  'icons/apple-touch-icon.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Re-check every saved file with the server. Unchanged files cost almost nothing
// (the server answers "not modified"); changed ones replace the saved copy.
function refreshSaved() {
  return caches.open(CACHE).then((c) =>
    Promise.all(FILES.map((f) =>
      fetch(new Request(f, {cache: 'no-cache'}))
        .then((res) => (res && res.status === 200 ? c.put(f, res) : null))
        .catch(() => null)
    ))
  );
}

// Same-site files only: network first (so updates show), cached copy when offline.
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== self.location.origin) return;
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        if (res && res.status === 200 && e.request.mode === 'navigate') e.waitUntil(refreshSaved());
        if (res && res.ok && res.status === 200) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, copy));
        }
        return res;
      })
      .catch(() => caches.match(e.request, {ignoreSearch: true}).then((hit) => hit || caches.match('index.html')))
  );
});
