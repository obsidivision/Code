# -*- coding: utf-8 -*-
from _common import *

CQ = '''
class CircularQueue:
    """Fixed-size queue on a Python list, with wrap-around indices.

    Convention used here:
      * `front` points at the slot *before* the first item
      * `rear`  points at the slot holding the last item
      * one slot is deliberately never used, so "full" and "empty" differ
    """

    def __init__(self, capacity):
        self.slots = capacity + 1          # +1 for the sacrificial empty slot
        self.buffer = [None] * self.slots
        self.front = 0
        self.rear = 0

    def is_empty(self):
        return self.front == self.rear

    def is_full(self):
        return self.front == (self.rear + 1) % self.slots

    def size(self):
        # +slots before the modulo keeps the result positive after a wrap
        return (self.rear - self.front + self.slots) % self.slots

    def enqueue(self, item):
        if self.is_full():
            raise IndexError("queue is full")
        self.rear = (self.rear + 1) % self.slots   # step forward, wrapping to 0
        self.buffer[self.rear] = item

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        self.front = (self.front + 1) % self.slots
        item = self.buffer[self.front]
        self.buffer[self.front] = None             # not required, but keeps prints readable
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        return self.buffer[(self.front + 1) % self.slots]

    def display(self):
        """Items in front-to-rear order, without disturbing the queue."""
        out, i = [], self.front
        while i != self.rear:
            i = (i + 1) % self.slots
            out.append(self.buffer[i])
        return out


q = CircularQueue(4)
for name in ["a", "b", "c", "d"]:
    q.enqueue(name)
print(q.display(), q.size(), q.is_full())   # ['a', 'b', 'c', 'd'] 4 True
q.dequeue(); q.dequeue()
q.enqueue("e")                              # reuses the slots 'a' and 'b' vacated
print(q.display(), q.size())                # ['c', 'd', 'e'] 3
'''

RING = '''
class RingBuffer:
    """Keeps only the N most recent items. When it is full the oldest is overwritten."""

    def __init__(self, keep):
        self.buffer = [None] * keep
        self.keep = keep
        self.next = 0        # where the next write goes
        self.count = 0       # how many real items are stored (caps at `keep`)

    def push(self, item):
        self.buffer[self.next] = item              # no "full" check: overwriting is the point
        self.next = (self.next + 1) % self.keep
        self.count = min(self.count + 1, self.keep)

    def recent(self):
        """Stored items, oldest first."""
        start = (self.next - self.count) % self.keep
        return [self.buffer[(start + k) % self.keep] for k in range(self.count)]


log = RingBuffer(3)
for message in ["m1", "m2", "m3", "m4", "m5"]:
    log.push(message)
print(log.recent())          # ['m3', 'm4', 'm5'] - only the last 3 survive
'''

QUEUE = head("큐 (Queue) — DSA 연습 허브",
             "선형 큐가 배열 공간을 낭비하는 이유, 모듈로 연산으로 이를 해결하는 원형 큐, 그리고 링 버퍼.",
             "queue") + page_head(
    "queue",
    "큐는 선입선출입니다. 뒤에서 넣고 앞에서 뺍니다. 창구 앞에 선 줄과 같습니다. "
    "재미있는 부분은 이 규칙 자체가 아니라, 고정 크기 배열 위에서 공간을 낭비하지 않고 이 규칙을 구현하는 방법입니다.",
    "A queue is first-in-first-out: you add at the rear and remove from the front, like a line at a counter. "
    "The interesting part is not the rule — it is making it work on a fixed-size array without wasting space."
) + toc("queue", [("linear", "선형 큐의 문제", "The linear queue problem"),
                  ("circular", "원형으로 만들기", "Going circular"),
                  ("gap", "비워 두는 한 칸", "The sacrificial slot"),
                  ("code", "참고 구현", "Reference implementation"),
                  ("ring", "링 버퍼", "Ring buffers"),
                  ("practice", "연습 문제", "Practice problems")]) + """

<section id="linear" style="--grad: var(--grad-queue)">
  """ + section_title("선형 큐의 문제", "The linear queue problem") + """
  <p>""" + L(
    "칸이 5개인 배열과 인덱스 두 개를 준비합시다. 값이 빠져나가는 자리를 가리키는 <code>front</code>, 값이 들어오는 자리를 가리키는 <code>rear</code>입니다. "
    "enqueue는 <code>rear</code>를 오른쪽으로 옮기고, dequeue는 <code>front</code>를 오른쪽으로 옮깁니다. 간단합니다 — 그리고 고장나 있습니다.",
    "Take an array of 5 slots and two indices: <code>front</code> for where things leave and "
    "<code>rear</code> for where things arrive. Enqueue moves <code>rear</code> right; dequeue moves "
    "<code>front</code> right. Simple — and broken.") + """</p>
  <p>""" + L(
    "다섯 개를 넣은 뒤 세 개를 뺐다고 해 봅시다. 이제 <code>front</code>는 인덱스 3에 있고 <code>rear</code>는 배열의 끝에 닿았습니다. "
    "왼쪽의 세 칸은 비어 있지만 쓸 수 없고, 그런데도 다음 <code>enqueue</code>는 \"가득 찼다\"고 말합니다. "
    "큐가 뒤에 남은 공간을 재사용하지 못하고 배열의 오른쪽 끝으로 <em>기어나가</em> 버린 것입니다.",
    "Enqueue five items, then dequeue three. <code>front</code> is now at index 3 and <code>rear</code> has hit "
    "the end of the array. Three slots at the left are empty and unusable, yet the next "
    "<code>enqueue</code> reports \"full\". The queue has <em>crawled</em> off the right edge of the array "
    "instead of reusing the space behind it.") + """</p>
  <p>""" + L("해결 방법은 두 가지입니다.", "Two ways out:") + """</p>
  <ul>
    <li>""" + L(
      "<strong>dequeue할 때마다 전부 왼쪽으로 밀기.</strong> <code>front</code>를 항상 0에 두는 방법입니다. 맞기는 하지만 dequeue가 O(1)이 아니라 O(n)이 됩니다. 공간 문제를 시간으로 갚은 셈입니다.",
      "<strong>Shift everything left</strong> on every dequeue so <code>front</code> stays at 0. Correct, but each dequeue is now O(n) instead of O(1) — you have paid for the fix with time.") + """</li>
    <li>""" + L(
      "<strong>인덱스가 끝에 닿으면 배열의 처음으로 돌아가게 하기.</strong> 여전히 O(1)이고 자료를 옮기지도 않습니다. 이것이 원형 큐입니다.",
      "<strong>Let the indices wrap around</strong> to the start of the array when they run off the end. Still O(1), no data moves. This is the circular queue.") + """</li>
  </ul>
</section>

<section id="circular" style="--grad: var(--grad-queue)">
  """ + section_title("원형으로 만들기", "Going circular") + """
  <p>""" + L(
    "배열 자체는 아무것도 달라지지 않습니다. 여전히 일렬로 놓인 메모리 덩어리입니다. 달라지는 것은 인덱스를 전진시키는 방식입니다. "
    "<code>rear = rear + 1</code> 대신 이렇게 씁니다.",
    "Nothing about the array changes — it is still a flat block of memory. What changes is how you advance "
    "the indices. Instead of <code>rear = rear + 1</code>, you write:") + """</p>
""" + code("advance.py", '''
front = (front + 1) % capacity
rear  = (rear + 1) % capacity
''') + """
  <p>""" + L(
    "모듈로 연산이 모든 일을 합니다. 인덱스가 마지막 칸에 도달하면 다음 걸음에서 0으로 돌아가므로, 배열은 양쪽 끝이 이어진 고리처럼 동작합니다. "
    "앞에서 <code>dequeue</code>로 비워진 칸을 <code>enqueue</code>가 다시 쓸 수 있고, 두 연산 모두 O(1)을 유지합니다.",
    "The modulo does all the work. When an index reaches the last slot, the next step sends it back to 0, so "
    "the array behaves as if its two ends were joined into a ring. Slots freed by <code>dequeue</code> at the "
    "front become available to <code>enqueue</code> again, and both operations stay O(1).") + """</p>
  <div class="note">
    <b>""" + L("그림을 그려 보면 이해가 빠릅니다.", "Drawing it helps.") + """</b>
    <p>""" + L(
      "배열을 시계 문자판처럼 그리고 테두리에 인덱스를 적어 보세요. <code>front</code>와 <code>rear</code>는 시계 방향으로만 도는 두 개의 바늘이고, "
      "<code>rear</code>는 문자판 위에서 <code>front</code>를 영원히 쫓아다닙니다. 큐에 담긴 내용은 두 바늘 사이의 호(arc)입니다.",
      "Sketch the array as a clock face with the slot indices around the rim. <code>front</code> and "
      "<code>rear</code> are two hands that only ever move clockwise, and <code>rear</code> chases "
      "<code>front</code> around the dial forever. The queue's contents are the arc from one hand to the other.") + """</p>
  </div>
</section>

<section id="gap" style="--grad: var(--grad-queue)">
  """ + section_title("비워 두는 한 칸", "The sacrificial slot") + """
  <p>""" + L(
    "인덱스를 원형으로 돌리면 곤란한 모호함이 하나 생깁니다. 배열을 끝까지 채우면 <code>rear</code>가 <code>front</code>를 따라잡는데, "
    "<code>front == rear</code>는 빈 큐의 모습과 정확히 같습니다. 정반대의 두 상태를 같은 조건식으로 판별하게 되는 것입니다.",
    "Circular indices create one nasty ambiguity. If you fill the array completely, <code>rear</code> catches "
    "up to <code>front</code> — and <code>front == rear</code> is also exactly what an empty queue looks like. "
    "Two opposite states, one identical test.") + """</p>
  <p>""" + L(
    "표준적인 해결책은 마지막 빈 칸 하나를 끝내 쓰지 않는 것입니다. <code>capacity</code>개를 담는 큐에 <code>capacity + 1</code>개의 칸을 잡고, 한 걸음 일찍 \"가득 참\"으로 판정합니다.",
    "The standard fix is to refuse to use the last free slot. Allocate <code>capacity + 1</code> slots for a "
    "queue that holds <code>capacity</code> items, and call it full one step early:") + """</p>
  <div class="kv">
    <div><b>""" + L("비어 있음", "Empty") + """</b><span><code>front == rear</code></span></div>
    <div><b>""" + L("가득 참", "Full") + """</b><span><code>front == (rear + 1) % slots</code></span></div>
    <div><b>""" + L("크기", "Size") + """</b><span><code>(rear - front + slots) % slots</code></span></div>
  </div>
  <p>""" + L(
    "항상 한 칸이 비어 있으므로 두 조건이 동시에 참이 될 수 없습니다. 크기 식에 들어 있는 <code>+ slots</code>는 <code>rear</code>가 0을 넘어 되돌아와 "
    "<code>front</code>보다 숫자가 작아진 경우를 위한 것입니다. 이것이 없으면 음수가 나옵니다.",
    "Because one slot is always left open, the two conditions can never be true at the same time. The "
    "<code>+ slots</code> inside the size formula is there for the case where <code>rear</code> has wrapped "
    "past 0 and is numerically smaller than <code>front</code> — without it you would get a negative count.") + """</p>
  <p>""" + L(
    "다른 방법은 <code>count</code> 필드를 따로 두고 배열 전체를 쓰는 것입니다. 이것도 잘 동작하며, 칸 하나 대신 정수 하나를 더 쓰는 셈입니다. "
    "수업에서 빈 칸 방식을 주로 가르치는 이유는 이 방식이 되돌아오는 인덱스를 직접 따져 보게 만들기 때문입니다.",
    "The alternative is to keep an explicit <code>count</code> field and use the whole array. That works too, "
    "and costs one extra integer instead of one wasted slot. Courses usually teach the empty-slot version "
    "because it forces you to actually reason about the wrap-around.") + """</p>
</section>

<section id="code" style="--grad: var(--grad-queue)">
  """ + section_title("참고 구현", "Reference implementation") + """
""" + code("circular_queue.py", CQ) + """
  <div class="table-scroll">
  <table class="data">
    <thead><tr><th>""" + L("연산", "Operation") + """</th><th>""" + L("비용", "Cost") + """</th><th>""" + L("하는 일", "What it touches") + """</th></tr></thead>
    <tbody>
      <tr><td><code>enqueue</code></td><td>O(1)</td><td>""" + L("<code>rear</code>를 전진시키고 한 칸에 씁니다", "Advances <code>rear</code>, writes one slot") + """</td></tr>
      <tr><td><code>dequeue</code></td><td>O(1)</td><td>""" + L("<code>front</code>를 전진시키고 한 칸을 읽습니다", "Advances <code>front</code>, reads one slot") + """</td></tr>
      <tr><td><code>peek</code></td><td>O(1)</td><td>""" + L("<code>front</code> 다음 칸을 읽기만 하고 아무것도 옮기지 않습니다", "Reads the slot after <code>front</code>, moves nothing") + """</td></tr>
      <tr><td><code>size</code></td><td>O(1)</td><td>""" + L("두 인덱스로 하는 산술 계산뿐입니다", "Pure arithmetic on the two indices") + """</td></tr>
      <tr><td><code>display</code></td><td>O(n)</td><td>""" + L("<code>front</code>에서 <code>rear</code>까지의 호를 따라갑니다", "Walks the arc from <code>front</code> to <code>rear</code>") + """</td></tr>
    </tbody>
  </table>
  </div>
</section>

<section id="ring" style="--grad: var(--grad-queue)">
  """ + section_title("링 버퍼 — 쓸모 있는 변형", "Ring buffers — the useful twist") + """
  <p>""" + L(
    "규칙 하나만 바꾸면 원형 큐는 실제 시스템에서 늘 마주치는 물건이 됩니다. 가득 찼을 때 <strong>새 값을 거절하는 대신 가장 오래된 값을 덮어쓰는</strong> 것입니다.",
    "Change one rule and the circular queue turns into something you will meet constantly in real systems: "
    "when it is full, <strong>do not refuse the new item — overwrite the oldest one</strong>.") + """</p>
  <p>""" + L(
    "그러면 상수 시간, 상수 메모리로 항상 최근 N개만 담고 있는 구조가 됩니다. 최근 채팅 메시지 10개, 최근 로그 100줄, 최근 센서 값 60프레임, 50단계까지만 남기는 실행 취소 기록 같은 것들입니다. "
    "메모리를 새로 잡지도, 값을 밀지도, 크기가 자라지도 않습니다.",
    "That gives you a structure that always holds the N most recent things, in constant time and constant "
    "memory: the last 10 chat messages, the last 100 log lines, the last 60 frames of sensor readings, an "
    "undo history capped at 50 steps. No allocation, no shifting, no growth.") + """</p>
""" + code("ring_buffer.py", RING) + """
  <p>""" + L(
    "<strong>이동 평균</strong>이 대표적인 활용입니다. 최근 N개 값을 링에 담아 두고 합계를 따로 유지하다가, 값을 넣을 때마다 덮어쓸 값을 빼고 새 값을 더합니다. "
    "N이 아무리 커도 평균 계산은 O(1)로 유지됩니다. 아래 목록의 LC 346이 바로 이 문제입니다.",
    "<strong>Moving averages</strong> are the classic application: keep the last N readings in the ring, keep "
    "a running sum, and on each push subtract the value you are about to overwrite and add the new one. The "
    "average stays O(1) no matter how large N is. That is precisely the LC 346 problem in the list below.") + """</p>
</section>

""" + practice_section("queue",
    "여기서는 설계(design) 문제가 가장 중요합니다. LC 622는 사실상 수업에서 만든 그 구조를 영어로 옮겨 놓은 문제입니다.",
    "The design problems are the ones that matter most here — LC 622 is essentially the class exercise, "
    "in English.") + pager(None, ("linked-list.html", "연결 리스트", "Linked List")) + """
</div>
</div>
</main>
""" + foot()
write("queue.html", QUEUE)
