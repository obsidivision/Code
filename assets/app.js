/* =========================================================
   DSA Practice Hub — shared behaviour
   language (ko/en) · theme · progress (localStorage) ·
   problem rendering · filtering · random problem · sort tracer
   ========================================================= */
(function () {
  "use strict";

  /* ------------------------------------------------------------------
     1. Topics
     `hidden: true` keeps a unit's page working and reachable by URL, but
     drops it from the nav, the home grid, the random-problem pool and the
     progress totals. Flip the flag when the unit comes back on the
     syllabus — nothing else needs editing.
     ------------------------------------------------------------------ */
  const TOPICS = [
    { id: "sorting", file: "sorting.html", icon: "⇅", hidden: true,
      ko: "정렬", en: "Sorting", stepKo: "1단원", stepEn: "Unit 01",
      blurbKo: "버블 정렬과 선택 정렬 — 패스마다 순서가 어떻게 잡히는지, 그리고 O(n²)이라는 대가.",
      blurbEn: "Bubble and selection sort — how ordering works, pass by pass, and why O(n²) is the price." },
    { id: "queue", file: "queue.html", icon: "◷",
      ko: "큐", en: "Queue", stepKo: "2단원", stepEn: "Unit 02",
      blurbKo: "고정 크기 배열 위의 원형 큐: 모듈로 인덱스, 일부러 비워 두는 한 칸, 링 버퍼.",
      blurbEn: "Circular queues on a fixed array: modulo indices, the deliberately empty slot, ring buffers." },
    { id: "linked-list", file: "linked-list.html", icon: "⛓",
      ko: "연결 리스트", en: "Linked List", stepKo: "3단원", stepEn: "Unit 03",
      blurbKo: "노드와 링크, 그 위에 올린 스택과 큐, 그리고 리스트 중간에서 링크를 다시 잇는 법.",
      blurbEn: "Nodes and links, stacks and queues built on them, and relinking in the middle of a chain." },
    { id: "graph", file: "graph.html", icon: "◈",
      ko: "그래프", en: "Graph", stepKo: "4단원", stepEn: "Unit 04",
      blurbKo: "G = (V, E): 정점과 간선, 차수와 경로, 그리고 인접 행렬과 인접 리스트의 선택.",
      blurbEn: "G = (V, E): vertices, edges, degree, and the matrix vs. adjacency-list trade-off." },
    { id: "tree", file: "tree.html", icon: "🌲",
      ko: "트리", en: "Tree", stepKo: "5단원", stepEn: "Unit 05",
      blurbKo: "이진 트리와 세 가지 순회, 수식 트리, 그리고 이진 탐색 트리의 탐색·삽입·삭제.",
      blurbEn: "Binary trees, the three traversals, expression trees, and search/insert/delete on a BST." }
  ];

  const visibleTopics = () => TOPICS.filter((t) => !t.hidden);
  const topicMeta = (id) => TOPICS.filter((t) => t.id === id)[0];

  /* ------------------------------------------------------------------
     2. Problems. Titles stay in English because that is how they are
     listed on the judge; only the hint is translated.
     ------------------------------------------------------------------ */
  const LC = "https://leetcode.com/problems/";
  const p = (num, title, diff, hintEn, hintKo, url, src, extra) =>
    ({ num, title, diff, hintEn, hintKo, url, src: src || "LeetCode", extra: extra || "" });

  const PROBLEMS = {
    sorting: [
      p("LC 88", "Merge Sorted Array", "Easy",
        "Merging two ordered runs in place — the core move behind merge sort.",
        "정렬된 두 구간을 제자리에서 합치기 — 병합 정렬의 핵심 동작입니다.",
        LC + "merge-sorted-array/"),
      p("LC 977", "Squares of a Sorted Array", "Easy",
        "Re-sorting after a transformation; the two-pointer trick beats a full sort.",
        "값을 바꾼 뒤 다시 정렬하기. 투 포인터를 쓰면 전체 정렬보다 빠릅니다.",
        LC + "squares-of-a-sorted-array/"),
      p("LC 1051", "Height Checker", "Easy",
        "Compare an array against its sorted copy — a direct 'is this ordered?' drill.",
        "배열을 정렬한 사본과 비교하기 — '정렬되어 있는가'를 그대로 묻는 문제입니다.",
        LC + "height-checker/"),
      p("LC 283", "Move Zeroes", "Easy",
        "Selection-sort-style scanning and swapping to partition an array.",
        "선택 정렬처럼 훑으면서 교환해 배열을 두 부분으로 나눕니다.",
        LC + "move-zeroes/"),
      p("LC 75", "Sort Colors", "Medium",
        "One-pass three-way partition; think about swap counts like selection sort.",
        "한 번의 순회로 세 부분 분할. 선택 정렬처럼 교환 횟수를 세어 보세요.",
        LC + "sort-colors/"),
      p("LC 912", "Sort an Array", "Medium",
        "Write a real O(n log n) sort yourself — the natural sequel to O(n²).",
        "O(n log n) 정렬을 직접 구현해 보기 — O(n²) 다음에 올 자연스러운 단계입니다.",
        LC + "sort-an-array/"),
      p("LC 215", "Kth Largest Element in an Array", "Medium",
        "Partial sorting: you only need k passes, not a full sort.",
        "부분 정렬: 전체를 정렬할 필요 없이 k번의 패스면 충분합니다.",
        LC + "kth-largest-element-in-an-array/"),
      p("LC 179", "Largest Number", "Medium",
        "Sorting with a custom comparison rule instead of plain <.",
        "단순한 < 대신 직접 만든 비교 규칙으로 정렬합니다.",
        LC + "largest-number/"),
      p("BOJ 2750", "수 정렬하기", "Easy",
        "N is small — safe to submit a hand-written bubble or selection sort.",
        "N이 작아서 직접 짠 버블 정렬이나 선택 정렬로도 통과합니다.",
        "https://www.acmicpc.net/problem/2750", "Baekjoon"),
      p("GfG", "Bubble Sort (practice)", "Easy",
        "Implement the passes literally, including the early-exit optimisation.",
        "패스를 그대로 구현하기. 조기 종료 최적화까지 포함해 보세요.",
        "https://www.geeksforgeeks.org/problems/bubble-sort/1", "GeeksforGeeks")
    ],
    queue: [
      p("LC 933", "Number of Recent Calls", "Easy",
        "A sliding time window is just enqueue at the back, dequeue from the front.",
        "시간 윈도우 슬라이딩은 결국 뒤에서 넣고 앞에서 빼는 큐입니다.",
        LC + "number-of-recent-calls/"),
      p("LC 232", "Implement Queue using Stacks", "Easy",
        "Forces you to think about what front/rear really mean.",
        "front와 rear가 실제로 무엇을 가리키는지 다시 생각하게 만듭니다.",
        LC + "implement-queue-using-stacks/"),
      p("LC 225", "Implement Stack using Queues", "Easy",
        "The mirror image — rotate the queue to fake LIFO order.",
        "반대 방향 문제 — 큐를 회전시켜 후입선출을 흉내 냅니다.",
        LC + "implement-stack-using-queues/"),
      p("BOJ 2164", "카드2", "Easy",
        "Pure queue simulation; a circular queue handles it without shifting.",
        "순수한 큐 시뮬레이션. 원형 큐라면 값을 옮기지 않고 처리됩니다.",
        "https://www.acmicpc.net/problem/2164", "Baekjoon"),
      p("LC 622", "Design Circular Queue", "Medium",
        "The exact structure from class: fixed array, modulo indices, isFull/isEmpty.",
        "수업에서 배운 그 구조: 고정 배열, 모듈로 인덱스, isFull/isEmpty.",
        LC + "design-circular-queue/"),
      p("LC 641", "Design Circular Deque", "Medium",
        "Same idea with both ends open — push/pop at front and rear.",
        "양쪽 끝이 모두 열린 같은 구조 — 앞뒤에서 넣고 뺍니다.",
        LC + "design-circular-deque/"),
      p("BOJ 1021", "회전하는 큐", "Medium",
        "Rotating a circular queue left or right to reach a target index.",
        "원형 큐를 좌우로 회전시켜 목표 인덱스에 도달하는 문제입니다.",
        "https://www.acmicpc.net/problem/1021", "Baekjoon"),
      p("LC 239", "Sliding Window Maximum", "Hard",
        "A monotonic deque — the ring-buffer idea pushed to its limit.",
        "단조 덱 — 링 버퍼 아이디어를 끝까지 밀어붙인 문제입니다.",
        LC + "sliding-window-maximum/"),
      p("LC 346", "Moving Average from Data Stream", "Easy",
        "Textbook ring buffer over the last N values.",
        "최근 N개 값만 유지하는 교과서적인 링 버퍼입니다.",
        LC + "moving-average-from-data-stream/", "LeetCode", "Premium")
    ],
    "linked-list": [
      p("LC 206", "Reverse Linked List", "Easy",
        "Relinking every next pointer — the single most important list drill.",
        "모든 next 포인터를 다시 잇기 — 연결 리스트에서 가장 중요한 연습입니다.",
        LC + "reverse-linked-list/"),
      p("LC 21", "Merge Two Sorted Lists", "Easy",
        "Walk two lists with two cursors and splice nodes together.",
        "커서 두 개로 두 리스트를 훑으며 노드를 이어 붙입니다.",
        LC + "merge-two-sorted-lists/"),
      p("LC 83", "Remove Duplicates from Sorted List", "Easy",
        "The deleteNode(before) pattern: skip a node by rerouting its predecessor.",
        "deleteNode(before) 패턴: 앞 노드의 링크를 돌려 노드를 건너뜁니다.",
        LC + "remove-duplicates-from-sorted-list/"),
      p("LC 203", "Remove Linked List Elements", "Easy",
        "Same deletion pattern, plus the head-node edge case (use a dummy head).",
        "같은 삭제 패턴에 head 처리까지 — 더미 헤드를 쓰면 편합니다.",
        LC + "remove-linked-list-elements/"),
      p("LC 876", "Middle of the Linked List", "Easy",
        "Slow/fast cursors — no random access, so you walk it.",
        "느린/빠른 커서 — 임의 접근이 안 되니 직접 걸어가야 합니다.",
        LC + "middle-of-the-linked-list/"),
      p("LC 141", "Linked List Cycle", "Easy",
        "What happens when a link points backwards instead of to None.",
        "링크가 None이 아니라 뒤를 가리킬 때 어떤 일이 생기는지 봅니다.",
        LC + "linked-list-cycle/"),
      p("LC 707", "Design Linked List", "Medium",
        "Build the whole class: get, addAtHead, addAtIndex, deleteAtIndex.",
        "클래스 전체를 직접 구현: get, addAtHead, addAtIndex, deleteAtIndex.",
        LC + "design-linked-list/"),
      p("LC 19", "Remove Nth Node From End of List", "Medium",
        "Gap between two cursors, because you cannot index backwards.",
        "뒤에서부터 셀 수 없으니 커서 두 개의 간격을 이용합니다.",
        LC + "remove-nth-node-from-end-of-list/"),
      p("LC 146", "LRU Cache", "Medium",
        "Where a doubly linked list earns its extra pointer.",
        "이중 연결 리스트가 포인터 하나를 더 쓸 값을 하는 자리입니다.",
        LC + "lru-cache/"),
      p("GfG", "Implement a Stack using a Linked List", "Easy",
        "Push/pop only at the head — exactly the LinkedStack on this page.",
        "head에서만 push/pop — 이 페이지의 LinkedStack 그대로입니다.",
        "https://www.geeksforgeeks.org/problems/implement-stack-using-linked-list/1", "GeeksforGeeks")
    ],
    graph: [
      p("LC 1971", "Find if Path Exists in Graph", "Easy",
        "Build an adjacency list, then walk it — the minimal graph exercise.",
        "인접 리스트를 만들고 따라가 보기 — 가장 기본적인 그래프 문제입니다.",
        LC + "find-if-path-exists-in-graph/"),
      p("LC 997", "Find the Town Judge", "Easy",
        "Pure in-degree / out-degree counting on a directed graph.",
        "방향 그래프에서 진입 차수와 진출 차수만 세면 되는 문제입니다.",
        LC + "find-the-town-judge/"),
      p("LC 463", "Island Perimeter", "Easy",
        "A grid is a graph: each cell's neighbours are its adjacency list.",
        "격자도 그래프입니다: 각 칸의 이웃이 곧 인접 리스트입니다.",
        LC + "island-perimeter/"),
      p("BOJ 1260", "DFS와 BFS", "Easy",
        "Write both traversals over an adjacency list, smallest vertex first.",
        "인접 리스트 위에서 두 순회를 모두 구현합니다. 작은 정점부터 방문하세요.",
        "https://www.acmicpc.net/problem/1260", "Baekjoon"),
      p("LC 200", "Number of Islands", "Medium",
        "Connected components on an implicit grid graph.",
        "격자로 표현된 그래프에서 연결 요소를 세는 문제입니다.",
        LC + "number-of-islands/"),
      p("LC 133", "Clone Graph", "Medium",
        "Copy a graph node by node — you must understand adjacency to do it.",
        "그래프를 노드 단위로 복사하기 — 인접 관계를 이해해야 풀립니다.",
        LC + "clone-graph/"),
      p("LC 207", "Course Schedule", "Medium",
        "Directed graph, in-degrees, cycle detection (topological sort).",
        "방향 그래프, 진입 차수, 사이클 판별 (위상 정렬).",
        LC + "course-schedule/"),
      p("LC 785", "Is Graph Bipartite?", "Medium",
        "Two-colour the vertices while traversing an adjacency list.",
        "인접 리스트를 순회하면서 정점을 두 색으로 칠합니다.",
        LC + "is-graph-bipartite/"),
      p("LC 743", "Network Delay Time", "Medium",
        "Weighted directed edges — where the weight in matrix[i][j] matters.",
        "가중치 있는 방향 간선 — matrix[i][j]의 가중치가 의미를 갖는 문제입니다.",
        LC + "network-delay-time/")
    ],
    tree: [
      p("LC 144", "Binary Tree Preorder Traversal", "Easy",
        "VLR — visit, left, right.",
        "전위 순회 VLR — 노드, 왼쪽, 오른쪽 순서입니다.",
        LC + "binary-tree-preorder-traversal/"),
      p("LC 94", "Binary Tree Inorder Traversal", "Easy",
        "LVR — on a BST this prints the keys in sorted order.",
        "중위 순회 LVR — 이진 탐색 트리에서는 정렬된 순서로 나옵니다.",
        LC + "binary-tree-inorder-traversal/"),
      p("LC 145", "Binary Tree Postorder Traversal", "Easy",
        "LRV — the order an expression tree is evaluated in.",
        "후위 순회 LRV — 수식 트리를 계산하는 순서입니다.",
        LC + "binary-tree-postorder-traversal/"),
      p("LC 104", "Maximum Depth of Binary Tree", "Easy",
        "Height from the recursive definition of a binary tree.",
        "이진 트리의 재귀적 정의에서 바로 나오는 높이 계산입니다.",
        LC + "maximum-depth-of-binary-tree/"),
      p("LC 226", "Invert Binary Tree", "Easy",
        "Left/right order matters — swapping them changes the tree.",
        "왼쪽과 오른쪽의 구분이 중요합니다 — 바꾸면 다른 트리가 됩니다.",
        LC + "invert-binary-tree/"),
      p("LC 700", "Search in a Binary Search Tree", "Easy",
        "The three-way compare: match, go left, go right.",
        "세 갈래 비교: 같으면 찾음, 작으면 왼쪽, 크면 오른쪽.",
        LC + "search-in-a-binary-search-tree/"),
      p("LC 108", "Convert Sorted Array to BST", "Easy",
        "Middle element as root — builds a height-balanced BST.",
        "가운데 원소를 루트로 — 높이 균형이 잡힌 이진 탐색 트리가 만들어집니다.",
        LC + "convert-sorted-array-to-binary-search-tree/"),
      p("LC 701", "Insert into a Binary Search Tree", "Medium",
        "Insert exactly where a failed search would have stopped.",
        "탐색이 실패해 멈추는 바로 그 자리에 삽입합니다.",
        LC + "insert-into-a-binary-search-tree/"),
      p("LC 450", "Delete Node in a BST", "Medium",
        "All three deletion cases, including the in-order successor swap.",
        "삭제의 세 경우 전부 — 중위 후속자로 바꾸는 경우까지 포함합니다.",
        LC + "delete-node-in-a-bst/"),
      p("LC 1628", "Design an Expression Tree With Evaluate Function", "Medium",
        "Build a tree from postfix tokens, then evaluate it recursively.",
        "후위 표기 토큰으로 트리를 만들고 재귀적으로 계산합니다.",
        LC + "design-an-expression-tree-with-evaluate-function/", "LeetCode", "Premium")
    ]
  };

  /* ------------------------------------------------------------------
     3. UI strings
     ------------------------------------------------------------------ */
  const STR = {
    ko: {
      solved: function (d, t) { return d + " / " + t + "문제 완료"; },
      markSolved: function (title) { return title + " 완료로 표시"; },
      all: "전체", easy: "쉬움", medium: "보통", hard: "어려움",
      searchPlaceholder: "제목·힌트·저지로 검색…",
      searchLabel: "문제 검색",
      random: "🎲 안 푼 문제 랜덤",
      empty: "조건에 맞는 문제가 없습니다.",
      reset: "진행 상황 초기화",
      resetConfirm: "이 브라우저에 저장된 체크를 모두 지울까요?",
      resetDone: "진행 상황을 지웠습니다.",
      allSolved: "여기 있는 문제는 전부 풀었습니다! 🎉",
      complete: function (name, n) { return "🎉 " + name + " 완료 — " + n + "문제 전부 풀었습니다!"; },
      copy: "복사", copied: "복사됨",
      themeToDark: "어두운 테마로 전환", themeToLight: "밝은 테마로 전환",
      langLabel: "언어 전환 / Switch language", langButton: "EN",
      onThisPage: "목차"
    },
    en: {
      solved: function (d, t) { return d + " / " + t + " solved"; },
      markSolved: function (title) { return "Mark " + title + " as solved"; },
      all: "All", easy: "Easy", medium: "Medium", hard: "Hard",
      searchPlaceholder: "Filter by title, hint or judge…",
      searchLabel: "Filter problems",
      random: "🎲 Random unsolved",
      empty: "No problem matches that filter.",
      reset: "Reset all progress",
      resetConfirm: "Clear every solved checkbox on this device?",
      resetDone: "Progress cleared.",
      allSolved: "Everything here is solved. 다 풀었어요! 🎉",
      complete: function (name, n) { return "🎉 " + name + " complete — " + n + "/" + n + " solved!"; },
      copy: "copy", copied: "copied",
      themeToDark: "Switch to dark mode", themeToLight: "Switch to light mode",
      langLabel: "Switch language / 언어 전환", langButton: "한국어",
      onThisPage: "On this page"
    }
  };

  const KEY_SOLVED = "dsa-hub:solved";
  const KEY_THEME = "dsa-hub:theme";
  const KEY_LANG = "dsa-hub:lang";
  const KEY_CELEBRATED = "dsa-hub:celebrated";

  const readJSON = (key, fallback) => {
    try { return JSON.parse(localStorage.getItem(key)) || fallback; }
    catch (e) { return fallback; }
  };
  const writeJSON = (key, value) => {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* private mode */ }
  };
  const writeRaw = (key, value) => {
    try { localStorage.setItem(key, value); } catch (e) { /* private mode */ }
  };

  let solved = readJSON(KEY_SOLVED, {});
  let celebrated = readJSON(KEY_CELEBRATED, {});
  let lang = "ko";
  let traceRedraw = null;
  const t = () => STR[lang];
  const topicName = (topic) => (lang === "ko" ? topic.ko : topic.en);

  const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const pid = (topic, prob) => topic + "/" + slug(prob.num + "-" + prob.title);

  const topicStats = (topic) => {
    const list = PROBLEMS[topic] || [];
    const done = list.filter((prob) => solved[pid(topic, prob)]).length;
    return { done, total: list.length, pct: list.length ? Math.round((done / list.length) * 100) : 0 };
  };
  const overallStats = () => {
    let done = 0, total = 0;
    visibleTopics().forEach((topic) => {
      const s = topicStats(topic.id);
      done += s.done; total += s.total;
    });
    return { done, total, pct: total ? Math.round((done / total) * 100) : 0 };
  };

  /* ------------------------------------------------------------------
     4. Theme
     ------------------------------------------------------------------ */
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      btn.textContent = theme === "light" ? "☾" : "☀";
      btn.setAttribute("aria-label", theme === "light" ? t().themeToDark : t().themeToLight);
    });
  }
  function initTheme() {
    applyTheme(localStorage.getItem(KEY_THEME) || "dark");
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
        writeRaw(KEY_THEME, next);
        applyTheme(next);
      });
    });
  }

  /* ------------------------------------------------------------------
     5. Language
     Prose lives twice in the HTML, inside [data-lang="ko"] / [data-lang="en"]
     spans, and CSS hides the inactive one. Everything rendered by this
     file is rebuilt here instead.
     ------------------------------------------------------------------ */
  function applyLang(next) {
    lang = next === "en" ? "en" : "ko";
    const root = document.documentElement;
    root.setAttribute("data-lang", lang);
    root.setAttribute("lang", lang === "ko" ? "ko" : "en");
    document.querySelectorAll("[data-lang-toggle]").forEach((btn) => {
      btn.textContent = t().langButton;
      btn.setAttribute("aria-label", t().langLabel);
    });
    applyTheme(root.getAttribute("data-theme") || "dark");
    retranslateStaticUI();
    renderTopicCards();
    renderProblemItems();
    refreshProgress();
    applyFilters();
    if (traceRedraw) traceRedraw();
  }

  function retranslateStaticUI() {
    const search = document.getElementById("problem-search");
    if (search) {
      search.placeholder = t().searchPlaceholder;
      search.setAttribute("aria-label", t().searchLabel);
    }
    const empty = document.getElementById("problem-empty");
    if (empty) empty.textContent = t().empty;
    const random = document.getElementById("random-problem");
    if (random) random.textContent = t().random;
    const reset = document.getElementById("reset-progress");
    if (reset) reset.textContent = t().reset;
    document.querySelectorAll(".filters [data-diff]").forEach((chip) => {
      chip.textContent = t()[chip.dataset.diff];
    });
    document.querySelectorAll(".copy-btn").forEach((btn) => { btn.textContent = t().copy; });
    const tocTitle = document.querySelector(".toc b");
    if (tocTitle) tocTitle.textContent = t().onThisPage;
  }

  function initLang() {
    let stored = "ko";
    try { stored = localStorage.getItem(KEY_LANG) || "ko"; } catch (e) { /* ignore */ }
    applyLang(stored);
    document.querySelectorAll("[data-lang-toggle]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const next = lang === "ko" ? "en" : "ko";
        writeRaw(KEY_LANG, next);
        applyLang(next);
        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
        document.body.animate(
          [{ opacity: 0.55 }, { opacity: 1 }], { duration: 220, easing: "ease-out" });
      });
    });
  }

  /* ------------------------------------------------------------------
     6. Celebration
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
      const meta = topicMeta(topic);
      confetti();
      toast(t().complete(meta ? topicName(meta) : topic, s.total));
    } else if (s.done < s.total && celebrated[topic]) {
      delete celebrated[topic];
      writeJSON(KEY_CELEBRATED, celebrated);
    }
  }

  /* ------------------------------------------------------------------
     7. Problem list
     ------------------------------------------------------------------ */
  function problemNode(topic, prob) {
    const id = pid(topic, prob);
    const li = document.createElement("li");
    li.className = "pitem" + (solved[id] ? " done" : "");
    li.dataset.difficulty = prob.diff.toLowerCase();
    li.dataset.text = (prob.num + " " + prob.title + " " + prob.hintEn + " " +
      prob.hintKo + " " + prob.src).toLowerCase();

    const box = document.createElement("input");
    box.type = "checkbox";
    box.className = "pcheck";
    box.checked = !!solved[id];
    box.id = "chk-" + id;
    box.setAttribute("aria-label", t().markSolved(prob.title));

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
    hint.textContent = lang === "ko" ? prob.hintKo : prob.hintEn;
    body.appendChild(link);
    body.appendChild(hint);

    const meta = document.createElement("div");
    meta.className = "pmeta";
    const diff = document.createElement("span");
    diff.className = "badge " + prob.diff.toLowerCase();
    diff.textContent = t()[prob.diff.toLowerCase()];
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

  function renderProblemItems() {
    const mount = document.getElementById("problem-list");
    const topic = document.body.dataset.topic;
    if (!mount || !topic) return;
    mount.innerHTML = "";
    (PROBLEMS[topic] || []).forEach((prob) => mount.appendChild(problemNode(topic, prob)));
  }

  function applyFilters() {
    const mount = document.getElementById("problem-list");
    if (!mount) return;
    const search = document.getElementById("problem-search");
    const chips = Array.prototype.slice.call(document.querySelectorAll(".filters [data-diff]"));
    const empty = document.getElementById("problem-empty");
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

  function initFilters() {
    const search = document.getElementById("problem-search");
    if (search) search.addEventListener("input", applyFilters);
    const chips = Array.prototype.slice.call(document.querySelectorAll(".filters [data-diff]"));
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
  }

  /* ------------------------------------------------------------------
     8. Progress UI
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
      if (num) num.textContent = t().solved(s.done, s.total);
      if (ring) setRing(ring, s.pct);
    });
    const o = overallStats();
    document.querySelectorAll("[data-overall]").forEach((el) => {
      const kind = el.dataset.overall;
      if (kind === "pct") el.textContent = o.pct + "%";
      else if (kind === "done") el.textContent = o.done;
      else if (kind === "total") el.textContent = o.total;
      else if (kind === "remaining") el.textContent = o.total - o.done;
      else if (kind === "units") el.textContent = visibleTopics().length;
      else if (kind === "topics") {
        el.textContent = visibleTopics().filter((topic) => {
          const s = topicStats(topic.id);
          return s.total && s.done === s.total;
        }).length;
      } else if (kind === "bar") el.style.width = o.pct + "%";
      else if (kind === "ring") setRing(el, o.pct);
    });
  }

  /* ------------------------------------------------------------------
     9. Home page topic cards
     ------------------------------------------------------------------ */
  function ringSVG(pct) {
    return '<svg class="ring" viewBox="0 0 48 48" style="--pct:' + pct + '" aria-hidden="true">' +
      '<circle class="track" cx="24" cy="24" r="20"></circle>' +
      '<circle class="bar" cx="24" cy="24" r="20"></circle>' +
      '<text x="24" y="25" text-anchor="middle">' + pct + '%</text></svg>';
  }
  function renderTopicCards() {
    const grid = document.getElementById("topic-grid");
    if (!grid) return;
    grid.innerHTML = visibleTopics().map((topic) => {
      const s = topicStats(topic.id);
      const step = lang === "ko" ? topic.stepKo : topic.stepEn;
      const title = lang === "ko"
        ? topic.ko + ' <span class="ko">' + topic.en + "</span>"
        : topic.en + ' <span class="ko">' + topic.ko + "</span>";
      return [
        '<a class="card topic-card" href="', topic.file, '" style="--grad: var(--grad-', topic.id,
        ')" data-progress-topic="', topic.id, '">',
        '<div class="topic-head">',
        '<div class="topic-icon">', topic.icon, "</div>",
        '<div><div class="topic-step">', step, "</div>",
        "<h3>", title, "</h3></div>",
        "</div>",
        "<p>", lang === "ko" ? topic.blurbKo : topic.blurbEn, "</p>",
        '<div class="topic-foot">',
        ringSVG(s.pct),
        '<div style="flex:1"><div class="pbar"><span></span></div>',
        '<div class="pnum" style="margin-top:.35rem"></div></div>',
        "</div></a>"
      ].join("");
    }).join("");
  }

  /* ------------------------------------------------------------------
     10. Random problem
     ------------------------------------------------------------------ */
  function initRandom() {
    const btn = document.getElementById("random-problem");
    if (!btn) return;
    btn.addEventListener("click", () => {
      const scope = btn.dataset.topic;
      const pool = [];
      (scope ? [scope] : visibleTopics().map((topic) => topic.id)).forEach((id) => {
        (PROBLEMS[id] || []).forEach((prob) => {
          if (!solved[pid(id, prob)]) pool.push(prob);
        });
      });
      if (!pool.length) { toast(t().allSolved); return; }
      const pick = pool[Math.floor(Math.random() * pool.length)];
      toast("→ " + pick.num + " " + pick.title);
      window.open(pick.url, "_blank", "noopener");
    });
  }

  /* ------------------------------------------------------------------
     11. Reset
     ------------------------------------------------------------------ */
  function initReset() {
    const btn = document.getElementById("reset-progress");
    if (!btn) return;
    btn.addEventListener("click", () => {
      if (!window.confirm(t().resetConfirm)) return;
      solved = {}; celebrated = {};
      writeJSON(KEY_SOLVED, solved);
      writeJSON(KEY_CELEBRATED, celebrated);
      document.querySelectorAll(".pcheck").forEach((box) => {
        box.checked = false;
        box.closest(".pitem").classList.remove("done");
      });
      renderTopicCards();
      refreshProgress();
      toast(t().resetDone);
    });
  }

  /* ------------------------------------------------------------------
     12. In-page table of contents highlighting
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
      targets.forEach((target) => { if (seen.has(target.id) && !current) current = target.id; });
      if (current) links.forEach((a) => a.classList.toggle("active", map[current] === a));
    }, { rootMargin: "-88px 0px -65% 0px", threshold: 0 });
    targets.forEach((target) => io.observe(target));
  }

  /* ------------------------------------------------------------------
     13. Copy buttons
     ------------------------------------------------------------------ */
  function initCopy() {
    document.querySelectorAll(".code-card").forEach((card) => {
      const btn = card.querySelector(".copy-btn");
      const code = card.querySelector("code");
      if (!btn || !code || !navigator.clipboard) { if (btn) btn.style.display = "none"; return; }
      btn.addEventListener("click", () => {
        navigator.clipboard.writeText(code.textContent).then(() => {
          btn.textContent = t().copied;
          setTimeout(() => { btn.textContent = t().copy; }, 1400);
        });
      });
    });
  }

  /* ------------------------------------------------------------------
     14. Sorting trace widget (sorting.html only)
     Each step carries both languages so switching mid-trace works.
     ------------------------------------------------------------------ */
  function bubbleSteps(input) {
    const a = input.slice();
    const steps = [{ arr: a.slice(), locked: 0, cmp: [], swap: [], min: -1, note: {
      ko: "시작. 버블 정렬은 <b>이웃한</b> 두 값을 비교해 순서가 어긋났으면 교환합니다.",
      en: "Start. Bubble sort compares <b>adjacent</b> pairs and swaps them when they are out of order." } }];
    const n = a.length;
    for (let pass = 0; pass < n - 1; pass++) {
      let swapped = false;
      for (let i = 0; i < n - 1 - pass; i++) {
        steps.push({ arr: a.slice(), locked: pass, cmp: [i, i + 1], swap: [], min: -1, note: {
          ko: (pass + 1) + "번째 패스: <b>" + a[i] + "</b>와 <b>" + a[i + 1] + "</b>를 비교합니다.",
          en: "Pass " + (pass + 1) + ": compare <b>" + a[i] + "</b> and <b>" + a[i + 1] + "</b>." } });
        if (a[i] > a[i + 1]) {
          const tmp = a[i]; a[i] = a[i + 1]; a[i + 1] = tmp;
          swapped = true;
          steps.push({ arr: a.slice(), locked: pass, cmp: [], swap: [i, i + 1], min: -1, note: {
            ko: "순서가 어긋났으므로 교환합니다. 큰 값이 계속 오른쪽으로 밀려납니다.",
            en: "Out of order → swap. The larger value keeps moving right." } });
        } else {
          steps.push({ arr: a.slice(), locked: pass, cmp: [], swap: [], min: -1, note: {
            ko: "이미 순서가 맞으므로 교환하지 않고 한 칸 오른쪽으로 갑니다.",
            en: "Already in order → no swap, move one step right." } });
        }
      }
      steps.push({ arr: a.slice(), locked: pass + 1, cmp: [], swap: [], min: -1, note: {
        ko: (pass + 1) + "번째 패스 종료: <b>" + a[n - 1 - pass] + "</b>가 마지막 자리로 떠올랐습니다. " +
            (pass + 1) + "개의 값이 확정되었습니다.",
        en: "End of pass " + (pass + 1) + ": <b>" + a[n - 1 - pass] + "</b> has bubbled to its final slot. " +
            (pass + 1) + " value(s) locked." } });
      if (!swapped) {
        steps.push({ arr: a.slice(), locked: n, cmp: [], swap: [], min: -1, note: {
          ko: "이번 패스에서 교환이 한 번도 없었습니다 → 이미 정렬이 끝났으므로 여기서 멈춥니다 (최선의 경우 O(n)).",
          en: "No swap happened in this pass → the array is already sorted, so we can stop early (best case O(n))." } });
        return steps;
      }
    }
    steps.push({ arr: a.slice(), locked: n, cmp: [], swap: [], min: -1, note: {
      ko: "n−1 = " + (n - 1) + "번의 패스로 정렬이 끝났습니다. 완료!",
      en: "Done after n−1 = " + (n - 1) + " passes. 완료!" } });
    return steps;
  }

  function selectionSteps(input) {
    const a = input.slice();
    const steps = [{ arr: a.slice(), locked: 0, cmp: [], swap: [], min: -1, note: {
      ko: "시작. 선택 정렬은 <b>아직 정렬되지 않은 구간의 최솟값</b>을 찾아 제자리로 보냅니다.",
      en: "Start. Selection sort finds the <b>minimum of the unsorted part</b> and swaps it into place." } }];
    const n = a.length;
    for (let start = 0; start < n - 1; start++) {
      let lo = start;
      steps.push({ arr: a.slice(), locked: start, cmp: [], swap: [], min: lo, note: {
        ko: (start + 1) + "번째 패스: 남은 구간의 최솟값이 <b>" + a[lo] + "</b> (인덱스 " + lo + ")라고 가정합니다.",
        en: "Pass " + (start + 1) + ": assume <b>" + a[lo] + "</b> (index " + lo + ") is the smallest remaining value." } });
      for (let i = start + 1; i < n; i++) {
        steps.push({ arr: a.slice(), locked: start, cmp: [i], swap: [], min: lo, note: {
          ko: "<b>" + a[i] + "</b>를 현재 최솟값 <b>" + a[lo] + "</b>와 비교합니다.",
          en: "Compare <b>" + a[i] + "</b> against the current minimum <b>" + a[lo] + "</b>." } });
        if (a[i] < a[lo]) {
          lo = i;
          steps.push({ arr: a.slice(), locked: start, cmp: [], swap: [], min: lo, note: {
            ko: "더 작습니다 → 새로운 최솟값은 <b>" + a[lo] + "</b>입니다.",
            en: "Smaller → the new minimum is <b>" + a[lo] + "</b>." } });
        }
      }
      if (lo !== start) {
        const tmp = a[start]; a[start] = a[lo]; a[lo] = tmp;
        steps.push({ arr: a.slice(), locked: start, cmp: [], swap: [start, lo], min: -1, note: {
          ko: "최솟값을 인덱스 " + start + "로 교환합니다. 이 패스 전체에서 교환은 <b>단 한 번</b>뿐입니다.",
          en: "Swap the minimum into index " + start + ". That is <b>one</b> swap for the whole pass." } });
      } else {
        steps.push({ arr: a.slice(), locked: start, cmp: [], swap: [], min: -1, note: {
          ko: "최솟값이 이미 인덱스 " + start + "에 있으므로 교환하지 않습니다.",
          en: "The minimum was already in index " + start + " → no swap needed." } });
      }
      steps.push({ arr: a.slice(), locked: start + 1, cmp: [], swap: [], min: -1, note: {
        ko: (start + 1) + "번째 패스 종료: 인덱스 " + start + "가 확정되었습니다.",
        en: "End of pass " + (start + 1) + ": index " + start + " is final." } });
    }
    steps.push({ arr: a.slice(), locked: n, cmp: [], swap: [], min: -1, note: {
      ko: "완료 — 정확히 n−1 = " + (n - 1) + "번의 패스, 교환은 많아야 n−1번이었습니다.",
      en: "Done — exactly n−1 = " + (n - 1) + " passes, and at most n−1 swaps total." } });
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
      steps = algo === "bubble" ? bubbleSteps(parseInput()) : selectionSteps(parseInput());
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
        return '<div class="' + cls + '" style="height:' + h + 'px">' + v + "</div>";
      }).join("");
      noteEl.innerHTML = s.note[lang];
      countEl.textContent = (lang === "ko" ? "단계 " : "step ") + (idx + 1) + " / " + steps.length;
    }
    traceRedraw = function () {
      draw();
      if (!timer) root.querySelector("#trace-play").textContent = lang === "ko" ? "▶ 재생" : "▶ Play";
    };
    function go(delta) {
      idx = Math.min(steps.length - 1, Math.max(0, idx + delta));
      draw();
    }
    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
      root.querySelector("#trace-play").textContent = lang === "ko" ? "▶ 재생" : "▶ Play";
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
      this.textContent = lang === "ko" ? "⏸ 일시정지" : "⏸ Pause";
      timer = setInterval(() => {
        if (idx >= steps.length - 1) { stop(); return; }
        go(1);
      }, 750);
    });
    input.addEventListener("change", () => { stop(); build(); });
    build();
  }

  /* ------------------------------------------------------------------
     15. Fallback Python highlighter
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
     16. Boot
     ------------------------------------------------------------------ */
  function boot() {
    initTheme();
    initFilters();
    initRandom();
    initReset();
    initTOC();
    initCopy();
    initTrace();
    initLang();          // renders cards + problems + progress in the stored language
    if (window.Prism) window.Prism.highlightAll();
    fallbackHighlight();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
