# Pengcheng Xie Website

Personal academic website generated with `jemdoc`.

## Build

Run all page builds from the repository root:

```bash
./build.sh
```

This regenerates:

- `index.html`
- `research.html`
- `research-highlights.html`
- `publication.html`
- `talks.html`
- `mentorship.html`
- `codes.html`
- `blog.html`
- `album.html`

## Local Preview

Start a local static server:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/
```

## Notes

- Keep `xpcpublication.bib` in the repository root; the publications page loads it through BibBase.
- The menu label is `Software`, while the generated page remains `codes.html` for link stability.
- Research Highlights is linked from Research and Publications. Edit `research-highlights.jemdoc` to update its six papers and contribution statements; its scoped styling and mobile layout live in `research-highlights.css` and `research-highlights.conf`.
- To rebuild only the highlights page, run `python3 jemdoc.py -c research-highlights.conf research-highlights.jemdoc`. Paper section IDs are stable links for sharing individual highlights.
