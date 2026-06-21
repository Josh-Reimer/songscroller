# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

The `img/` directory is not committed. Generate it before running the app:

```bash
pip3 install -r requirements.txt
python3 download_and_convert.py   # downloads the PDF from Archive.org (via curl) and slices it into img/songscroller{n}.jpg
```

## Running the app

**Local development:**
```bash
python3 app.py
```

**Production (with Gunicorn):**
```bash
gunicorn --workers 4 --bind 0.0.0.0:5023 app:app
```

**Docker:**
```bash
docker-compose up
```

The app opens at `http://localhost:5023`. For PWA testing on mobile devices on the same network, ensure the app is bound to `0.0.0.0`.

## Architecture

This is a single-page PWA with a minimal Flask backend (`app.py`) and one Jinja2 template (`templates/Feed.html`).

**Data flow:**
- `app.py` scans `img/` at request time and passes `valid_indices` (page numbers of JPGs >30KB, filtering out blank/cover pages) into the template via Jinja2.
- `Feed.html` receives `VALID_INDICES` as an inlined JSON array and uses it to build random image URLs entirely client-side — the server never serves another API endpoint after the initial page load.

**Frontend slide engine (`Feed.html`):**
- A `.strip` flex column holds all `.slide` divs stacked vertically. Navigation is done by CSS `translateY` on the strip (not scrolling).
- `TOTAL_SLIDES` and `current` track state. `handleHymnalPages()` appends a new slide to the DOM when the user reaches the second-to-last slide, creating the infinite scroll illusion.
- A rolling preload queue (`RANDOM_IMAGES`, size 15) keeps images fetched ahead of the current position. When a slide is consumed, one new `Image()` is added to the back of the queue.
- Touch events drive drag-and-snap; mouse drag is commented out. Keyboard arrow keys also work.
- Animations use the `.animating` CSS class with a 0.5s cubic-bezier easing. The `moveTo()` function uses `requestAnimationFrame` to defer the transform change when animating, ensuring the browser processes the class addition before the transform (this is critical—without the frame delay, transitions won't fire reliably).

**Bookmarks:** stored in `localStorage` under `bookmarked_hymns` as a JSON array of `/img/songscrollerN.jpg` URL strings. The sidebar reads this array on open; `jumpToBookmark()` injects the bookmarked slide at the end of the strip and scrolls to it.

**PWA / Service Worker (`sw.js`):**
- On install, caches `/`, `/manifest.json`, and `/icon.svg`.
- On fetch, serves from cache first; images (`/img/`) are cached on-the-fly as they are first requested, enabling offline replay of viewed hymns.
- Cache is versioned by `CACHE_NAME = 'songscroller-v1'`. Bump this string to invalidate the cache on next deploy.

**No build step, no dependencies beyond Flask and PyMuPDF.** All JS is vanilla, inline in the template.

## Known Issues & Debugging

**Animations stop working after a few scrolls:**
This happens when the `.animating` class and `transform` style are set in the same synchronous call—the browser batches them without creating a transition. Fix: use `requestAnimationFrame` to defer the transform change (see `moveTo()` function in `Feed.html`).

**Service Worker cache not invalidating:**
Update the `CACHE_NAME` string in `sw.js` to force browsers to re-fetch cached assets on next load.

**PDF download fails:**
The script uses `curl` instead of `urllib` (Archive.org blocks urllib). Ensure `curl` is available, or check that the `christianhymnalc00chur.pdf` file is pre-mounted in Docker.
