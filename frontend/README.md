# Frontend (Vanilla JS)

## Features
- Text paste input + PDF/TXT drag-drop upload
- ORP pivot highlighting
- Play/Pause/Restart controls
- Speed control (250-1000 WPM)
- Seekable progress bar + keyboard shortcuts
- Backend fallback to local processing
- Responsive dark theme

## Run
```bash
cd frontend
python -m http.server 5173
```

Set backend URL with `.env` (see `.env.example`) or edit `js/config.js`.

## Deploy (Vercel)
- Static deploy of `frontend/`
- `vercel.json` rewrites to `index.html`
