# Rohan Dubey — Data & Systems Engineering

A responsive, static portfolio for GitHub Pages. Built with HTML, CSS, and a small amount of JavaScript; no package installation or build step is required.

## Local preview

```sh
python3 -m http.server 8000
```

Open http://localhost:8000.

## Files

- `index.html` — portfolio, career history, project links, and metadata.
- `styles.css` — charcoal, ivory, and muted gold visual design; responsive layouts and reduced-motion support.
- `script.js` — mobile navigation, keyboard-accessible architecture tabs, active navigation, and progressive reveal animations.
- `assets/fonts/` — self-hosted Manrope and Instrument Serif, with their SIL Open Font Licenses.
- `assets/github/` — checked-in GitHub statistics, language, streak, and activity SVGs.
- `scripts/refresh-github-widgets.py` — validates and refreshes the GitHub SVGs, preserving existing images if a source fails.
- `.github/workflows/refresh-github-widgets.yml` — daily and manually triggered widget updates using the repository's built-in token.
- `favicon.svg`, `og.png` — browser and social sharing artwork.
- `Rohan_Resume.pdf` — downloadable résumé.
- `.nojekyll` — bypasses Jekyll processing.

## Widget refresh

The page loads its fonts and images from this repository. Stats, languages, and streak cards are validated snapshots from the corresponding widget services; the 31-day activity graph is rendered directly from GitHub's contribution calendar. A failed refresh retains the most recent working image and reports the failure in Actions.

To refresh locally with an authenticated [GitHub CLI](https://cli.github.com/):

```sh
python3 scripts/refresh-github-widgets.py
```

The scheduled workflow becomes active after it is pushed to `main`. It can also be run from the repository's Actions tab. Branch protection rules must permit the bot's asset commits for automatic updates to reach the site.

## GitHub Pages

In repository **Settings → Pages**, choose **Deploy from a branch**, select `main`, and select the root folder. The site is served from https://rohankumardubey.github.io/.

Career content and project descriptions preserve the information from the existing portfolio.
