/* =========================================================
   DSA Practice Hub — shared behaviour
   theme · progress (localStorage) · problem rendering ·
   filtering · random problem · sort-trace widget
   ========================================================= */
(function () {
  "use strict";

  /* ------------------------------------------------------------------
     1. Topic + problem data (single source of truth for every page)
     ------------------------------------------------------------------ */
  const TOPICS = [
    { id: "sorting",     file: "sorting.html",     ko: "정렬",        en: "Sorting",     icon: "⇅", step: "Unit 01",
      blurb: "Bubble and selection sort — how ordering works, pass by pass, and why O(n²) is the price." },
    { id: "queue",       file: "queue.html",       ko: "큐",          en: "Queue",       icon: "◷", step: "Unit 02",
      blurb: "Circular queues on a fixed array: modulo indices, the deliberately empty slot, ring buffers." },
    { id: "linked-list", file: "linked-list.html", ko: "연결 리스트", en: "Linked List", icon: "⛓", step: "Unit 03",
      blurb: "Nodes and links, stacks and queues built on them, and relinking in the middle of a chain." },
    { id: "graph",       file: "graph.html",       ko: "그래프",      en: "Graph",       icon: "◈", step: "Unit 04",
      blurb: "G = (V, E): vertices, edges, degree, and the matrix vs. adjacency-list trade-off." },
    { id: "tree",        file: "tree.html",        ko: "트리",        en: "Tree",        icon: "🌲", step: "Unit 05",
      blurb: "Binary trees, the three traversals, expression trees, and search/insert/delete on a BST." }
  ];

  const LC = "https://leetcode.com/problems/";
  const p = (num, title, diff, hint, url, src, extra) =>
    ({ num, title, diff, hint, url, src: src || "LeetCode", extra: extra || "" });

  const PROBLEMS = {
    sorting: [
      p("LC 88",   "Merge Sorted Array",               "Easy",   "Merging two ordered runs in place — the core move behind merge sort.", LC + "merge-sorted-array/"),
      p("LC 977",  "Squares of a Sorted Array",        "Easy",   "Re-sorting after a transformation; the two-pointer trick beats a full sort.", LC + "squares-of-a-sorted-array/"),
      p("LC 1051", "Height Checker",                   "Easy",   "Compare an array against its sorted copy — a direct 'is this ordered?' drill.", LC + "height-checker/"),
      p("LC 283",  "Move Zeroes",                      "Easy",   "Selection-sort-style scanning and swapping to partition an array.", LC + "move-zeroes/"),
      p("LC 75",   "Sort Colors",                      "Medium", "One-pass three-way partition; think about swap counts like selection sort.", LC + "sort-colors/"),
      p("LC 912",  "Sort an Array",                    "Medium", "Write a real O(n log n) sort yourself — the natural sequel to O(n²).", LC + "sort-an-array/"),
      p("LC 215",  "Kth Largest Element in an Array",  "Medium", "Partial sorting: you only need k passes, not a full sort.", LC + "kth-largest-element-in-an-array/"),
      p("LC 179",  "Largest Number",                   "Medium", "Sorting with a custom comparison rule instead of plain <.", LC + "largest-number/"),
      p("BOJ 2750","수 정렬하기",                       "Easy",   "Small N — safe to submit a hand-written bubble or selection sort.", "https://www.acmicpc.net/problem/2750", "Baekjoon"),
      p("GfG",     "Bubble Sort (practice)",           "Easy",   "Implement the passes literally, including the early-exit optimisation.", "https://www.geeksforgeeks.org/problems/bubble-sort/1", "GeeksforGeeks")
    ],
    queue: [
      p("LC 933",  "Number of Recent Calls",           "Easy",   "A sliding time window is just enqueue at the back, dequeue from the front.", LC + "number-of-recent-calls/"),
      p("LC 232",  "Implement Queue using Stacks",     "Easy",   "Forces you to think about what front/rear really mean.", LC + "implement-queue-using-stacks/"),
      p("LC 225",  "Implement Stack using Queues",     "Easy",   "The mirror image — rotate the queue to fake LIFO order.", LC + "implement-stack-using-queues/"),
      p("BOJ 2164","카드2",                             "Easy",   "Pure queue simulation; a circular queue handles it without shifting.", "https://www.acmicpc.net/problem/2164", "Baekjoon"),
      p("LC 622",  "Design Circular Queue",            "Medium", "The exact structure from class: fixed array, modulo indices, isFull/isEmpty.", LC + "design-circular-queue/"),
      p("LC 641",  "Design Circular Deque",            "Medium", "Same idea with both ends open — push/pop at front and rear.", LC + "design-circular-deque/"),
      p("BOJ 1021","회전하는 큐",                       "Medium", "Rotating a circular queue left or right to reach a target index.", "https://www.acmicpc.net/problem/1021", "Baekjoon"),
      p("LC 239",  "Sliding Window Maximum",           "Hard",   "A monotonic deque — the ring-buffer idea pushed to its limit.", LC + "sliding-window-maximum/"),
      p("LC 346",  "Moving Average from Data Stream",  "Easy",   "Textbook ring buffer over the last N values.", LC + "moving-average-from-data-stream/", "LeetCode", "Premium")
    ],
    "linked-list": [
      p("LC 206",  "Reverse Linked List",              "Easy",   "Relinking every next pointer — the single most important list drill.", LC + "reverse-linked-list/"),
      p("LC 21",   "Merge Two Sorted Lists",           "Easy",   "Walk two lists with two cursors and splice nodes together.", LC + "merge-two-sorted-lists/"),
      p("LC 83",   "Remove Duplicates from Sorted List","Easy",  "The deleteNode(before) pattern: skip a node by rerouting its predecessor.", LC + "remove-duplicates-from-sorted-list/"),
      p("LC 203",  "Remove Linked List Elements",      "Easy",   "Same deletion pattern, plus the head-node edge case (use a dummy head).", LC + "remove-linked-list-elements/"),
      p("LC 876",  "Middle of the Linked List",        "Easy",   "Slow/fast cursors — no random access, so you walk it.", LC + "middle-of-the-linked-list/"),
      p("LC 141",  "Linked List Cycle",                "Easy",   "What happens when a link points backwards instead of to None.", LC + "linked-list-cycle/"),
      p("LC 707",  "Design Linked List",               "Medium", "Build the whole class: get, addAtHead, addAtIndex, deleteAtIndex.", LC + "design-linked-list/"),
      p("LC 19",   "Remove Nth Node From End of List", "Medium", "Gap between two cursors, because you cannot index backwards.", LC + "remove-nth-node-from-end-of-list/"),
      p("LC 146",  "LRU Cache",                        "Medium", "Where a doubly linked list earns its extra pointer.", LC + "lru-cache/"),
      p("GfG",     "Implement a Stack using a Linked List","Easy","Push/pop only at the head — exactly the LinkedStack on this page.", "https://www.geeksforgeeks.org/problems/implement-stack-using-linked-list/1", "GeeksforGeeks")
    ],
    graph: [
      p("LC 1971", "Find if Path Exists in Graph",     "Easy",   "Build an adjacency list, then walk it — the minimal graph exercise.", LC + "find-if-path-exists-in-graph/"),
      p("LC 997",  "Find the Town Judge",              "Easy",   "Pure in-degree / out-degree counting on a directed graph.", LC + "find-the-town-judge/"),
      p("LC 463",  "Island Perimeter",                 "Easy",   "A grid is a graph: each cell's neighbours are its adjacency list.", LC + "island-perimeter/"),
      p("BOJ 1260","DFS와 BFS",                        "Easy",   "Write both traversals over an adjacency list, smallest vertex first.", "https://www.acmicpc.net/problem/1260", "Baekjoon"),
      p("LC 200",  "Number of Islands",                "Medium", "Connected components on an implicit grid graph.", LC + "number-of-islands/"),
      p("LC 133",  "Clone Graph",                      "Medium", "Copy a graph node by node — you must understand adjacency to do it.", LC + "clone-graph/"),
      p("LC 207",  "Course Schedule",                  "Medium", "Directed graph, in-degrees, cycle detection (topological sort).", LC + "course-schedule/"),
      p("LC 785",  "Is Graph Bipartite?",              "Medium", "Two-colour the vertices while traversing an adjacency list.", LC + "is-graph-bipartite/"),
      p("LC 743",  "Network Delay Time",               "Medium", "Weighted directed edges — where the weight in matrix[i][j] matters.", LC + "network-delay-time/")
    ],
    tree: [
      p("LC 144",  "Binary Tree Preorder Traversal",   "Easy",   "VLR — visit, left, right.", LC + "binary-tree-preorder-traversal/"),
      p("LC 94",   "Binary Tree Inorder Traversal",    "Easy",   "LVR — on a BST this prints the keys in sorted order.", LC + "binary-tree-inorder-traversal/"),
      p("LC 145",  "Binary Tree Postorder Traversal",  "Easy",   "LRV — the order an expression tree is evaluated in.", LC + "binary-tree-postorder-traversal/"),
      p("LC 104",  "Maximum Depth of Binary Tree",     "Easy",   "Height from the recursive definition of a binary tree.", LC + "maximum-depth-of-binary-tree/"),
      p("LC 226",  "Invert Binary Tree",               "Easy",   "Left/right order matters — swapping them changes the tree.", LC + "invert-binary-tree/"),
      p("LC 700",  "Search in a Binary Search Tree",   "Easy",   "The three-way compare: match, go left, go right.", LC + "search-in-a-binary-search-tree/"),
      p("LC 108",  "Convert Sorted Array to BST",      "Easy",   "Middle element as root — builds a height-balanced BST.", LC + "convert-sorted-array-to-binary-search-tree/"),
      p("LC 701",  "Insert into a Binary Search Tree", "Medium", "Insert exactly where a failed search would have stopped.", LC + "insert-into-a-binary-search-tree/"),
      p("LC 450",  "Delete Node in a BST",             "Medium", "All three deletion cases, including the in-order successor swap.", LC + "delete-node-in-a-bst/"),
      p("LC 1628", "Design an Expression Tree With Evaluate Function", "Medium", "Build a tree from postfix tokens, then evaluate it recursively.", LC + "design-an-expression-tree-with-evaluate-function/", "LeetCode", "Premium")
    ]
  };

  /* ------------------------------------------------------------------
     2. Storage helpers
     ------------------------------------------------------------------ */
  const KEY_SOLVED = "dsa-hub:solved";
  const KEY_THEME = "dsa-hub:theme";
  const KEY_CELEBRATED = "dsa-hub:celebrated";

  const readJSON = (key, fallback) => {
    try { return JSON.parse(localStorage.getItem(key)) || fallback; }
    catch (e) { return fallback; }
  };
  const writeJSON = (key, value) => {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* private mode */ }
  };

  let solved = readJSON(KEY_SOLVED, {});
  let celebrated = readJSON(KEY_CELEBRATED, {});

  const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const pid = (topic, prob) => topic + "/" + slug(prob.num + "-" + prob.title);

  const topicStats = (topic) => {
    const list = PROBLEMS[topic] || [];
    const done = list.filter((prob) => solved[pid(topic, prob)]).length;
    return { done, total: list.length, pct: list.length ? Math.round((done / list.length) * 100) : 0 };
  };
  const overallStats = () => {
    let done = 0, total = 0;
    TOPICS.forEach((t) => { const s = topicStats(t.id); done += s.done; total += s.total; });
    return { done, total, pct: total ? Math.round((done / total) * 100) : 0 };
  };

  /* ------------------------------------------------------------------
     3. Theme
     ------------------------------------------------------------------ */
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      btn.textContent = theme === "light" ? "☾" : "☀";
      btn.setAttribute("aria-label", theme === "light" ? "Switch to dark mode" : "Switch to light mode");
    });
  }
  function initTheme() {
    applyTheme(localStorage.getItem(KEY_THEME) || "dark");
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
        try { localStorage.setItem(KEY_THEME, next); } catch (e) { /* ignore */ }
        applyTheme(next);
      });
    });
  }

  /* ------------------------------------------------------------------
     4. Celebration
     ------------------------------------------------------------------ */
  function confetti() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const colors = ["#8b5cf6", "#ec4899", "#22d3ee", "#f59e0b", "#34d399"];
    for (let i = 0; i < 70; i++) {
      const el = document.createElement("div");
      el.className = "confetti-piece";
      el.style.left = Math.random() * 100 + "vw";
      el.style.background = colors[i % colors.length];
      el.style.animationDuration = 2.2 + Math.random() * 1.6 + "s";
      el.style.animationDelay = Math.random() * 0.5 + "s";
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 4600);
    }
  }
  function toast(message) {
    const el = document.createElement("div");
    el.className = "toast";
    el.textContent = message;
    document.body.appendChild(el);
    requestAnimationFrame(() => el.classList.add("show"));
    setTimeout(() => { el.classList.remove("show"); setTimeout(() => el.remove(), 500); }, 3200);
  }
  function maybeCelebrate(topic) {
    const s = topicStats(topic);
    if (s.total && s.done === s.total && !celebrated[topic]) {
      celebrated[topic] = true;
      writeJSON(KEY_CELEBRATED, celebrated);
      const meta = TOPICS.find((t) => t.id === topic);
      confetti();
      toast("🎉 " + (meta ? meta.en : topic) + " complete — " + s.total + "/" + s.total + " solved!");
    } else if (s.done < s.total && celebrated[topic]) {
      delete celebrated[topic];
      writeJSON(KEY_CELEBRATED, celebrated);
    }
  }

  /* ------------------------------------------------------------------
     5. Problem list rendering (topic pages)
     ------------------------------------------------------------------ */
  function problemNode(topic, prob) {
    const id = pid(topic, prob);
    const li = document.createElement("li");
    li.className = "pitem" + (solved[id] ? " done" : "");
    li.dataset.difficulty = prob.diff.toLowerCase();
    li.dataset.text = (prob.num + " " + prob.title + " " + prob.hint + " " + prob.src).toLowerCase();

    const box = document.createElement("input");
    box.type = "checkbox";
    box.className = "pcheck";
    box.checked = !!solved[id];
    box.id = "chk-" + id;
    box.setAttribute("aria-label", "Mark " + prob.title + " as solved");

    const body = document.createElement("div");
    body.className = "pbody";
    const link = document.createElement("a");
    link.className = "ptitle";
    link.href = prob.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    const tag = document.createElement("span");
    tag.className = "pnum-tag";
    tag.textContent = prob.num;
    link.appendChild(tag);
    link.appendChild(document.createTextNode(prob.title));
    const hint = document.createElement("p");
    hint.className = "phint";
    hint.textContent = prob.hint;
    body.appendChild(link);
    body.appendChild(hint);

    const meta = document.createElement("div");
    meta.className = "pmeta";
    const diff = document.createElement("span");
    diff.className = "badge " + prob.diff.toLowerCase();
    diff.textContent = prob.diff;
    const src = document.createElement("span");
    src.className = "badge src";
    src.textContent = prob.extra ? prob.src + " · " + prob.extra : prob.src;
    meta.appendChild(diff);
    meta.appendChild(src);

    box.addEventListener("change", () => {
      if (box.checked) { solved[id] = 1; } else { delete solved[id]; }
      writeJSON(KEY_SOLVED, solved);
      li.classList.toggle("done", box.checked);
      refreshProgress();
      if (box.checked) maybeCelebrate(topic);
    });

    li.appendChild(box);
    li.appendChild(body);
    li.appendChild(meta);
    return li;
  }

  function renderProblems(topic) {
    const mount = document.getElementById("problem-list");
    if (!mount) return;
    const list = PROBLEMS[topic] || [];
    mount.innerHTML = "";
    list.forEach((prob) => mount.appendChild(problemNode(topic, prob)));

    const search = document.getElementById("problem-search");
    const chips = Array.prototype.slice.call(document.querySelectorAll(".filters [data-diff]"));
    const empty = document.getElementById("problem-empty");

    function applyFilters() {
      const q = (search && search.value || "").trim().toLowerCase();
      const active = chips.filter((c) => c.getAttribute("aria-pressed") === "true").map((c) => c.dataset.diff);
      let visible = 0;
      Array.prototype.forEach.call(mount.children, (li) => {
        const okDiff = !active.length || active.indexOf("all") > -1 || active.indexOf(li.dataset.difficulty) > -1;
        const okText = !q || li.dataset.text.indexOf(q) > -1;
        const show = okDiff && okText;
        li.style.display = show ? "" : "none";
        if (show) visible++;
      });
      if (empty) empty.style.display = visible ? "none" : "block";
    }

    if (search) search.addEventListener("input", applyFilters);
    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        const isAll = chip.dataset.diff === "all";
        const on = chip.getAttribute("aria-pressed") === "true";
        if (isAll) {
          chips.forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
        } else {
          chip.setAttribute("aria-pressed", String(!on));
          const allChip = chips.filter((c) => c.dataset.diff === "all")[0];
          if (allChip) {
            const any = chips.some((c) => c.dataset.diff !== "all" && c.getAttribute("aria-pressed") === "true");
            allChip.setAttribute("aria-pressed", String(!any));
          }
        }
        applyFilters();
      });
    });
    applyFilters();
  }

  /* ------------------------------------------------------------------
     6. Progress UI
     ------------------------------------------------------------------ */
  function setRing(el, pct) {
    el.style.setProperty("--pct", pct);
    const label = el.querySelector("text");
    if (label) label.textContent = pct + "%";
  }
  function refreshProgress() {
    document.querySelectorAll("[data-progress-topic]").forEach((el) => {
      const s = topicStats(el.dataset.progressTopic);
      const bar = el.querySelector(".pbar span");
      const num = el.querySelector(".pnum");
      const ring = el.querySelector(".ring");
      if (bar) bar.style.width = s.pct + "%";
      if (num) num.textContent = s.done + " / " + s.total + " solved";
      if (ring) setRing(ring, s.pct);
    });
    const o = overallStats();
    document.querySelectorAll("[data-overall]").forEach((el) => {
      const kind = el.dataset.overall;
      if (kind === "pct") el.textContent = o.pct + "%";
      else if (kind === "done") el.textContent = o.done;
      else if (kind === "total") el.textContent = o.total;
      else if (kind === "remaining") el.textContent = o.total - o.done;
      else if (kind === "topics") el.textContent = TOPICS.filter((t) => { const s = topicStats(t.id); return s.total && s.done === s.total; }).length;
      else if (kind === "bar") el.style.width = o.pct + "%";
      else if (kind === "ring") setRing(el, o.pct);
    });
  }

  /* ------------------------------------------------------------------
     7. Home page: topic cards
     ------------------------------------------------------------------ */
  function renderTopicCards() {
    const grid = document.getElementById("topic-grid");
    if (!grid) return;
    grid.innerHTML = TOPICS.map((t) => {
      const s = topicStats(t.id);
      return [
        '<a class="card topic-card" href="', t.file, '" style="--grad: var(--grad-', t.id, ')" data-progress-topic="', t.id, '">',
        '<div class="topic-head">',
        '<div class="topic-icon">', t.icon, '</div>',
        '<div><div class="topic-step">', t.step, '</div>',
        '<h3>', t.en, ' <span class="ko">', t.ko, '</span></h3></div>',
        '</div>',
        '<p>', t.blurb, '</p>',
        '<div class="topic-foot">',
        ringSVG(s.pct),
        '<div style="flex:1"><div class="pbar"><span></span></div>',
        '<div class="pnum" style="margin-top:.35rem"></div></div>',
        '</div></a>'
      ].join("");
    }).join("");
  }
  function ringSVG(pct) {
    return '<svg class="ring" viewBox="0 0 48 48" style="--pct:' + pct + '" aria-hidden="true">' +
      '<circle class="track" cx="24" cy="24" r="20"></circle>' +
      '<circle class="bar" cx="24" cy="24" r="20"></circle>' +
      '<text x="24" y="25" text-anchor="middle">' + pct + '%</text></svg>';
  }

  /* ------------------------------------------------------------------
     8. Random problem
     ------------------------------------------------------------------ */
  function initRandom() {
    const btn = document.getElementById("random-problem");
    if (!btn) return;
    btn.addEventListener("click", () => {
      const scope = btn.dataset.topic;
      const pool = [];
      (scope ? [scope] : TOPICS.map((t) => t.id)).forEach((topic) => {
        (PROBLEMS[topic] || []).forEach((prob) => {
          if (!solved[pid(topic, prob)]) pool.push(prob);
        });
      });
      if (!pool.length) { toast("Everything here is solved. 다 풀었어요! 🎉"); return; }
      const pick = pool[Math.floor(Math.random() * pool.length)];
      toast("→ " + pick.num + " " + pick.title);
      window.open(pick.url, "_blank", "noopener");
    });
  }

  /* ------------------------------------------------------------------
     9. Reset button
     ------------------------------------------------------------------ */
  function initReset() {
    const btn = document.getElementById("reset-progress");
    if (!btn) return;
    btn.addEventListener("click", () => {
      if (!window.confirm("Clear every solved checkbox on this device?")) return;
      solved = {}; celebrated = {};
      writeJSON(KEY_SOLVED, solved);
      writeJSON(KEY_CELEBRATED, celebrated);
      document.querySelectorAll(".pcheck").forEach((box) => {
        box.checked = false;
        box.closest(".pitem").classList.remove("done");
      });
      renderTopicCards();
      refreshProgress();
      toast("Progress cleared.");
    });
  }

  /* ------------------------------------------------------------------
     10. In-page table of contents highlighting
     ------------------------------------------------------------------ */
  function initTOC() {
    const links = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
    if (!links.length || !("IntersectionObserver" in window)) return;
    const map = {};
    const targets = [];
    links.forEach((a) => {
      const el = document.querySelector(a.getAttribute("href"));
      if (el) { map[el.id] = a; targets.push(el); }
    });
    const seen = new Set();
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) seen.add(e.target.id); else seen.delete(e.target.id); });
      let current = null;
      targets.forEach((t) => { if (seen.has(t.id) && !current) current = t.id; });
      if (current) links.forEach((a) => a.classList.toggle("active", map[current] === a));
    }, { rootMargin: "-88px 0px -65% 0px", threshold: 0 });
    targets.forEach((t) => io.observe(t));
  }

  /* ------------------------------------------------------------------
     11. Copy buttons for code blocks
     ------------------------------------------------------------------ */
  function initCopy() {
    document.querySelectorAll(".code-card").forEach((card) => {
      const btn = card.querySelector(".copy-btn");
      const code = card.querySelector("code");
      if (!btn || !code || !navigator.clipboard) { if (btn) btn.style.display = "none"; return; }
      btn.addEventListener("click", () => {
        navigator.clipboard.writeText(code.textContent).then(() => {
          btn.textContent = "copied";
          setTimeout(() => { btn.textContent = "copy"; }, 1400);
        });
      });
    });
  }

  /* ------------------------------------------------------------------
     12. Sorting trace widget (sorting.html only)
     ------------------------------------------------------------------ */
  function bubbleSteps(input) {
    const a = input.slice();
    const steps = [{ arr: a.slice(), locked: 0, cmp: [], swap: [],
      note: "Start. Bubble sort compares <b>adjacent</b> pairs and swaps them when they are out of order." }];
    const n = a.length;
    for (let pass = 0; pass < n - 1; pass++) {
      let swapped = false;
      for (let i = 0; i < n - 1 - pass; i++) {
        steps.push({ arr: a.slice(), locked: pass, cmp: [i, i + 1], swap: [],
          note: "Pass " + (pass + 1) + ": compare <b>" + a[i] + "</b> and <b>" + a[i + 1] + "</b>." });
        if (a[i] > a[i + 1]) {
          const t = a[i]; a[i] = a[i + 1]; a[i + 1] = t;
          swapped = true;
          steps.push({ arr: a.slice(), locked: pass, cmp: [], swap: [i, i + 1],
            note: "Out of order → swap. The larger value keeps moving right." });
        } else {
          steps.push({ arr: a.slice(), locked: pass, cmp: [], swap: [],
            note: "Already in order → no swap, move one step right." });
        }
      }
      steps.push({ arr: a.slice(), locked: pass + 1, cmp: [], swap: [],
        note: "End of pass " + (pass + 1) + ": <b>" + a[n - 1 - pass] + "</b> has bubbled to its final slot. " +
          (pass + 1) + " value(s) locked." });
      if (!swapped) {
        steps.push({ arr: a.slice(), locked: n, cmp: [], swap: [],
          note: "No swap happened in this pass → the array is already sorted, so we can stop early (best case O(n))." });
        return steps;
      }
    }
    steps.push({ arr: a.slice(), locked: n, cmp: [], swap: [], note: "Done after n−1 = " + (n - 1) + " passes. 완료!" });
    return steps;
  }

  function selectionSteps(input) {
    const a = input.slice();
    const steps = [{ arr: a.slice(), locked: 0, cmp: [], swap: [], min: -1,
      note: "Start. Selection sort finds the <b>minimum of the unsorted part</b> and swaps it into place." }];
    const n = a.length;
    for (let start = 0; start < n - 1; start++) {
      let lo = start;
      steps.push({ arr: a.slice(), locked: start, cmp: [], swap: [], min: lo,
        note: "Pass " + (start + 1) + ": assume <b>" + a[lo] + "</b> (index " + lo + ") is the smallest remaining value." });
      for (let i = start + 1; i < n; i++) {
        steps.push({ arr: a.slice(), locked: start, cmp: [i], swap: [], min: lo,
          note: "Compare <b>" + a[i] + "</b> against the current minimum <b>" + a[lo] + "</b>." });
        if (a[i] < a[lo]) {
          lo = i;
          steps.push({ arr: a.slice(), locked: start, cmp: [], swap: [], min: lo,
            note: "Smaller → the new minimum is <b>" + a[lo] + "</b>." });
        }
      }
      if (lo !== start) {
        const t = a[start]; a[start] = a[lo]; a[lo] = t;
        steps.push({ arr: a.slice(), locked: start, cmp: [], swap: [start, lo], min: -1,
          note: "Swap the minimum into index " + start + ". That is <b>one</b> swap for the whole pass." });
      } else {
        steps.push({ arr: a.slice(), locked: start, cmp: [], swap: [], min: -1,
          note: "The minimum was already in index " + start + " → no swap needed." });
      }
      steps.push({ arr: a.slice(), locked: start + 1, cmp: [], swap: [], min: -1,
        note: "End of pass " + (start + 1) + ": index " + start + " is final." });
    }
    steps.push({ arr: a.slice(), locked: n, cmp: [], swap: [], min: -1,
      note: "Done — exactly n−1 = " + (n - 1) + " passes, and at most n−1 swaps total." });
    return steps;
  }

  function initTrace() {
    const root = document.getElementById("trace-widget");
    if (!root) return;
    const barsEl = root.querySelector(".bars");
    const noteEl = root.querySelector(".trace-note");
    const countEl = root.querySelector(".step-count");
    const input = root.querySelector("#trace-input");
    const algoBtns = Array.prototype.slice.call(root.querySelectorAll("[data-algo]"));

    let algo = "bubble";
    let steps = [];
    let idx = 0;
    let timer = null;

    function parseInput() {
      const raw = (input.value || "").split(/[^0-9-]+/).filter(Boolean).map(Number).slice(0, 9);
      return raw.length >= 2 ? raw : [5, 4, 3, 2, 1];
    }
    function build() {
      const arr = parseInput();
      steps = algo === "bubble" ? bubbleSteps(arr) : selectionSteps(arr);
      idx = 0;
      draw();
    }
    function draw() {
      const s = steps[idx];
      const max = Math.max.apply(null, s.arr.map(Math.abs)) || 1;
      barsEl.innerHTML = s.arr.map((v, i) => {
        let cls = "bar";
        if (s.swap.indexOf(i) > -1) cls += " swap";
        else if (s.cmp.indexOf(i) > -1) cls += " cmp";
        else if (s.min === i) cls += " min";
        const lockedFromRight = algo === "bubble" && i >= s.arr.length - s.locked;
        const lockedFromLeft = algo === "selection" && i < s.locked;
        if (lockedFromRight || lockedFromLeft) cls += " locked";
        const h = 44 + Math.round((Math.abs(v) / max) * 120);
        return '<div class="' + cls + '" style="height:' + h + 'px">' + v + '</div>';
      }).join("");
      noteEl.innerHTML = s.note;
      countEl.textContent = "step " + (idx + 1) + " / " + steps.length;
    }
    function go(delta) {
      idx = Math.min(steps.length - 1, Math.max(0, idx + delta));
      draw();
    }
    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
      root.querySelector("#trace-play").textContent = "▶ Play";
    }

    algoBtns.forEach((btn) => btn.addEventListener("click", () => {
      algo = btn.dataset.algo;
      algoBtns.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
      stop(); build();
    }));
    root.querySelector("#trace-next").addEventListener("click", () => { stop(); go(1); });
    root.querySelector("#trace-prev").addEventListener("click", () => { stop(); go(-1); });
    root.querySelector("#trace-reset").addEventListener("click", () => { stop(); build(); });
    root.querySelector("#trace-play").addEventListener("click", function () {
      if (timer) { stop(); return; }
      this.textContent = "⏸ Pause";
      timer = setInterval(() => {
        if (idx >= steps.length - 1) { stop(); return; }
        go(1);
      }, 750);
    });
    input.addEventListener("change", () => { stop(); build(); });
    build();
  }

  /* ------------------------------------------------------------------
     12b. Fallback Python highlighter
     Prism is loaded from a CDN. If that request is blocked or the reader is
     offline, code still has to be readable, so tokenise it here using the
     same class names Prism would have produced.
     ------------------------------------------------------------------ */
  const PY_TOKENS = new RegExp(
    "(#[^\\n]*)" +                                                    // comment
    "|(\"\"\"[\\s\\S]*?\"\"\"|'''[\\s\\S]*?'''" +
      "|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*')" +            // string
    "|(@[A-Za-z_][\\w.]*)" +                                          // decorator
    "|\\b(False|None|True|and|as|assert|async|await|break|class|continue|def|del" +
      "|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal" +
      "|not|or|pass|raise|return|try|while|with|yield)\\b" +          // keyword
    "|\\b(abs|all|any|bool|dict|enumerate|float|int|len|list|map|max|min|print" +
      "|range|repr|reversed|round|self|set|sorted|str|sum|super|tuple|type|zip" +
      "|IndexError|ValueError|deque|defaultdict|operator)\\b" +       // builtin-ish
    "|\\b(\\d+\\.?\\d*)\\b" +                                         // number
    "|(\\*\\*|//|[+\\-*/%<>!=]=?)",                                   // operator
    "g");

  function escapeHTML(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlightPython(source) {
    let out = "";
    let last = 0;
    source.replace(PY_TOKENS, function (match, comment, str, deco, keyword, builtin, number, operator, offset) {
      out += escapeHTML(source.slice(last, offset));
      const cls = comment ? "comment" : str ? "string" : deco ? "decorator"
        : keyword ? "keyword" : builtin ? "builtin" : number ? "number" : "operator";
      out += '<span class="token ' + cls + '">' + escapeHTML(match) + "</span>";
      last = offset + match.length;
      return match;
    });
    return out + escapeHTML(source.slice(last));
  }

  function fallbackHighlight() {
    document.querySelectorAll(".code-card code.language-python").forEach(function (el) {
      if (el.querySelector(".token")) return;      // Prism already did the job
      el.innerHTML = highlightPython(el.textContent);
    });
  }

  /* ------------------------------------------------------------------
     13. Boot
     ------------------------------------------------------------------ */
  function boot() {
    initTheme();
    renderTopicCards();
    const topic = document.body.dataset.topic;
    if (topic) renderProblems(topic);
    refreshProgress();
    initRandom();
    initReset();
    initTOC();
    initCopy();
    initTrace();
    if (window.Prism) window.Prism.highlightAll();
    fallbackHighlight();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
