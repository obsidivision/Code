# DSA Practice Hub

A static study site that pairs a Korean high-school **정보/정보과학 (Informatics)** syllabus with
English-language practice problems from LeetCode, Baekjoon and GeeksforGeeks.

Every page is written in **both Korean and English**, with Korean as the default; the `EN / 한국어`
button in the header switches the whole site and the choice is remembered.

Each unit gives you three things:

1. a short concept refresher written in plain language,
2. a clean, commented Python reference implementation, and
3. a curated Easy → Medium → Hard problem list with per-problem checkboxes.

## Live site

**https://obsidivision.github.io/code/**

> If the link 404s, GitHub Pages has not been switched on yet — see [Deploying](#deploying) below.

## Units

| # | Topic | Covers |
|---|-------|--------|
| 01 | Sorting · 정렬 *(hidden — not on this semester's syllabus)* | Bubble sort, selection sort, an interactive pass-by-pass tracer, stability and swap counts, insertion/quick sort preview |
| 02 | Queue · 큐 | Why linear array queues waste space, circular queues with modulo indices, the sacrificial empty slot, ring buffers |
| 03 | Linked List · 연결 리스트 | Nodes and links, array trade-offs, singly/circular/doubly, stack on a list, circular queue from a tail pointer, middle insert/delete |
| 04 | Graph · 그래프 | Königsberg, `G = (V, E)`, set notation, the four directed/weighted combinations, degree and paths, adjacency matrix vs. adjacency list |
| 05 | Tree · 트리 | Binary trees, full/complete/skewed, array vs. linked representation, pre/in/post-order, expression trees, BST search/insert/delete |

## Hiding a unit

Sorting is not on the syllabus this semester, so it is hidden. Its entry in `TOPICS`
(`assets/app.js`) carries `hidden: true`, which drops it from the top nav, the home-page unit grid,
the random-problem pool and the overall progress totals. The page itself still works at
`sorting.html` and shows a banner explaining why it is not in the menu — nothing was deleted.

To bring it back, set `hidden: false` in `assets/app.js`, flip the last field of its row in the
`TOPICS` list in `tools/_common.py` (the nav is baked into the static HTML), and re-run
`python3 tools/build.py`. Both lists are one line each.

## Features

- **Korean / English toggle** — prose is authored twice, inside `[data-lang="ko"]` and
  `[data-lang="en"]` spans, and CSS shows only the active one; anything rendered by JS is rebuilt on
  switch. Korean is the default, and the choice persists in `localStorage`. Problem titles always
  stay in English so they can be found on the judge; code comments are English in both modes.
- **Progress tracking** — every problem has a checkbox stored in `localStorage`, rolling up into per-unit
  progress bars, progress rings on the home page, and an overall summary. Nothing is uploaded anywhere.
- **Dark / light theme** with the choice remembered between visits (dark is the default).
- **Interactive sort tracer** — step or play through bubble and selection sort on any array you type in,
  with comparisons, swaps and locked positions colour-coded.
- **Filtering** — search problems by title, hint or judge, and filter by difficulty.
- **🎲 Random unsolved problem** button, per unit or across the whole site.
- **Syntax-highlighted Python** via Prism.js, with copy buttons.
- Responsive down to phone widths; respects `prefers-reduced-motion`.

## Running locally

No build step, no dependencies. Either open `index.html` directly, or serve the folder:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## How the content is organised

```
index.html            hero, unit grid with progress rings, overall progress summary
sorting.html          ┐
queue.html            │
linked-list.html      ├─ one page per unit: concept → reference code → practice list → next unit
graph.html            │
tree.html             ┘
assets/styles.css     all styling: theme tokens, gradients, cards, widgets, language switching
assets/app.js         topic + problem data, UI strings, localStorage progress, filtering,
                      theme + language toggles, sort tracer
tools/                authoring scripts that regenerate the HTML (not needed to serve the site)
.nojekyll             tells GitHub Pages to serve the files as-is
```

### Editing the pages

The HTML is generated, because each page carries its prose twice (Korean and English) on top of
shared chrome. Edit the module for the page in `tools/`, then:

```bash
python3 tools/build.py      # rewrites all six .html files in place
```

`tools/_common.py` holds `TOPICS`, the `L(ko, en)` bilingual helper and the shared head/nav/footer;
`tools/page_*.py` holds one page each. There is no build step for *serving* the site — the committed
HTML is what GitHub Pages hands out.

`assets/app.js` is the single source of truth for content lists. The `TOPICS` array defines the units
(including the `hidden` flag) and the `PROBLEMS` object holds every problem (`num`, `title`, `diff`,
`hintEn`, `hintKo`, `url`, `src`). Topic pages render their own list from it at load time, so **adding a
problem means editing one array** — the progress bars, filters and random-problem button pick it up
automatically. `STR` holds the Korean and English UI strings.

All asset paths are relative (`assets/styles.css`, not `/assets/styles.css`), so the site works both at a
repository sub-path like `user.github.io/code/` and at a custom domain root.

## Deploying

GitHub Pages, straight from the branch — no workflow needed:

1. **Settings → Pages**
2. **Source:** *Deploy from a branch*
3. **Branch:** `main` (or whichever branch holds these files) · **Folder:** `/ (root)`
4. Save, wait for the first build, then open the URL above.

## A note on sources

Concept explanations, diagrams, exercises and code on this site are written from scratch. No text, image,
diagram or example from any class material is reproduced. The algorithms themselves (bubble sort, circular
queues, binary search trees…) are standard curriculum. Linked practice problems belong to their respective
judges and are only referenced by title and URL.
