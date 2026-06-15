# Bug Report — Song Scroller Code Review

Generated: 2026-06-14

## Bugs

### 1. Share cancel triggers misleading error alert
**File:** `templates/Feed.html:557`

When a user opens the native share sheet and dismisses it without sharing, the browser rejects `navigator.share()` with `DOMException(name='AbortError')`. The catch block has no guard for this case and unconditionally calls `alert('Could not share the song.')`.

**Fix:** Add `if (error.name === 'AbortError') return;` as the first line of the catch block.

---

### 2. Service worker caches stale VALID_INDICES in rendered HTML
**File:** `sw.js:3`

The install handler caches `'/'` (the Jinja2-rendered page with `VALID_INDICES` baked in). After images are added or removed, all installed-PWA users continue receiving the old index list until `CACHE_NAME` is manually bumped and redeployed. New images never appear; deleted indices produce 404s.

**Fix:** Serve `VALID_INDICES` from a separate `/api/indices` JSON endpoint (not baked into HTML), or implement a deploy-time cache-busting strategy (e.g. hash in `CACHE_NAME`).

---

### 3. Unbounded DOM growth — slides never removed
**File:** `templates/Feed.html:436`

`handleHymnalPages()` and `jumpToBookmark()` only append slides to `#strip`; nothing ever removes them. After ~100 swipes the DOM holds 100 full-height elements each retaining a decoded JPEG bitmap. On mobile this accumulates hundreds of MB and triggers the OS memory watchdog, killing the tab.

**Fix:** In `dragEnd`, after advancing `current`, remove slide elements more than 2 positions behind `current` from the DOM.

---

### 4. `startY = 0` makes drag guards dead before first touchend
**File:** `templates/Feed.html:354`

`startY` is initialized to `0`, but `dragMove` and `dragEnd` guard with `if (startY === null) return`. The guard only works after the first `dragEnd` sets `startY = null`. Before that, a stray `touchmove` (carried-over gesture on some Android browsers) runs with stale `startY = 0`, computes a large bogus `dragDelta`, and snaps the strip to the wrong slide.

**Fix:** Change the initialization to `let startY = null;`.

---

## Security

### 5. Bookmark URLs from localStorage injected into innerHTML unsanitized
**File:** `templates/Feed.html:584`

`renderBookmarks()` and `jumpToBookmark()` inject URL strings read from `localStorage` directly into `innerHTML`/`insertAdjacentHTML`. If `localStorage` is poisoned (via devtools, a browser extension, or a same-origin script), a payload like `" onerror="alert(1)` executes arbitrary script in the page context.

**Fix:** Replace `innerHTML` template literals with `document.createElement` + `element.setAttribute` for all dynamic attribute construction.

---

### 6. `serve_image` passes filename to `send_from_directory` with no validation
**File:** `app.py:20`

`filename` from the URL path is passed to `send_from_directory("img", filename)` without any pattern check. On Werkzeug <1.0 this allows path traversal (`GET /img/../app.py`). On any version, non-`.jpg` files in `img/` are served without restriction. There is no `requirements.txt` pinning Werkzeug to a safe version.

**Fix:** Validate the filename against `^songscroller\d+\.jpg$` before calling `send_from_directory`, or add a `requirements.txt` with `werkzeug>=1.0`.

---

## Cleanup

### 7. Dead `srcView` variable queried on every slide creation
**File:** `templates/Feed.html:438`

`let srcView = document.getElementById(\`Isrc${slideIndex}\`)` is assigned but never read. It performs a live DOM query on every call to `handleHymnalPages()` for no effect.

**Fix:** Remove the line.

---

### 8. Slide HTML template duplicated between `handleHymnalPages` and `jumpToBookmark`
**File:** `templates/Feed.html:423` and `templates/Feed.html:601`

The full `.slide.slide-image` HTML — including both SVG buttons, overlay, and counter — is copy-pasted nearly verbatim in two places. Changes to the layout must be applied in both locations in sync.

**Fix:** Extract a shared `createSlideHTML(imgUrl, slideIndex, bookmarkClass)` function that returns the template string.
