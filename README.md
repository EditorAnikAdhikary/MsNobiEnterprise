# M/s Nabi Enterprises & M/s Jhimik Transport Agency — Website

Static multi-page website, no dependencies. Bengali is the default language; English is available from the header switcher (choice persists via localStorage).

## Structure
- `site/` — deployable output (clean URLs: `/about/`, `/products/cement/` …)
- `build.py`, `style.css`, `main.js` — generator and shared source. Edit these, then run `python3 build.py site`.
- `site/assets/logo-*.svg` — logo mark (dark/light) and horizontal lockup.
- `site/assets/images/MANIFEST.md` — **the 16 photographs still required** (exact filenames and subjects).

## Run locally
    cd site && python3 -m http.server 8000     # open http://localhost:8000/
(Paths are root-absolute, so serve from the `site/` folder; opening files directly via file:// will not resolve them.)

## Deploy
Upload `site/` to any static host (Netlify, Cloudflare Pages, GitHub Pages user site, Nginx). `404.html` is the error page. Folder URLs work out of the box on all of these.

## Open items before launch
1. **Photographs are not included.** Add the files listed in `MANIFEST.md`; until then pages show a navy fallback block. Record licences in `CREDITS.md`.
2. **Contact form is not connected** to any backend; it says so on submit. Connect a form service or server endpoint.
3. Phone numbers and address come from the existing site and need owner confirmation. No email, map, registration, history or specifications were invented.
4. Proprietor portrait needs a genuine photograph (`about/proprietor-portrait.jpg`).
5. Bengali/English copy should be proofread by a native reader.
