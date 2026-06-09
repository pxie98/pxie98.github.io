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
