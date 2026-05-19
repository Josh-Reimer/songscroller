# Song Scroller 📜🎶

Now you can doom scroll the Christian Hymnal songbook. Congratulations.

Song Scroller transforms the classic hymnal experience into a modern, TikTok-style vertical scrolling Progressive Web App (PWA). Swipe through randomly served hymns, save your favorites to a slide-out sidebar, and share them directly from your phone.

## ✨ Features
- **Endless Doom Scrolling:** Smooth, infinite vertical scrolling through random hymns.
- **Progressive Web App (PWA):** Fully responsive edge-to-edge mobile design. You can install it directly to your iOS or Android home screen!
- **Offline Caching:** Uses a Service Worker to automatically cache the UI and any song images you scroll past. Lose internet? Keep scrolling through your cached history.
- **Local Bookmarking:** Tap the frosted-glass bookmark button to save hymns. They are stored natively in your browser's `localStorage` and can be viewed via the slide-out sidebar menu.
- **Native Sharing:** Send the physical JPG of a song directly to a friend via iMessage/WhatsApp using the native share button (or download it on desktop).

## 🚀 Setup & Installation

I have not provided the song JPGs in this repository to save space, but you can generate them yourself!

1. Download the Christian Hymnal PDF from [Archive.org](https://archive.org/details/christianhymnalc00chur).
2. Place the `christianhymnalc00chur.pdf` in the root of this project.
3. Run the included Python script to automatically slice the PDF into images:
   ```bash
   python download_and_convert.py
   ```
   *Note: This script requires `PyMuPDF` (`pip install PyMuPDF`). It will extract the pages and place them into the `img/` directory with names like `songscroller1.jpg`.*

## 🏃 Running the App
The app is powered by a lightweight Flask backend to serve the files and PWA manifest.

1. Install Flask if you haven't already:
   ```bash
   pip install flask
   ```
2. Start the server:
   ```bash
   python app.py
   ```
3. Open `http://localhost:5023` in your browser. On a mobile device (or in Chrome on Desktop), look for the prompt to **Install App** to get the full native experience!

## 🛠 Tech Stack
- **Backend:** Python + Flask
- **Frontend:** Vanilla HTML, CSS, JavaScript
- **PWA Capabilities:** Manifest JSON, Service Workers (Offline Image Interception)
- **Data Storage:** Browser `localStorage` API