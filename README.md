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

## The 12 slots

All twelve are filled with screenshots, built from the raw grabs in
`Desktop/1 Testing/photos` and stored here as `images/step-01.jpg` ... `step-12.jpg`.

Each one is a 1920x1080 card: the screenshot is trimmed of dead white or black
border, scaled as large as it will go, and the leftover space filled with a
blurred, darkened copy of the shot itself. That keeps every card the same shape
whether the source was ultra-wide (the Envato grab is 2.8:1) or nearly square
(two of the Premiere grabs are 1:1), without ever cropping the content.

Screenshots are shown whole and **tapping one opens it full screen**, because
editing UI is unreadable at phone width.

Total 2.7 MB across twelve images, lazy-loaded, so only what you scroll past
is downloaded.

### Replacing one

Drop a new file at `images/step-NN.jpg` (or `.png` — the page checks `.jpg`
first, then `.png`) and push. If a slot has no file at all, the striped blue
placeholder stays and the page carries on.

To rebuild a card from a fresh grab with the same trim-and-fill treatment:

```bash
python scripts/build_images.py
```

That reads every `N description.png` in the photos folder, uses the leading
number as the step number, and writes the cards into `images/`.

> The page is public. Check each shot for file paths, client names and anything
> else you would not want a stranger reading.

### Video instead (optional)

A slot with no screenshot falls back to `videos/step-NN.mp4`. Clips autoplay
muted when scrolled into view and must be silent:

```bash
ffmpeg -i raw-recording.mp4 -t 30 -vf "scale=1280:-2,fps=30"   -c:v libx264 -crf 26 -preset slow -an -movflags +faststart videos/step-01.mp4
```

GitHub blocks any file over **100 MB** and warns above 50 MB, so keep clips to
15-30 seconds.

---

## Playback behavior

- Screenshots load as soon as the page does, shown whole and never cropped.
  Tapping one opens it full screen; Escape or a tap anywhere closes it.
- Clips (if you use any) autoplay when they scroll past 55% visible and pause
  once they drop below 25%. That gap stops the flicker while a phone is scrolled.
- Clips are muted and looping, and carry no audio.
- Playback stops when the tab goes to the background and resumes on return.
- Honors `prefers-reduced-motion`.

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

- **Colors:** the `:root` block at the top of the `<style>` tag.
- **Steps:** the `<article class="step">` blocks in the `#workflow` section.
- **Chart:** the `data-w` attribute on each `.fill` is the bar width as a percentage
  of the top video. Update the numbers when you re-check performance.
- **Thumbnail:** `assets/thumbnail.jpg`, stored locally so the page does not depend
  on YouTube's CDN.
