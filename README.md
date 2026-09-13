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

## Filling the 12 slots

Every step has an empty slot. **Screenshots are the easy path** — no editing, no
encoding, no waiting. Drop a file in and it appears; no code change needed.

```
images/step-01.png    Rough cut
images/step-02.png    Remove silence
images/step-03.png    Colour correction & grading
images/step-04.png    Download b-roll
images/step-05.png    Motion graphics
images/step-06.png    Lay in b-roll & effects
images/step-07.png    Refine clip by clip
images/step-08.png    Music & ducking
images/step-09.png    Rewatch & export
images/step-10.png    Upload & package
images/step-11.png    Thumbnail
images/step-12.png    Blog post
```

`.jpg` works too — the page checks for `.png` first, then `.jpg`.

Screenshots are shown whole, never cropped, and **tapping one opens it full
screen**, because editing UI is unreadable at phone width.

If a slot has no file, the striped blue placeholder stays and the page carries
on. Add them one at a time.

### Taking the screenshots

**Win + Shift + S** captures a region straight to the clipboard, then paste and
save. Anything that produces a PNG or JPG is fine.

Grab the part of the screen that makes the point — the timeline, the effect
panel, the export dialog — not the whole desktop. A tighter shot reads better
on a phone.

> The page is public. Check each shot for file paths, client names and anything
> else you would not want a stranger reading.

### If a PNG gets large

Screenshots of dense UI can run several MB. Anything over about 500 KB is worth
shrinking:

```bash
ffmpeg -i images/step-01.png -vf "scale='min(1600,iw)':-2" -q:v 4 images/step-01.jpg
```

Then delete the PNG — the page prefers PNG, so leaving both means the big one wins.

### Video instead (optional)

A slot with no screenshot falls back to `videos/step-NN.mp4` if one is there.
Clips autoplay muted when scrolled into view and must be silent:

```bash
ffmpeg -i raw-recording.mp4 -t 30 -vf "scale=1280:-2,fps=30"   -c:v libx264 -crf 26 -preset slow -an -movflags +faststart videos/step-01.mp4
```

GitHub blocks any file over **100 MB** and warns above 50 MB, so keep clips to
15-30 seconds.

---

## Playback behaviour

- Screenshots load as soon as the page does, shown whole and never cropped.
  Tapping one opens it full screen; Escape or a tap anywhere closes it.
- Clips (if you use any) autoplay when they scroll past 55% visible and pause
  once they drop below 25%. That gap stops the flicker while a phone is scrolled.
- Clips are muted and looping, and carry no audio.
- Playback stops when the tab goes to the background and resumes on return.
- Honours `prefers-reduced-motion`.

---

## Previewing locally

Relative paths need a server. Double-clicking `index.html` will not load `images/`,
`videos/` or `assets/`.

```bash
python -m http.server 8777
```

Then open `http://127.0.0.1:8777`.

> Until all 12 slots are filled you will see 404s in the browser console, a few per
> empty slot. That is how the page detects what exists; it is not an error.

---

## Editing the content

Everything is in `index.html` — content and styles in one file.

- **Colours:** the `:root` block at the top of the `<style>` tag.
- **Steps:** the `<article class="step">` blocks in the `#workflow` section.
- **Chart:** the `data-w` attribute on each `.fill` is the bar width as a percentage
  of the top video. Update the numbers when you re-check performance.
- **Thumbnail:** `assets/thumbnail.jpg`, stored locally so the page does not depend
  on YouTube's CDN.
