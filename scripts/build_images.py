"""
Turn the raw screenshots into consistent 16:9 cards for the site.

Per image:
  1. trim flat white/black dead borders (one shot was 45% empty page)
  2. scale the real content as large as it will go inside the frame
  3. fill the leftover with a blurred, darkened copy of the shot itself,
     so a square or ultra-wide grab still reads as a finished card
"""
import os, glob
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

SRC = r"C:\Users\ACER NITRO-Pc\Desktop\1 Testing\photos"
DST = r"C:\Users\ACER NITRO-Pc\Desktop\1 Testing\editing pattern\site\images"

W, H = 1920, 1080          # card size
PAD = 42                   # breathing room around the content
FG_W, FG_H = W - PAD * 2, H - PAD * 2


def dead(line):
    return line.std() < 4.0 and (line.mean() > 238 or line.mean() < 18)


def content_box(im):
    a = np.asarray(im.convert("L"), dtype=np.float32)
    h, w = a.shape
    top = 0
    while top < h - 1 and dead(a[top]):
        top += 1
    bot = h - 1
    while bot > top and dead(a[bot]):
        bot -= 1
    left = 0
    while left < w - 1 and dead(a[:, left]):
        left += 1
    right = w - 1
    while right > left and dead(a[:, right]):
        right -= 1
    return (left, top, right + 1, bot + 1)


def fit(im, bw, bh):
    r = min(bw / im.width, bh / im.height)
    return im.resize((max(1, int(round(im.width * r))),
                      max(1, int(round(im.height * r)))), Image.LANCZOS)


def cover(im, bw, bh):
    r = max(bw / im.width, bh / im.height)
    big = im.resize((int(round(im.width * r)), int(round(im.height * r))), Image.LANCZOS)
    x = (big.width - bw) // 2
    y = (big.height - bh) // 2
    return big.crop((x, y, x + bw, y + bh))


def build(path, out):
    im = Image.open(path).convert("RGB")
    ow, oh = im.size

    box = content_box(im)
    im = im.crop(box)
    tw, th = im.size

    # background: the shot itself, blown up, blurred, pushed back
    bg = cover(im, W, H).filter(ImageFilter.GaussianBlur(38))
    bg = ImageEnhance.Brightness(bg).enhance(0.52)
    bg = ImageEnhance.Color(bg).enhance(0.55)

    fg = fit(im, FG_W, FG_H)
    x = (W - fg.width) // 2
    y = (H - fg.height) // 2

    # hairline so the shot separates from the blur behind it
    edge = Image.new("RGB", (fg.width + 2, fg.height + 2), (255, 255, 255))
    bg.paste(edge, (x - 1, y - 1))
    bg.paste(fg, (x, y))

    bg.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    return ow, oh, tw, th, fg.width, fg.height, os.path.getsize(out)


if not os.path.isdir(DST):
    os.makedirs(DST)

files = sorted(glob.glob(os.path.join(SRC, "*.png")),
               key=lambda x: int(os.path.basename(x).split()[0]))

print("%-22s %-11s %-11s %-11s %-6s %s" %
      ("source", "original", "trimmed", "placed", "fill%", "output"))
total = 0
for p in files:
    n = int(os.path.basename(p).split()[0])
    out = os.path.join(DST, "step-%02d.jpg" % n)
    ow, oh, tw, th, fw, fh, size = build(p, out)
    total += size
    fill = 100.0 * (fw * fh) / (W * H)
    print("%-22s %-11s %-11s %-11s %-6s %s (%d KB)" % (
        os.path.basename(p), "%dx%d" % (ow, oh), "%dx%d" % (tw, th),
        "%dx%d" % (fw, fh), "%.0f%%" % fill,
        os.path.basename(out), size // 1024))

print("\n%d images, %.1f MB total" % (len(files), total / 1024.0 / 1024.0))
