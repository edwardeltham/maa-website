# Mahatma Alumni Association website

Static site: plain HTML, CSS and a little JavaScript. No build step needed to host it.

## Publish on GitHub Pages
1. Create a repo (e.g. `maa-website`) and upload everything in this folder to the `main` branch.
2. Settings > Pages > Build and deployment > Source: **Deploy from a branch**, Branch: `main`, folder `/ (root)`. Save.
3. The site appears at `https://<your-username>.github.io/maa-website/` in about a minute.
4. For a custom domain, add it under Settings > Pages and create a `CNAME` file.

## Add photos
Every grey-dashed box is a photo placeholder. Put images in `assets/img/` and, in the HTML, add `data-src="assets/img/name.jpg"` to the matching `<figure class="ph ...">`. Ratios: portraits `4:5`, wide `4:3`, square `1:1`. Aim for under 300 KB each (JPG/WebP).
Needed: Ma'am portrait, Ma'am with children, timeline photos (5), six "memory lane" photos, team portraits.

## Edit text
Content lives in `build.py`. Edit it and run `python3 build.py` to regenerate all pages. Or edit the `.html` files directly.

## Fill in before going live
- Link placeholders (`data-todo`): YouTube webinar link, Instagram, YouTube channel, WhatsApp.
- Vision and mission wording (draft).
- Kurals in `assets/js/main.js`: have a Tamil teacher confirm text and meanings.
- Team names and titles (Arun Kesav's title, council, committees, batch reps).
- Venue (deliberately not named) and the contact email `alumni@mahatmaschools.com`.
- The webinar banner hides itself after 31 Oct 2026, 12:00 IST.
