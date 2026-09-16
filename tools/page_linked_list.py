# -*- coding: utf-8 -*-
from _common import *

NODE = '''
class Node:
    """One link in the chain: a payload plus a reference to whatever comes next."""

    def __init__(self, data, link=None):
        self.data = data
        self.link = link          # another Node, or None at the end of the list


class LinkedList:
    def __init__(self):
        self.head = None          # None means "empty list"

    def push_front(self, data):
        """Insert at the head - O(1), no shifting of anything."""
        self.head = Node(data, self.head)

    def find(self, target):
        """Return the first node holding `target`, or None. O(n) - you must walk."""
        cur = self.head
        while cur is not None:
            if cur.data == target:
                return cur
            cur = cur.link        # the one line that defines traversal
        return None

    def to_list(self):
        out, cur = [], self.head
        while cur is not None:
            out.append(cur.data)
            cur = cur.link
        return out

    def __len__(self):
        n, cur = 0, self.head
        while cur is not None:
            n += 1
            cur = cur.link
        return n                  # O(n): there is no stored length to read
'''

MIDDLE = '''
    def insert_after(self, before, data):
        """Insert `data` directly after the node `before`.

        Order matters: point the new node at the rest of the list *first*,
        otherwise you overwrite `before.link` and lose the tail.
        """
        before.link = Node(data, before.link)

    def delete_after(self, before):
        """Unlink the node following `before` and return its data."""
        victim = before.link
        if victim is None:
            return None
        before.link = victim.link      # route around the victim
        victim.link = None             # optional: leave no dangling reference
        return victim.data

    def insert_after_value(self, target, data):
        """Walk to the node holding `target`, then insert behind it."""
        before = self.find(target)
        if before is None:
            raise ValueError("no node holds " + repr(target))
        self.insert_after(before, data)


numbers = LinkedList()
for value in [30, 20, 10]:
    numbers.push_front(value)          # -> 10 -> 20 -> 30
numbers.insert_after_value(20, 25)     # -> 10 -> 20 -> 25 -> 30
print(numbers.to_list())               # [10, 20, 25, 30]
'''

LSTACK = '''
class LinkedStack:
    """A stack where `top` is just the head of a linked list."""

    def __init__(self):
        self.top = None

    def push(self, data):
        self.top = Node(data, self.top)      # new node becomes the head - O(1)

    def pop(self):
        if self.top is None:
            raise IndexError("stack is empty")
        node = self.top
        self.top = node.link                 # head moves one step down - O(1)
        return node.data

    def peek(self):
        if self.top is None:
            raise IndexError("stack is empty")
        return self.top.data

    def is_empty(self):
        return self.top is None


s = LinkedStack()
for ch in "ABC":
    s.push(ch)
print(s.pop(), s.pop(), s.peek())    # C B A
'''

LQUEUE = '''
class LinkedCircularQueue:
    """Circular linked queue holding a *tail* pointer only.

    Because the last node links back to the first, `tail.link` is always the
    front. One pointer therefore gives O(1) access to both ends.
    """

    def __init__(self):
        self.tail = None

    def is_empty(self):
        return self.tail is None

    def enqueue(self, data):
        node = Node(data)
        if self.tail is None:
            node.link = node             # a one-node ring points at itself
        else:
            node.link = self.tail.link   # new node takes over as the last node,
            self.tail.link = node        # still pointing at the front
        self.tail = node

    def dequeue(self):
        if self.tail is None:
            raise IndexError("queue is empty")
        front = self.tail.link
        if front is self.tail:           # last remaining node
            self.tail = None
        else:
            self.tail.link = front.link  # skip the old front
        front.link = None
        return front.data

    def to_list(self):
        if self.tail is None:
            return []
        out, cur = [], self.tail.link
        while True:
            out.append(cur.data)
            if cur is self.tail:
                return out
            cur = cur.link


q = LinkedCircularQueue()
for name in ["a", "b", "c"]:
    q.enqueue(name)
print(q.to_list(), q.dequeue(), q.to_list())   # ['a', 'b', 'c'] a ['b', 'c']
'''

LL = head("연결 리스트 (Linked List) — DSA 연습 허브",
          "노드와 링크, 배열과의 비교, 연결 리스트로 만든 스택과 원형 큐, 그리고 중간 삽입·삭제.",
          "linked-list") + page_head(
    "linked-list",
    "배열은 원소들을 하나의 연속된 덩어리에 담아 둡니다. 연결 리스트는 그 덩어리를 포기합니다. 각 원소가 따로 떨어진 객체가 되고, 대신 모든 원소가 다음 원소의 주소를 들고 있습니다. "
    "나머지는 전부 여기서 따라 나옵니다.",
    "An array keeps its items in one contiguous block. A linked list gives up that block: each item is its "
    "own object, and every item stores the address of the next one. Everything else follows from that."
) + toc("linked-list", [("nodes", "노드와 링크", "Nodes and links"),
                        ("vs-array", "배열과 비교하면", "Versus arrays"),
                        ("flavors", "세 가지 형태", "Three flavours"),
                        ("code", "참고 구현", "Reference implementation"),
                        ("middle", "중간 삽입과 삭제", "Insert and delete"),
                        ("stack", "리스트로 만든 스택", "Stack on a list"),
                        ("cqueue", "리스트로 만든 원형 큐", "Circular queue on a list"),
                        ("practice", "연습 문제", "Practice problems")]) + """

<section id="nodes" style="--grad: var(--grad-linked-list)">
  """ + section_title("노드와 링크", "Nodes and links") + """
  <p>""" + L(
    "연결 리스트는 <strong>노드</strong>로 이루어집니다. 각 노드는 두 가지를 담습니다. 실제로 쓰려는 값(<code>data</code>)과 다음 노드를 가리키는 참조"
    "(<code>link</code>, 흔히 <code>next</code>라고도 합니다)입니다. <code>head</code>라는 변수 하나가 첫 노드를 가리킵니다. "
    "마지막 노드의 링크는 <code>None</code>이고, 그것으로 끝에 도달했음을 압니다.",
    "A linked list is made of <strong>nodes</strong>. Each node holds two things: the value you care about "
    "(<code>data</code>) and a reference to the next node (<code>link</code>, often called <code>next</code>). "
    "A single variable, <code>head</code>, points at the first node. The final node's link is "
    "<code>None</code>, which is how you know you have reached the end.") + """</p>
  <p>""" + L("순회는 언제나 똑같은 세 줄입니다.", "Traversal is the same three lines every single time:") + """</p>
""" + code("traverse.py", '''
cur = head
while cur is not None:
    print(cur.data)
    cur = cur.link      # "follow the link" - the whole idea in one statement
''') + """
  <p>""" + L(
    "노드들은 메모리 어디에, 어떤 순서로 놓여 있어도 상관없습니다. 각 노드가 다음 노드의 주소를 알고 있다는 사실만으로 사슬이 존재합니다. "
    "<code>head</code>를 잃어버리면 노드들이 전부 그대로 남아 있어도 리스트 전체에 닿을 수 없게 됩니다.",
    "The nodes can sit anywhere in memory, in any order. The chain exists only because each node knows the "
    "address of the next. Lose <code>head</code> and the whole list becomes unreachable, even though every "
    "node is still there.") + """</p>
</section>

<section id="vs-array" style="--grad: var(--grad-linked-list)">
  """ + section_title("배열과 비교하면", "Versus arrays") + """
  <div class="table-scroll">
  <table class="data">
    <thead><tr><th>&nbsp;</th><th>""" + L("배열 / 파이썬 리스트", "Array / Python list") + """</th><th>""" + L("연결 리스트", "Linked list") + """</th></tr></thead>
    <tbody>
      <tr><td><strong>""" + L("<em>i</em>번째 원소 접근", "Access item <em>i</em>") + """</strong></td><td>""" + L("O(1) — 주소를 계산하면 됩니다", "O(1) — compute the address") + """</td><td>""" + L("O(n) — head부터 걸어가야 합니다", "O(n) — walk from the head") + """</td></tr>
      <tr><td><strong>""" + L("맨 앞에 삽입", "Insert at the front") + """</strong></td><td>""" + L("O(n) — 뒤를 전부 오른쪽으로 밉니다", "O(n) — shift everything right") + """</td><td>""" + L("O(1) — 노드 하나 만들고 대입 한 번", "O(1) — one new node, one reassignment") + """</td></tr>
      <tr><td><strong>""" + L("알고 있는 노드 삭제", "Delete a known node") + """</strong></td><td>""" + L("O(n) — 뒤를 전부 왼쪽으로 당깁니다", "O(n) — shift everything left") + """</td><td>""" + L("O(1) — 링크 하나만 돌리면 됩니다", "O(1) — reroute one link") + """</td></tr>
      <tr><td><strong>""" + L("크기 결정 시점", "Size decided") + """</strong></td><td>""" + L("미리 (고정 배열의 경우)", "Up front (in a fixed array)") + """</td><td>""" + L("정하지 않음 — 노드 단위로 자랍니다", "Never — grows node by node") + """</td></tr>
      <tr><td><strong>""" + L("원소당 메모리", "Memory per item") + """</strong></td><td>""" + L("값만", "Just the value") + """</td><td>""" + L("값 + 노드마다 참조 하나", "Value + one reference per node") + """</td></tr>
      <tr><td><strong>""" + L("캐시 효율", "Cache behaviour") + """</strong></td><td>""" + L("좋음 — 연속되어 있습니다", "Great — contiguous") + """</td><td>""" + L("나쁨 — 노드가 흩어져 있습니다", "Poor — nodes scattered") + """</td></tr>
    </tbody>
  </table>
  </div>
  <div class="note">
    <b>""" + L("삽입·삭제 줄을 꼼꼼히 읽으세요.", "Read the insert/delete row carefully.") + """</b>
    <p>""" + L(
      "\"삭제가 O(1)\"이라는 말은 지우려는 노드의 <em>바로 앞 노드를 이미 손에 쥐고 있다</em>는 전제 위에 있습니다. 값만 알고 있다면 먼저 찾아야 하고, 찾는 일은 O(n)입니다. "
      "연결 리스트가 싸게 만들어 주는 것은 편집이지 탐색이 아닙니다.",
      "\"O(1) to delete\" assumes you are <em>already holding</em> the node before the one you want to remove. "
      "If you only know the value, you first have to find it, and finding is O(n). Linked lists make the "
      "editing cheap, not the searching.") + """</p>
  </div>
</section>

<section id="flavors" style="--grad: var(--grad-linked-list)">
  """ + section_title("세 가지 형태", "Three flavours") + """
  <div class="kv">
    <div><b>단순 연결 리스트 · Singly linked</b><span>""" + L(
      "노드마다 앞으로 향하는 링크 하나. 마지막 노드는 <code>None</code>을 가리킵니다. 가장 저렴하고, 이 페이지에서 자세히 구현하는 형태입니다.",
      "One link per node, pointing forward. The last node links to <code>None</code>. Cheapest, and the one implemented in depth here.") + """</span></div>
    <div><b>원형 연결 리스트 · Circularly linked</b><span>""" + L(
      "마지막 노드가 <code>None</code> 대신 첫 노드를 가리킵니다. 끝이 없으므로 출발한 자리로 돌아오면 멈춥니다. 돌아가며 차례를 주는 구조에 잘 맞습니다.",
      "The last node links back to the first instead of to <code>None</code>. There is no end — you stop when you arrive back where you started. Perfect for round-robin turn taking.") + """</span></div>
    <div><b>이중 연결 리스트 · Doubly linked</b><span>""" + L(
      "노드가 <code>next</code>뿐 아니라 <code>prev</code>도 들고 있어서 뒤로도 걸어갈 수 있고, 지금 서 있는 노드를 앞 노드를 몰라도 지울 수 있습니다. 대신 노드마다 참조를 하나 더 씁니다.",
      "Each node stores <code>prev</code> as well as <code>next</code>, so you can walk backwards and delete a node you are standing on without knowing its predecessor. Costs one more reference per node.") + """</span></div>
  </div>
</section>

<section id="code" style="--grad: var(--grad-linked-list)">
  """ + section_title("참고 구현", "Reference implementation") + """
""" + code("linked_list.py", NODE) + """
  <p>""" + L(
    "<code>__len__</code>을 보세요. 길이를 따로 저장해 두지 않았으므로 세려면 걸어가야 합니다. <code>len()</code>을 자주 쓸 거라면 카운터 필드를 두고 삽입·삭제마다 갱신하세요.",
    "Note <code>__len__</code>: the length is not stored anywhere, so counting means walking. If you need "
    "<code>len()</code> often, keep a counter field and update it in every insert and delete.") + """</p>
</section>

<section id="middle" style="--grad: var(--grad-linked-list)">
  """ + section_title("중간 삽입과 삭제", "Insert and delete in the middle") + """
  <p>""" + L(
    "두 연산 모두 목표 위치의 <em>바로 앞</em> 노드를 기준으로 표현합니다. 고전적인 <code>insertNode(before, data)</code> / <code>deleteNode(before)</code> 짝입니다. "
    "단순 연결 리스트의 노드는 뒤를 볼 수 없으므로, 앞 노드가 우리가 가진 유일한 손잡이입니다.",
    "Both operations are expressed relative to the node <em>before</em> the position you care about — the "
    "classic <code>insertNode(before, data)</code> / <code>deleteNode(before)</code> pair. A singly linked "
    "node cannot see backwards, so the predecessor is the only handle you have.") + """</p>
  <p><strong>""" + L("<code>before</code> 뒤에 삽입하기:", "Insert after <code>before</code>:") + """</strong></p>
  <ol>
    <li>""" + L("새 노드를 만듭니다.", "Make a new node.") + """</li>
    <li>""" + L("새 노드의 링크를 <code>before.link</code>(지금의 나머지 리스트)로 향하게 합니다.", "Point the new node's link at <code>before.link</code> (the current rest of the list).") + """</li>
    <li>""" + L("<code>before.link</code>가 새 노드를 가리키게 합니다.", "Point <code>before.link</code> at the new node.") + """</li>
  </ol>
  <p>""" + L(
    "2번과 3번의 순서를 바꾸면 안 됩니다. <code>before.link</code>를 먼저 덮어쓰면 나머지 리스트로 가는 유일한 참조를 버리게 됩니다. "
    "파이썬에서는 <code>Node(data, before.link)</code>가 생성자 안에서 2번을 처리해 주므로 순서를 틀리기 어렵습니다.",
    "Steps 2 and 3 cannot be swapped. Overwrite <code>before.link</code> first and you have thrown away the "
    "only reference to the rest of the list. In Python, <code>Node(data, before.link)</code> does step 2 "
    "inside the constructor, which makes the correct order hard to get wrong.") + """</p>
  <p>""" + L(
    "<strong><code>before</code> 뒤를 삭제하기:</strong> <code>before.link</code>가 지울 노드를 건너뛰어 <code>victim.link</code>를 가리키게 합니다. "
    "그러면 그 노드에는 닿을 수 없게 되고 파이썬이 알아서 회수합니다.",
    "<strong>Delete after <code>before</code>:</strong> point <code>before.link</code> past the victim, at "
    "<code>victim.link</code>. The victim is now unreachable and Python reclaims it.") + """</p>
""" + code("linked_list.py (continued)", MIDDLE) + """
</section>

<section id="stack" style="--grad: var(--grad-linked-list)">
  """ + section_title("연결 리스트로 만든 스택", "A stack built on a linked list") + """
  <p>""" + L(
    "스택은 후입선출이라 push와 pop이 모두 한쪽 끝에서만 일어납니다. 연결 리스트의 head 쪽은 두 연산 모두 O(1)이므로 스택은 거의 공짜입니다. "
    "<code>head</code>를 <code>top</code>으로 이름만 바꾸면 끝입니다. 용량 제한도, 크기 재조정도, 버려지는 칸도 없습니다.",
    "A stack is last-in-first-out: push and pop both happen at one end. A linked list's head end is O(1) for "
    "both, so a stack is almost free — rename <code>head</code> to <code>top</code> and you are done. No "
    "capacity limit, no resizing, no wasted slots.") + """</p>
""" + code("linked_stack.py", LSTACK) + """
</section>

<section id="cqueue" style="--grad: var(--grad-linked-list)">
  """ + section_title("연결 리스트로 만든 원형 큐", "A circular queue built on a linked list") + """
  <p>""" + L(
    "큐는 양쪽 끝이 모두 필요합니다. 앞에서 빼고 뒤에서 넣습니다. 매번 뒤까지 걸어가면 O(n)이 되므로, 평범한 리스트라면 포인터를 두 개 둬야 합니다.",
    "A queue needs both ends: remove from the front, add at the rear. Walking to the rear each time would be "
    "O(n), so a plain list would need two pointers.") + """</p>
  <p>""" + L(
    "리스트를 <strong>원형</strong>으로 만들면 — 마지막 노드가 첫 노드를 가리키게 하면 — 포인터 하나로 충분합니다. <code>tail</code>만 들고 있으면 "
    "<code>tail.link</code>가 정의상 맨 앞 노드이므로, 양쪽 끝이 모두 한 걸음 거리에 있고 두 연산 다 O(1)입니다.",
    "Make the list <strong>circular</strong> — the last node links back to the first — and one pointer does "
    "the job. Keep only <code>tail</code>. Then <code>tail.link</code> is, by definition, the front node, so "
    "both ends are one step away and both operations are O(1).") + """</p>
""" + code("linked_circular_queue.py", LQUEUE) + """
  <div class="note">
    <b>""" + L("2단원과 비교해 보세요.", "Compare with Unit 02.") + """</b>
    <p>""" + L(
      "배열 버전은 저장 공간이 고정이라 모듈로 연산과 버리는 칸 하나가 필요했습니다. 이 버전은 둘 다 필요 없습니다. 원소마다 노드를 만들어 고리에 끼워 넣으면 됩니다. "
      "대신 노드마다 참조 하나와 나쁜 캐시 효율을 대가로 치릅니다. 추상적으로는 같은 큐인데, 절충의 방향이 정반대입니다.",
      "The array version needed modulo arithmetic and a wasted slot because the storage was fixed. This "
      "version needs neither — it allocates a node per item and links it into the ring. It pays instead with "
      "one reference per node and worse cache behaviour. Same abstract queue, opposite trade-offs.") + """</p>
  </div>
</section>

""" + practice_section("linked-list",
    "여기 있는 문제는 거의 전부 포인터를 다시 잇는 연습입니다. 코드를 쓰기 전에 바뀌기 전과 후의 그림을 먼저 그려 보세요.",
    "Nearly every one of these is really a pointer-rewiring exercise. Draw the before/after picture before "
    "you write code.") + pager(("queue.html", "큐", "Queue"), ("graph.html", "그래프", "Graph")) + """
</div>
</div>
</main>
""" + foot()
write("linked-list.html", LL)
