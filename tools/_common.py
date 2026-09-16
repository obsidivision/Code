# -*- coding: utf-8 -*-
"""Authoring helper: emits the static HTML pages for DSA Practice Hub.

Every page carries both languages: prose is wrapped in
<span data-lang="ko"> / <span data-lang="en"> and CSS hides the inactive one.
Korean is the default. Topics flagged hidden=True keep their page but drop
out of the nav (mirrors the `hidden` flag in assets/app.js).
"""
import html, os, textwrap

# repo root, one level up from tools/
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# id, file, ko, en, icon, step_ko, step_en, hidden
TOPICS = [
    ("sorting",     "sorting.html",     "정렬",        "Sorting",     "⇅",  "1단원", "Unit 01", True),
    ("queue",       "queue.html",       "큐",          "Queue",       "◷",  "2단원", "Unit 02", False),
    ("linked-list", "linked-list.html", "연결 리스트", "Linked List", "⛓",  "3단원", "Unit 03", False),
    ("graph",       "graph.html",       "그래프",      "Graph",       "◈",  "4단원", "Unit 04", False),
    ("tree",        "tree.html",        "트리",        "Tree",        "🌲", "5단원", "Unit 05", False),
]

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
           "%3Crect width='100' height='100' rx='24' fill='%238b5cf6'/%3E%3Ctext x='50' y='70' "
           "font-size='56' text-anchor='middle' fill='white' font-family='sans-serif' "
           "font-weight='bold'%3EDS%3C/text%3E%3C/svg%3E")

CDN = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0"


def L(ko, en):
    """One phrase in both languages; CSS shows whichever is active."""
    return '<span data-lang="ko">%s</span><span data-lang="en">%s</span>' % (ko, en)


def head(title, desc, topic=None):
    nav = "\n".join(
        '        <a href="{f}"{cur}>{label}</a>'.format(
            f=f, label=L(ko, en), cur=' aria-current="page"' if tid == topic else "")
        for tid, f, ko, en, _i, _sk, _se, hidden in TOPICS if not hidden)
    body_attr = ' data-topic="{}"'.format(topic) if topic else ""
    return """<!DOCTYPE html>
<html lang="ko" data-theme="dark" data-lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="dark light">
<link rel="icon" href="{favicon}">
<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
<link rel="stylesheet" href="assets/styles.css">
<script>
try {{
  var d = document.documentElement;
  d.setAttribute('data-theme', localStorage.getItem('dsa-hub:theme') || 'dark');
  var l = localStorage.getItem('dsa-hub:lang') || 'ko';
  d.setAttribute('data-lang', l);
  d.setAttribute('lang', l);
}} catch (e) {{}}
</script>
</head>
<body{body_attr}>
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#8b5cf6"/><stop offset="100%" stop-color="#ec4899"/></linearGradient>
</defs></svg>

<header class="nav">
  <div class="nav-inner">
    <a class="brand" href="index.html">
      <span class="brand-mark">DS</span><span class="brand-text">{brand}</span>
    </a>
    <nav class="nav-links" aria-label="{navlabel}">
{nav}
    </nav>
    <button class="lang-toggle" data-lang-toggle type="button" aria-label="언어 전환 / Switch language">EN</button>
    <button class="theme-toggle" data-theme-toggle type="button" aria-label="테마 전환 / Toggle theme">☀</button>
  </div>
</header>
""".format(title=html.escape(title), desc=html.escape(desc), favicon=FAVICON,
           nav=nav, body_attr=body_attr,
           brand=L("DSA 연습 허브", "DSA Practice Hub"),
           navlabel="단원 / Topics")


def foot():
    return """
<footer>
  <div class="wrap">
    <p style="margin:0 0 .4rem">""" + L(
        "<strong>DSA 연습 허브</strong> — 1년 과정 정보/정보과학 수업을 위한 개인 학습 사이트입니다. "
        "여기 있는 설명·그림·코드는 모두 새로 작성한 것이며, 수업 자료를 그대로 옮긴 부분은 없습니다.",
        "<strong>DSA Practice Hub</strong> — a personal study site for a year-long 정보/정보과학 course. "
        "All explanations, diagrams and code here are written from scratch; no class material is reproduced.") + """
    </p>
    <p style="margin:0">""" + L(
        '문제 링크는 <a href="https://leetcode.com/" target="_blank" rel="noopener">LeetCode</a>, '
        '<a href="https://www.acmicpc.net/" target="_blank" rel="noopener">백준</a>, '
        '<a href="https://www.geeksforgeeks.org/" target="_blank" rel="noopener">GeeksforGeeks</a>로 연결됩니다. '
        '각 문제의 저작권은 해당 저지에 있습니다. 진행 상황은 이 브라우저에만 저장됩니다.',
        'Problem links point to <a href="https://leetcode.com/" target="_blank" rel="noopener">LeetCode</a>, '
        '<a href="https://www.acmicpc.net/" target="_blank" rel="noopener">Baekjoon</a> and '
        '<a href="https://www.geeksforgeeks.org/" target="_blank" rel="noopener">GeeksforGeeks</a>; '
        'those problems belong to their respective judges. Progress is stored only in this browser.') + """
    </p>
  </div>
</footer>

<script src="{cdn}/prism.min.js"></script>
<script src="{cdn}/components/prism-python.min.js"></script>
<script src="assets/app.js"></script>
</body>
</html>
""".format(cdn=CDN)


def code(filename, source, lang="python"):
    return """<div class="code-card">
  <div class="code-head"><span>{name}</span><button class="copy-btn" type="button">복사</button></div>
  <pre class="language-{lang}"><code class="language-{lang}">{src}</code></pre>
</div>""".format(name=html.escape(filename), lang=lang,
                 src=html.escape(textwrap.dedent(source).strip("\n")))


def page_head(tid, tagline_ko, tagline_en, banner=""):
    meta = [t for t in TOPICS if t[0] == tid][0]
    _id, _f, ko, en, icon, step_ko, step_en, _h = meta
    return """<main class="wrap">
<div class="page-head" style="--grad: var(--grad-{tid}); --c-accent: var(--c-{tid})">
  <div class="topic-icon">{icon}</div>
  <div class="topic-step" style="margin-top:.9rem">{step}</div>
  <h1>{title}</h1>
  <p class="lead" style="max-width:62ch">{tagline}</p>
  {banner}
</div>
""".format(tid=tid, icon=icon, step=L(step_ko, step_en),
           title=L('%s <span class="ko">%s</span>' % (ko, en),
                   '%s <span class="ko">%s</span>' % (en, ko)),
           tagline=L(tagline_ko, tagline_en), banner=banner)


def practice_section(tid, blurb_ko, blurb_en):
    return """<section id="practice" style="--grad: var(--grad-{tid})">
  <h2 class="section-title">{heading}</h2>
  <p>{blurb}</p>

  <div class="card topic-progress" data-progress-topic="{tid}" style="--grad: var(--grad-{tid})">
    <div class="pbar"><span></span></div>
    <div class="pnum">0 / 0</div>
  </div>

  <div class="filters">
    <input class="search" id="problem-search" type="search" placeholder="제목·힌트·저지로 검색…" aria-label="문제 검색">
    <button class="chip" type="button" data-diff="all" aria-pressed="true">전체</button>
    <button class="chip" type="button" data-diff="easy" aria-pressed="false">쉬움</button>
    <button class="chip" type="button" data-diff="medium" aria-pressed="false">보통</button>
    <button class="chip" type="button" data-diff="hard" aria-pressed="false">어려움</button>
    <button class="chip" type="button" id="random-problem" data-topic="{tid}">🎲 안 푼 문제 랜덤</button>
  </div>

  <ul class="plist" id="problem-list"></ul>
  <p class="empty" id="problem-empty" style="display:none">조건에 맞는 문제가 없습니다.</p>
  <p style="font-size:.84rem;color:var(--text-faint);margin-top:1rem">{footnote}</p>
</section>
""".format(
        tid=tid,
        heading=L("연습 문제", "Practice problems"),
        blurb=L(blurb_ko + " 문제를 풀면 체크하세요. 진행 상황은 이 브라우저에만 저장됩니다.",
                blurb_en + " Tick a box when you solve it — progress is saved in this browser only."),
        footnote=L("<em>Premium</em> 표시가 붙은 문제는 LeetCode 유료 계정이 필요합니다. 나머지는 모두 무료입니다. "
                   "링크는 각 저지의 현재 문제 주소를 기준으로 확인했습니다. 혹시 주소가 바뀌었다면 저지에서 제목으로 검색하세요.",
                   "Problems marked <em>Premium</em> need a paid LeetCode account — everything else is free. "
                   "Links were checked against each judge's current problem slug; if one ever moves, "
                   "search the title on the judge's site."))


def pager(prev, nxt):
    """prev / nxt are (href, ko_label, en_label) or None."""
    out = ['<div class="pager">']
    if prev:
        out.append('  <a class="card" href="{0}"><span>{1}</span><b>{2}</b></a>'.format(
            prev[0], L("← 이전", "← Previous"), L(prev[1], prev[2])))
    else:
        out.append('  <a class="card" href="index.html"><span>←</span><b>{0}</b></a>'.format(
            L("홈으로", "Back to the hub")))
    if nxt:
        out.append('  <a class="card" href="{0}" style="text-align:right"><span>{1}</span><b>{2}</b></a>'.format(
            nxt[0], L("다음 단원 →", "Next topic →"), L(nxt[1], nxt[2])))
    else:
        out.append('  <a class="card" href="index.html" style="text-align:right"><span>{0}</span><b>{1}</b></a>'.format(
            L("진도 끝 →", "Finished the syllabus →"), L("홈으로", "Back to the hub")))
    out.append('</div>')
    return "\n".join(out)


def toc(tid, items):
    """items: list of (anchor, ko, en)."""
    links = "\n".join('    <a href="#{0}">{1}</a>'.format(a, L(ko, en)) for a, ko, en in items)
    return """<div class="layout">
<aside class="card toc" style="--c-accent: var(--c-{tid})">
    <b>목차</b>
{links}
</aside>
<div>
""".format(tid=tid, links=links)


def section_title(ko, en):
    return '<h2 class="section-title">%s</h2>' % L(ko, en)


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(content)
    print("wrote", name, len(content), "bytes")
