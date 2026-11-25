#!/usr/bin/env python3
"""Makes the talk transcripts in _transcripts/ from the videos in the program.

Run it from the repository root. The steps can be run one by one and every
step skips work that is already done, so it is safe to stop and restart.

  python _tools/transcripts/transcripts.py list                 # videos in _data/program
  python _tools/transcripts/transcripts.py fetch                # download the audio
  python _tools/transcripts/transcripts.py transcribe [threads] # Whisper, slow on a CPU
  python _tools/transcripts/transcripts.py check                # find broken transcripts
  python _tools/transcripts/transcripts.py build                # write _transcripts/YYYY/*.html

`--year 2026` limits any step to one edition.

Audio and raw Whisper output go to _tools/transcripts/work/ (not in git).
Fixes for names and technical terms go into corrections/<video id>.json as a
list of {"from": "...", "to": "..."} pairs. `build` applies them to the text
and warns when a "from" text is not found.

Needs ffmpeg and Google Chrome, plus `pip install -r requirements.txt`.
"""
import argparse, glob, html, json, os, re, subprocess, sys, time, urllib.request

import yaml

ROOT = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
MODEL = "large-v3-turbo"
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")


# ---------------------------------------------------------------- list

def video_id(url):
    m = re.search(r"youtu\.be/([\w-]{11})|[?&]v=([\w-]{11})", url)
    if m:
        return m.group(1) or m.group(2)
    m = re.search(r"/(1_[a-z0-9]{8})", url)  # UCSD MediaSpace (Kaltura)
    return m.group(1) if m else None


def videos(year=None):
    """Every video in _data/program, with what the transcript page needs."""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "_data", "program", "y*.yml"))):
        y = int(re.search(r"y(\d{4})", f).group(1))
        if year and y != year:
            continue
        d = yaml.safe_load(open(f, encoding="utf-8"))

        def add(kind, e, url, title):
            if not str(url or "").startswith("http"):
                return
            out.append({"year": y, "kind": kind, "url": url, "id": video_id(url),
                        "title": " ".join(str(title).split()),
                        "author-list": e.get("author-list"), "authors": e.get("authors"),
                        "pdf": e.get("pdf") or None})

        for k in ("keynote", "keynote2"):
            if isinstance(d.get(k), dict):
                add(k, d[k], d[k].get("video"), d[k].get("title"))
        for e in d.get("papers") or []:
            add("paper", e, e.get("video"), e.get("title"))
        for e in d.get("sessions") or []:
            add("session", e, e.get("video"), e.get("title"))
            add("qa", {}, e.get("qa_video"), f"Q&A of session {e.get('id')}: {e.get('title')}")
    return out


# ---------------------------------------------------------------- fetch

def audio_file(vid):
    hits = [f for f in glob.glob(os.path.join(WORK, "audio", vid + ".*")) if f.endswith((".webm", ".m4a"))]
    return hits[0] if hits else None


def kaltura_stream(page):
    """yt-dlp cannot read UCSD MediaSpace, so press play in Chrome and take the HLS URL."""
    from playwright.sync_api import sync_playwright
    seen = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        pg.on("request", lambda r: seen.append(r.url))
        pg.goto(page, wait_until="networkidle", timeout=90000)
        pg.wait_for_timeout(2000)
        pg.mouse.click(640, 400)
        for _ in range(20):
            pg.wait_for_timeout(1000)
            if any("serveFlavor" in u and "index.m3u8" in u for u in seen):
                break
        b.close()
    return next((u for u in seen if "serveFlavor" in u and "index.m3u8" in u), None)


def fetch(items):
    os.makedirs(os.path.join(WORK, "audio"), exist_ok=True)
    for it in items:
        if audio_file(it["id"]):
            continue
        base = os.path.join(WORK, "audio", it["id"])
        print("fetch", it["year"], it["id"], it["title"][:60], flush=True)
        if "youtu" in it["url"]:
            # Some formats answer 403, so try the next one until a file is there.
            for fmt in ("worstaudio[acodec=opus]", "bestaudio[acodec=opus]", "bestaudio"):
                subprocess.run(["yt-dlp", "-q", "--no-warnings", "-f", fmt, "-o", base + ".%(ext)s", it["url"]])
                if audio_file(it["id"]):
                    break
        else:
            hls = kaltura_stream(it["url"])
            if hls:
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", hls, "-vn", "-c:a", "copy", base + ".m4a"])
        if not audio_file(it["id"]):
            print("  FAILED", it["url"], flush=True)


# ---------------------------------------------------------------- transcribe

# Without a prompt, Whisper sometimes falls into a mode with no capitals, no
# punctuation and every "uh" kept, for a whole talk. A short punctuated
# example sentence keeps it in normal written text.
PROMPT = "Hello, and welcome to my talk. Today, I will present our work."


def transcribe(items, threads, redo=()):
    import numpy as np
    from faster_whisper import WhisperModel
    os.makedirs(os.path.join(WORK, "raw"), exist_ok=True)
    todo = [it for it in items if audio_file(it["id"])
            and (it["id"] in redo or not os.path.exists(raw_file(it["id"])))]
    if not todo:
        return
    model = WhisperModel(MODEL, device="cpu", compute_type="int8", cpu_threads=threads)
    for it in todo:
        t0 = time.time()
        pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", audio_file(it["id"]), "-ac", "1", "-ar", "16000",
                              "-f", "f32le", "-"], capture_output=True, check=True).stdout
        segments, info = model.transcribe(np.frombuffer(pcm, dtype=np.float32), language="en",
                                          beam_size=5, vad_filter=True, initial_prompt=PROMPT)
        segs = [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()} for s in segments]
        with open(raw_file(it["id"]) + ".tmp", "w") as f:
            json.dump({"id": it["id"], "model": MODEL, "duration": round(info.duration, 1), "segments": segs}, f)
        os.replace(raw_file(it["id"]) + ".tmp", raw_file(it["id"]))
        print(f"{it['year']} {it['id']}: {info.duration / 60:.1f} min in {(time.time() - t0) / 60:.1f} min", flush=True)


def raw_file(vid):
    return os.path.join(WORK, "raw", vid + ".json")


def check(items):
    """Lists transcripts that look broken: hardly any punctuation, or one line repeated."""
    bad = []
    for it in items:
        if not os.path.exists(raw_file(it["id"])):
            continue
        segs = [s["text"] for s in json.load(open(raw_file(it["id"]), encoding="utf-8"))["segments"]]
        text = " ".join(segs)
        words = max(len(text.split()), 1)
        punct = len(re.findall(r"[.?!,]", text)) / words
        top = max((segs.count(s) for s in set(segs) if len(s) > 15), default=0)
        if punct < 0.05 or top >= 4:
            bad.append(it["id"])
            print(f"{it['year']} {it['id']:12} punctuation per word {punct:.3f}, most repeated line {top}x  {it['title'][:50]}")
    if bad:
        print("\nRedo with: transcribe --redo=" + ",".join(bad))


# ---------------------------------------------------------------- build

def paragraphs(segments):
    """Groups Whisper segments into paragraphs at pauses and sentence ends."""
    paras, cur, words, last_end = [], [], 0, None
    for s in segments:
        if not s["text"]:
            continue
        gap = s["start"] - last_end if last_end is not None else 0
        ends_sentence = bool(cur) and cur[-1]["text"].rstrip().endswith((".", "?", "!"))
        if cur and ((gap >= 1.5 and words >= 40) or (words >= 130 and ends_sentence) or words >= 220):
            paras.append(cur)
            cur, words = [], 0
        cur.append(s)
        words += len(s["text"].split())
        last_end = s["end"]
    if cur:
        paras.append(cur)
    return [(p[0]["start"], " ".join(s["text"] for s in p)) for p in paras]


def stamp(sec):
    sec = int(sec)
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def slugify(title, taken):
    words = re.sub(r"[^a-z0-9]+", " ", title.lower()).split()
    slug = "-".join(words[:6]) or "talk"
    base, n = slug, 2
    while slug in taken:
        slug, n = f"{base}-{n}", n + 1
    taken.add(slug)
    return slug


def apply_corrections(vid, paras):
    path = os.path.join(HERE, "corrections", vid + ".json")
    if not os.path.exists(path):
        return paras, 0
    fixes = json.load(open(path, encoding="utf-8"))
    out, done = list(paras), 0
    for fx in fixes:
        hit = False
        for i, (t, text) in enumerate(out):
            if fx["from"] in text:
                out[i] = (t, text.replace(fx["from"], fx["to"]))
                hit = True
        if hit:
            done += 1
        else:
            print(f"  {vid}: correction not found: {fx['from']!r}", flush=True)
    return out, done


def front_matter(d):
    lines = ["---"]
    for k, v in d.items():
        if v is not None:
            lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    return "\n".join(lines + ["---", ""])


def build(items):
    taken = {}
    for it in items:
        raw = raw_file(it["id"])
        if not os.path.exists(raw):
            continue
        data = json.load(open(raw, encoding="utf-8"))
        # Whisper sometimes invents text after the audio has ended
        # ("Thank you." or worse), so segments past the end are dropped.
        segs = [s for s in data["segments"] if s["start"] < data["duration"] - 0.5]
        paras, fixed = apply_corrections(it["id"], paragraphs(segs))
        slug = slugify(it["title"], taken.setdefault(it["year"], set()))
        youtube = "youtu" in it["url"]
        body = []
        for start, text in paras:
            ts = stamp(start)
            if youtube:
                ts = f'<a class="ts" href="https://www.youtube.com/watch?v={it["id"]}&amp;t={int(start)}s" target="_blank" rel="noopener">{ts}</a>'
            else:
                ts = f'<span class="ts">{ts}</span>'
            body.append(f"<p>{ts} {html.escape(text, quote=False)}</p>")
        fm = front_matter({
            "title": it["title"], "edition": it["year"], "section": "transcript",
            "permalink": f"/{it['year']}/transcripts/{slug}/", "video": it["url"],
            "pdf": it["pdf"], "author-list": it["author-list"], "authors": it["authors"],
            "model": data["model"], "duration": stamp(data["duration"]),
        })
        os.makedirs(os.path.join(ROOT, "_transcripts", str(it["year"])), exist_ok=True)
        out = os.path.join(ROOT, "_transcripts", str(it["year"]), slug + ".html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(fm + "\n".join(body) + "\n")
        # Plain text with paragraphs, the input for writing corrections.
        os.makedirs(os.path.join(WORK, "text"), exist_ok=True)
        with open(os.path.join(WORK, "text", it["id"] + ".txt"), "w", encoding="utf-8") as f:
            f.write("\n\n".join(t for _, t in paras) + "\n")
        print(f"{os.path.relpath(out, ROOT)}  ({len(paras)} paragraphs, {fixed} corrections)")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["list", "fetch", "transcribe", "check", "build"])
    ap.add_argument("threads", nargs="?", type=int, default=12)
    ap.add_argument("--year", type=int)
    ap.add_argument("--redo", default="", help="comma separated video ids to transcribe again")
    a = ap.parse_args()
    items = videos(a.year)
    if a.step == "list":
        for it in items:
            state = "transcribed" if os.path.exists(raw_file(it["id"])) else "audio" if audio_file(it["id"]) else "-"
            print(f"{it['year']}  {it['kind']:8} {it['id']:12} {state:12} {it['title'][:70]}")
    elif a.step == "fetch":
        fetch(items)
    elif a.step == "transcribe":
        transcribe(items, a.threads, set(filter(None, a.redo.split(","))))
    elif a.step == "check":
        check(items)
    else:
        build(items)


if __name__ == "__main__":
    main()
