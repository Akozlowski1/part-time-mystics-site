# parttimemystics.com

Static site for Part Time Mystics (Portland, Oregon).

- `public/` — what is published. `index.html`, `img/`, `CNAME`.
- `src/` — source. `template.html` is edited by hand; `build.py` regenerates
  `index.html` (deployable) and `preview.html` (private preview, images inlined).

To change the site: edit `src/template.html`, run `python3 src/build.py`, copy the
generated `index.html` into `public/`, commit and push. Pushing to `main` deploys
via GitHub Actions.
