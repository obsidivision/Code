# -*- coding: utf-8 -*-
from _common import *

BUBBLE = '''
def bubble_sort(values):
    """Sort `values` in place with bubble sort. Returns the same list."""
    n = len(values)
    for done in range(n - 1):              # n-1 passes is always enough
        swapped = False
        # after `done` passes the last `done` slots already hold the biggest values,
        # so each pass can stop a little earlier than the previous one
        for i in range(n - 1 - done):
            if values[i] > values[i + 1]:  # strict > keeps equal items in order -> stable
                values[i], values[i + 1] = values[i + 1], values[i]
                swapped = True
        if not swapped:                    # a clean pass means it is already sorted
            break                          # best case becomes O(n)
    return values


print(bubble_sort([5, 4, 3, 2, 1]))        # [1, 2, 3, 4, 5]
'''

SELECTION = '''
def selection_sort(values):
    """Sort `values` in place with selection sort. Returns the same list."""
    n = len(values)
    for start in range(n - 1):
        lowest = start
        for i in range(start + 1, n):      # scan the unsorted remainder
            if values[i] < values[lowest]:
                lowest = i                 # remember *where* the minimum is, do not swap yet
        if lowest != start:
            values[start], values[lowest] = values[lowest], values[start]
    return values                          # at most n-1 swaps for the whole sort


print(selection_sort([5, 4, 3, 2, 1]))     # [1, 2, 3, 4, 5]
'''

BANNER = '<div class="banner"><span>🗓️</span><div>' + L(
    "<b>이번 학기 진도에는 없는 단원입니다.</b> 그래서 상단 메뉴와 홈 화면 목록에서는 숨겨 두었습니다. "
    "내용은 그대로 남아 있으니 이 주소로 언제든 볼 수 있고, 진행률 합계에는 포함되지 않습니다.",
    "<b>This unit is not on the syllabus this semester,</b> so it is hidden from the top menu and the home "
    "page list. The page itself still works at this URL, and its problems are left out of the overall "
    "progress totals.") + '</div></div>'

SORTING = head("정렬 (Sorting) — DSA 연습 허브",
               "버블 정렬과 선택 정렬을 패스 단위로 설명하고, 직접 단계를 밟아 보는 위젯과 연습 문제를 제공합니다.",
               "sorting") + page_head(
    "sorting",
    "데이터를 순서대로 놓는 일은 대부분의 수업에서 가장 먼저 배우는 알고리즘입니다. 정렬해 두면 그 뒤의 거의 모든 작업이 쉬워지기 때문입니다. "
    "먼저 손으로 따라갈 수 있는 두 가지 O(n²) 정렬부터 시작합니다.",
    "Putting data in order is the first algorithm most courses teach, because almost everything else "
    "gets easier once the data is sorted. Start with the two quadratic sorts you can trace by hand.",
    BANNER
) + toc("sorting", [("why", "왜 정렬하는가", "Why sort at all"),
                    ("bubble", "버블 정렬", "Bubble sort"),
                    ("selection", "선택 정렬", "Selection sort"),
                    ("trace", "단계별로 따라가기", "Trace the passes"),
                    ("compare", "둘을 비교하면", "Side by side"),
                    ("next", "다음에 배울 것", "Coming up next"),
                    ("practice", "연습 문제", "Practice problems")]) + """

<section id="why" style="--grad: var(--grad-sorting)">
  """ + section_title("왜 정렬하는가", "Why sort at all") + """
  <p>""" + L(
    "정렬은 자료를 정해진 순서대로 다시 배치하는 일입니다. 작은 값부터 큰 값 순으로, 가나다순으로, 날짜순으로 — 기준은 정하기 나름입니다. "
    "정렬 자체가 목적인 경우는 드뭅니다. <em>다음</em> 단계를 싸게 만들려고 먼저 해 두는 것입니다.",
    "Sorting is rearranging a collection so its items sit in a defined order — smallest to largest, "
    "alphabetically, by date, by whatever key you choose. It is rarely the goal by itself. It is what you do "
    "first so that the <em>next</em> step gets cheap:") + """</p>
  <ul>
    <li>""" + L("<strong>탐색.</strong> 정렬되지 않은 자료에서 값을 찾으려면 전부 확인해야 해서 O(n)입니다. 정렬해 두면 이진 탐색으로 O(log n)에 끝납니다.",
                "<strong>Searching.</strong> Finding a value in unordered data means checking everything, O(n). Once it is sorted you can binary-search it in O(log n).") + """</li>
    <li>""" + L("<strong>구조 파악.</strong> 중복은 서로 이웃하게 되고, 최솟값과 최댓값은 양 끝에, 중앙값은 가운데에 놓입니다.",
                "<strong>Spotting structure.</strong> Duplicates sit next to each other, the minimum and maximum are at the ends, and the median is in the middle.") + """</li>
    <li>""" + L("<strong>병합과 비교.</strong> 정렬된 두 목록은 한 번의 선형 순회로 합칠 수 있지만, 정렬되지 않은 두 목록은 그렇지 않습니다.",
                "<strong>Merging and comparing.</strong> Two sorted lists can be combined in one linear pass; two unsorted ones cannot.") + """</li>
  </ul>
  <p>""" + L(
    "버블 정렬과 선택 정렬은 둘 다 <strong>O(n²)</strong>이라서 큰 입력에 실제로 쓰지는 않습니다. 그래도 배우는 이유는 종이에 손으로 따라갈 수 있을 만큼 짧기 때문이고, "
    "그렇게 따라가 보는 과정이 반복문의 불변식 — \"<code>k</code>번째 패스가 끝난 시점에 내가 확실히 아는 것은 무엇인가?\" — 을 생각하는 훈련이 되기 때문입니다.",
    "Bubble sort and selection sort are both <strong>O(n²)</strong>, so nobody ships them for large inputs. "
    "You learn them because they are short enough to trace on paper, and tracing them is what teaches you to "
    "reason about loop invariants — \"after pass <code>k</code>, what do I know for certain?\"") + """</p>
</section>

<section id="bubble" style="--grad: var(--grad-sorting)">
  """ + section_title("버블 정렬", "Bubble sort") + """
  <p>""" + L(
    "배열을 따라가면서 각 원소를 바로 오른쪽 원소와 비교합니다. 순서가 어긋나 있으면 교환합니다. 왼쪽 끝에서 오른쪽 끝까지 한 번 지나가는 것을 <strong>패스</strong>라고 부릅니다.",
    "Walk along the array comparing each item with the one directly to its right. If the pair is out of order, "
    "swap it. One walk from left to right is called a <strong>pass</strong>.") + """</p>
  <p>""" + L(
    "핵심은 이것입니다. 한 패스를 도는 동안 만나는 가장 큰 값은 계속 오른쪽으로 교환되며 멈추지 않습니다. 그래서 패스가 끝날 때쯤이면 그 값은 마지막 칸, 즉 자기 자리에 도착해 있습니다. "
    "패스마다 남은 값 중 가장 큰 값이 끝으로 \"떠오릅니다\". 이를 반복하되, 각 패스는 직전 패스보다 한 칸 일찍 멈춰도 됩니다. 많아야 <code>n − 1</code>번의 패스면 전부 정렬됩니다.",
    "The key observation: during a pass, the largest value you meet keeps getting swapped rightward and never "
    "stops, so by the end of the pass it is sitting in the last slot — its final position. The largest unsorted "
    "value \"bubbles\" to the end every pass. Repeat, and each pass can stop one slot earlier than the last one. "
    "After at most <code>n − 1</code> passes everything is in place.") + """</p>
  <div class="kv">
    <div><b>""" + L("시간 복잡도", "Time") + """</b><span>""" + L("평균·최악 O(n²) · 조기 종료를 넣으면 최선 O(n)", "O(n²) average and worst · O(n) best, with early exit") + """</span></div>
    <div><b>""" + L("교환 횟수", "Swaps") + """</b><span>""" + L("최대 O(n²)번 — 이웃끼리의 짧은 교환이 많습니다", "Up to O(n²) — many small adjacent swaps") + """</span></div>
    <div><b>""" + L("추가 메모리", "Extra memory") + """</b><span>""" + L("O(1) — 제자리 정렬", "O(1) — sorts in place") + """</span></div>
    <div><b>""" + L("안정 정렬인가?", "Stable?") + """</b><span>""" + L("예. 교환 조건을 엄격한 <code>&gt;</code>로 두면 그렇습니다", "Yes, if you only swap on a strict <code>&gt;</code>") + """</span></div>
  </div>
""" + code("bubble_sort.py", BUBBLE) + """
  <div class="note">
    <b>""" + L("조기 종료 플래그가 중요합니다.", "The early-exit flag matters.") + """</b>
    <p>""" + L(
    "한 패스 동안 교환이 한 번도 일어나지 않았다면 이웃한 모든 쌍이 이미 제 순서라는 뜻이고, 그것은 곧 배열 전체가 정렬되었다는 뜻이므로 멈춰도 됩니다. "
    "이 덕분에 최선의 경우가 한 번의 O(n) 패스로 끝납니다. 플래그가 없으면 이미 정렬된 자료에도 버블 정렬은 O(n²)입니다.",
    "If a whole pass makes zero swaps, every adjacent pair is already in order — which means the entire array "
    "is sorted, and you can stop. That is what turns the best case into a single O(n) pass. Without the flag, "
    "bubble sort is O(n²) even on data that was already sorted.") + """</p>
  </div>
</section>

<section id="selection" style="--grad: var(--grad-sorting)">
  """ + section_title("선택 정렬", "Selection sort") + """
  <p>""" + L(
    "전략은 다르지만 비용은 같습니다. 배열을 정렬이 끝난 앞부분(처음에는 비어 있습니다)과 아직 정렬되지 않은 나머지로 나누어 생각합니다. "
    "패스마다 나머지 전체를 훑어 가장 작은 값을 찾고, 그 값을 나머지의 첫 칸으로 교환해 넣습니다. 정렬된 앞부분이 왼쪽에서 오른쪽으로 한 칸씩 자랍니다.",
    "Different strategy, same quadratic cost. Treat the array as a sorted prefix (empty at the start) and an "
    "unsorted remainder. Each pass scans the whole remainder, finds the smallest value in it, and swaps that "
    "value into the first slot of the remainder. The sorted prefix grows by one, left to right.") + """</p>
  <p>""" + L(
    "안쪽 반복문이 하는 일을 눈여겨보세요. 지금까지 찾은 최솟값의 <em>인덱스</em>만 기억할 뿐입니다. 훑기가 끝나기 전에는 아무것도 움직이지 않고, 끝난 뒤에 많아야 한 번 교환합니다. "
    "이것이 버블 정렬과의 진짜 차이입니다. 비교 횟수는 비슷하지만 쓰기 횟수가 훨씬 적습니다.",
    "Notice what the inner loop does: it only tracks the <em>index</em> of the smallest value found so far. "
    "Nothing moves until the scan is finished, and then at most one swap happens. That is the real difference "
    "from bubble sort — same number of comparisons, far fewer writes.") + """</p>
  <div class="kv">
    <div><b>""" + L("시간 복잡도", "Time") + """</b><span>""" + L("항상 O(n²) — 훑는 범위가 줄지 않아 최선의 경우가 없습니다", "O(n²) always — no best case, the scan never shortens") + """</span></div>
    <div><b>""" + L("교환 횟수", "Swaps") + """</b><span>""" + L("많아야 n − 1번 — 패스당 한 번", "At most n − 1 — one per pass") + """</span></div>
    <div><b>""" + L("추가 메모리", "Extra memory") + """</b><span>""" + L("O(1) — 제자리 정렬", "O(1) — sorts in place") + """</span></div>
    <div><b>""" + L("안정 정렬인가?", "Stable?") + """</b><span>""" + L("아니요 — 멀리 떨어진 교환이 같은 값의 순서를 뒤집을 수 있습니다", "No — a long-distance swap can jump equal items past each other") + """</span></div>
  </div>
""" + code("selection_sort.py", SELECTION) + """
  <div class="note">
    <b>""" + L("왜 불안정할까요?", "Why is it unstable?") + """</b>
    <p>""" + L(
    "<code>[3a, 3b, 1]</code>을 정렬해 봅시다. 첫 패스에서 <code>1</code>을 찾아 0번 칸의 값과 교환하는데, 그 값이 바로 <code>3a</code>입니다. "
    "그래서 <code>3a</code>는 맨 오른쪽으로 던져져 <code>3b</code>보다 <em>뒤에</em> 놓입니다. 값이 같은 두 원소의 상대 순서가 바뀐 것이고, 이것이 바로 \"불안정\"의 의미입니다. "
    "버블 정렬은 이웃끼리만 교환하므로 이런 일이 생기지 않습니다.",
    "Sort <code>[3a, 3b, 1]</code>. The first pass finds <code>1</code> and swaps it with the value in slot 0, "
    "which is <code>3a</code> — so <code>3a</code> is thrown to the far right, landing <em>after</em> "
    "<code>3b</code>. Two equal keys changed their relative order, which is exactly what \"unstable\" means. "
    "Bubble sort never does this, because it only ever swaps neighbours.") + """</p>
  </div>
</section>

<section id="trace" style="--grad: var(--grad-sorting)">
  """ + section_title("단계별로 따라가기", "Trace the passes") + """
  <p>""" + L(
    "직접 한 단계씩 넘겨 보세요. <span class=\"swatch\" style=\"background:var(--grad-queue)\"></span> 비교 중인 두 값 &nbsp;·&nbsp; "
    "<span class=\"swatch\" style=\"background:var(--grad-sorting)\"></span> 방금 교환된 값 &nbsp;·&nbsp; "
    "<span class=\"swatch\" style=\"background:var(--grad-graph)\"></span> 현재 최솟값(선택 정렬) &nbsp;·&nbsp; "
    "<span class=\"swatch\" style=\"background:var(--ok)\"></span> 자리가 확정된 값.",
    "Step through it. <span class=\"swatch\" style=\"background:var(--grad-queue)\"></span> the pair being compared &nbsp;·&nbsp; "
    "<span class=\"swatch\" style=\"background:var(--grad-sorting)\"></span> a swap just happened &nbsp;·&nbsp; "
    "<span class=\"swatch\" style=\"background:var(--grad-graph)\"></span> the current minimum (selection sort) &nbsp;·&nbsp; "
    "<span class=\"swatch\" style=\"background:var(--ok)\"></span> locked in its final position.") + """</p>
  <div class="card widget" id="trace-widget">
    <div class="widget-controls">
      <button class="chip" type="button" data-algo="bubble" aria-pressed="true">""" + L("버블 정렬", "Bubble sort") + """</button>
      <button class="chip" type="button" data-algo="selection" aria-pressed="false">""" + L("선택 정렬", "Selection sort") + """</button>
      <input class="search" id="trace-input" style="flex:0 1 190px" value="5, 4, 3, 2, 1"
             aria-label="정렬할 배열 (숫자 2~9개) / Array to trace">
      <button class="chip" type="button" id="trace-prev">""" + L("‹ 이전", "‹ Prev") + """</button>
      <button class="chip" type="button" id="trace-play">▶ 재생</button>
      <button class="chip" type="button" id="trace-next">""" + L("다음 ›", "Next ›") + """</button>
      <button class="chip" type="button" id="trace-reset">""" + L("↺ 초기화", "↺ Reset") + """</button>
      <span class="step-count"></span>
    </div>
    <div class="bars"></div>
    <p class="trace-note"></p>
  </div>
  <p style="font-size:.86rem;color:var(--text-faint)">""" + L(
    "버블 정렬에 <code>1, 2, 3, 4, 5</code>를 넣어 보면 패스 한 번 만에 조기 종료가 걸리는 것을 볼 수 있습니다. "
    "같은 입력을 선택 정렬에 넣으면 그런 것과 상관없이 모든 패스를 끝까지 돕니다.",
    "Try <code>1, 2, 3, 4, 5</code> on bubble sort to watch the early exit fire after a single pass — "
    "then try the same input on selection sort, which grinds through every pass regardless.") + """</p>
</section>

<section id="compare" style="--grad: var(--grad-sorting)">
  """ + section_title("둘을 비교하면", "Side by side") + """
  <div class="table-scroll">
  <table class="data">
    <thead><tr><th>&nbsp;</th><th>""" + L("버블 정렬", "Bubble sort") + """</th><th>""" + L("선택 정렬", "Selection sort") + """</th></tr></thead>
    <tbody>
      <tr><td><strong>""" + L("아이디어", "Idea") + """</strong></td><td>""" + L("어긋난 이웃 쌍을 계속 교환한다", "Swap adjacent pairs until nothing is out of order") + """</td><td>""" + L("남은 구간의 최솟값을 찾아 제자리로 보낸다", "Find the minimum of the remainder, swap it into place") + """</td></tr>
      <tr><td><strong>""" + L("비교 횟수", "Comparisons") + """</strong></td><td>~n²/2</td><td>""" + L("~n²/2 (항상)", "~n²/2 (always)") + """</td></tr>
      <tr><td><strong>""" + L("교환 횟수", "Swaps") + """</strong></td><td>0 … ~n²/2</td><td>""" + L("많아야 n − 1", "at most n − 1") + """</td></tr>
      <tr><td><strong>""" + L("최선의 경우", "Best case") + """</strong></td><td>""" + L("조기 종료를 넣으면 O(n)", "O(n) with the early-exit flag") + """</td><td>""" + L("O(n²) — 지름길이 없습니다", "O(n²) — no shortcut exists") + """</td></tr>
      <tr><td><strong>""" + L("안정성", "Stable") + """</strong></td><td>""" + L("있음", "Yes") + """</td><td>""" + L("없음", "No") + """</td></tr>
      <tr><td><strong>""" + L("유리한 상황", "Good when") + """</strong></td><td>""" + L("자료가 거의 정렬되어 있을 때", "Data is nearly sorted already") + """</td><td>""" + L("메모리에 쓰는 비용이 클 때", "Writing to memory is expensive") + """</td></tr>
    </tbody>
  </table>
  </div>
  <p>""" + L(
    "비교 횟수는 대체로 비슷합니다. 비교가 비싼 작업이라면 둘은 비슷하고, <em>자료를 옮기는</em> 일이 비싸다면 선택 정렬이 확실히 유리합니다.",
    "Both do roughly the same number of comparisons. If comparing is the expensive part, they tie; if "
    "<em>moving</em> data is expensive, selection sort wins clearly.") + """</p>
</section>

<section id="next" style="--grad: var(--grad-sorting)">
  """ + section_title("다음에 배울 것", "Coming up next") + """
  <p>""" + L("이 단원은 뒤에 두 가지 정렬이 더 이어집니다. 이름이 낯설지 않도록 한 줄씩 미리 적어 둡니다.",
             "Your course continues through this unit — here is a one-line preview of each, so the names are not new when they arrive.") + """</p>
  <div class="kv">
    <div><b>삽입 정렬 · Insertion sort</b><span>""" + L(
      "다음 원소를 집어 이미 정렬된 앞부분 안으로 뒤에서부터 밀어 넣습니다. O(n²)이지만 거의 정렬된 자료에는 실제로 빠르고 안정 정렬입니다. "
      "<a href=\"https://leetcode.com/problems/insertion-sort-list/\" target=\"_blank\" rel=\"noopener\">LC 147 Insertion Sort List</a>로 연습해 보세요.",
      "Take the next item and slide it backwards into its place in the already-sorted prefix. O(n²), but genuinely fast on nearly-sorted data and stable. "
      "Drill it on <a href=\"https://leetcode.com/problems/insertion-sort-list/\" target=\"_blank\" rel=\"noopener\">LC 147 Insertion Sort List</a>.") + """</span></div>
    <div><b>퀵 정렬 · Quicksort</b><span>""" + L(
      "기준값(피벗)을 하나 고르고 그보다 작은 값은 왼쪽, 큰 값은 오른쪽으로 분할한 뒤 양쪽에 대해 같은 일을 반복합니다. 평균 O(n log n), 최악 O(n²)입니다. "
      "<a href=\"https://leetcode.com/problems/sort-an-array/\" target=\"_blank\" rel=\"noopener\">LC 912</a>와 "
      "<a href=\"https://leetcode.com/problems/kth-largest-element-in-an-array/\" target=\"_blank\" rel=\"noopener\">LC 215</a>로 연습해 보세요.",
      "Pick a pivot, partition everything smaller to its left and larger to its right, then recurse on both sides. O(n log n) average, O(n²) worst. "
      "Drill it on <a href=\"https://leetcode.com/problems/sort-an-array/\" target=\"_blank\" rel=\"noopener\">LC 912 Sort an Array</a> and "
      "<a href=\"https://leetcode.com/problems/kth-largest-element-in-an-array/\" target=\"_blank\" rel=\"noopener\">LC 215 Kth Largest Element</a>.") + """</span></div>
  </div>
</section>

""" + practice_section("sorting",
    "쉬움 → 보통 → 어려움 순입니다. 앞쪽은 순서를 알아보는 문제이고, 뒤로 갈수록 라이브러리 함수를 부르는 대신 정렬 전략을 직접 고르게 만듭니다.",
    "Ordered Easy → Medium → Hard. The first few are about recognising order; the later ones make you "
    "choose a sorting strategy rather than call a library function.") + pager(
        None, ("queue.html", "큐", "Queue")) + """
</div>
</div>
</main>
""" + foot()
write("sorting.html", SORTING)
