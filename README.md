# South Charlotte Video Edit — Kim

A single-page, no-login static site documenting the 12-step video edit workflow,
the YouTube performance audit, the After Effects motion spec and the thumbnail anatomy.

No build step. No dependencies. Just `index.html`.

---

## Hosting

Anyone can open the site in a normal browser — **no GitHub account, no login, nothing to install.**
GitHub only stores the files; the visitor just gets a normal web page at a normal URL.

### GitHub Pages (recommended — code and hosting in one place)

The repo must be **public** for Pages to work on the free plan.

```bash
git init
git add .
git commit -m "South Charlotte Video Edit — Kim"
git branch -M main
git remote add origin https://github.com/<your-username>/south-charlotte-video-edit.git
git push -u origin main
```

Then on GitHub: **Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)` → Save.**

Live in about a minute at:

```
https://<your-username>.github.io/south-charlotte-video-edit/
```

### Netlify (alternative — drag and drop, no git)

Drag the whole `site` folder onto [app.netlify.com/drop](https://app.netlify.com/drop).
You get a URL immediately. Sign in afterwards to keep it permanently and to rename it
to something like `south-charlotte-video-edit.netlify.app`.

Netlify is worth it if you want a **custom domain** or a nicer URL. Otherwise GitHub Pages
is simpler, because updating the site is the same `git push` that backs up the code.

Either way the result is identical for the visitor: a normal public website.

---

## Adding your screen recordings

Each of the 12 steps has an empty video slot. Drop a file into `videos/` with the
matching name and it appears automatically — no code change needed.

```
videos/step-01.mp4    Rough cut
videos/step-02.mp4    Remove silence
videos/step-03.mp4    Colour correction & grading
videos/step-04.mp4    Download b-roll
videos/step-05.mp4    Motion graphics
videos/step-06.mp4    Lay in b-roll & effects
videos/step-07.mp4    Refine clip by clip
videos/step-08.mp4    Music & ducking
videos/step-09.mp4    Rewatch & export
videos/step-10.mp4    Upload & package
videos/step-11.mp4    Thumbnail
videos/step-12.mp4    Blog post
```

If a file is missing, the striped blue placeholder stays — the page never breaks.
Add them one at a time as you record.

### Encoding the clips

The clips are **silent** — there is no sound control on the page, so strip the audio
when you encode. That also makes the files considerably smaller.

GitHub has a **100 MB hard limit per file** and warns above 50 MB. Aim for 15–30 seconds
at 1280×720, which lands around 5–15 MB each.

```bash
ffmpeg -i raw-recording.mp4 -t 30 -vf "scale=1280:-2,fps=30" \
  -c:v libx264 -crf 26 -preset slow -an -movflags +faststart videos/step-01.mp4
```

- `-an` — strips the audio track (required, the page plays muted)
- `-t 30` — trims to the first 30 seconds; drop it to keep the whole recording
- `-movflags +faststart` — lets the browser start playing before the full download

Batch the whole folder:

```bash
for f in raw/*.mp4; do
  ffmpeg -i "$f" -vf "scale=1280:-2,fps=30" -c:v libx264 -crf 26 -preset slow \
    -an -movflags +faststart "videos/$(basename "$f")"
done
```

> If a clip ends up over 100 MB, shorten it or raise `-crf` — GitHub will reject the push otherwise.

---

## Playback behaviour

- Clips autoplay when they scroll past 55% visible, and pause once they drop below 25%.
  That gap stops the flicker while a phone is being scrolled.
- Everything is muted and looping — the clips carry no audio.
- Everything pauses when the browser tab goes to the background.
- Honours `prefers-reduced-motion`.

---

## Previewing locally

Relative paths need a server — double-clicking `index.html` will not load `videos/` or `assets/`.

```bash
python -m http.server 8777
```

Then open `http://127.0.0.1:8777`.

> Until all 12 clips are in place you will see 404s in the browser console — one per missing
> file. That is how the page detects what exists; it is not an error.

---

## Editing the content

Everything is in `index.html` — content and styles in one file.

- **Colours:** the `:root` block at the top of the `<style>` tag.
- **Steps:** the `<article class="step">` blocks in the `#workflow` section.
- **Chart:** the `data-w` attribute on each `.fill` is the bar width as a percentage
  of the top video. Update the numbers when you re-check performance.
- **Thumbnail:** `assets/thumbnail.jpg`, stored locally so the page does not depend
  on YouTube's CDN.
