# -*- coding: utf-8 -*-
import math
from _common import *

POS = {"A": (42, 34), "B": (166, 34), "C": (42, 116), "D": (166, 116)}
R = 19


def shrink(p, q, pad):
    (x1, y1), (x2, y2) = p, q
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy) or 1
    return (x1 + dx / d * pad, y1 + dy / d * pad, x2 - dx / d * pad, y2 - dy / d * pad)


def graph_svg(uid, edges, directed=False, weighted=False):
    parts = ['<svg viewBox="0 0 208 150" role="img" aria-label="example graph">']
    if directed:
        parts.append('<defs><marker id="ah-%s" viewBox="0 0 10 10" refX="9" refY="5" '
                     'markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" '
                     'orient="auto-start-reverse">'
                     '<path d="M0,0 L10,5 L0,10 z" fill="var(--text-faint)" stroke="none"/>'
                     '</marker></defs>' % uid)
    for a, b, w in edges:
        pad = R + (7 if directed else 2)
        x1, y1, x2, y2 = shrink(POS[a], POS[b], pad)
        marker = ' marker-end="url(#ah-%s)"' % uid if directed else ""
        parts.append('<line class="dg-edge" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"%s/>'
                     % (x1, y1, x2, y2, marker))
        if weighted:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            parts.append('<rect x="%.1f" y="%.1f" width="20" height="14" rx="4" fill="var(--bg-2)"/>'
                         % (mx - 10, my - 7))
            parts.append('<text class="dg-weight" x="%.1f" y="%.1f">%s</text>' % (mx, my + 4, w))
    for name, (x, y) in POS.items():
        parts.append('<circle class="dg-node" cx="%d" cy="%d" r="%d"/>' % (x, y, R))
        parts.append('<text class="dg-label" x="%d" y="%d">%s</text>' % (x, y + 1, name))
    parts.append('</svg>')
    return "".join(parts)


E = [("A", "B", 4), ("A", "C", 2), ("B", "D", 5), ("C", "D", 1)]

DIAGRAMS = """<div class="diagram-grid">
  <div class="card diagram"><h4>%s</h4><p>%s</p>%s</div>
  <div class="card diagram"><h4>%s</h4><p>%s</p>%s</div>
  <div class="card diagram"><h4>%s</h4><p>%s</p>%s</div>
  <div class="card diagram"><h4>%s</h4><p>%s</p>%s</div>
</div>""" % (
    L("무방향·비가중치", "Undirected, unweighted"), L("친구 관계망", "A friendship network"), graph_svg("u1", E),
    L("방향·비가중치", "Directed, unweighted"), L("누가 누구를 팔로우하는가", "\"Who follows whom\""), graph_svg("d1", E, directed=True),
    L("무방향·가중치", "Undirected, weighted"), L("거리가 붙은 도로망", "Roads with distances"), graph_svg("u2", E, weighted=True),
    L("방향·가중치", "Directed, weighted"), L("비용이 붙은 일방통행 경로", "One-way routes with costs"), graph_svg("d2", E, directed=True, weighted=True))

FLOORPLAN = """<svg viewBox="0 0 340 200" role="img" aria-label="floor plan with five rooms" style="max-width:340px">
  <g fill="var(--surface-2)" stroke="var(--border-strong)" stroke-width="2">
    <rect x="10" y="10" width="110" height="80" rx="6"/>
    <rect x="130" y="10" width="90" height="80" rx="6"/>
    <rect x="230" y="10" width="100" height="180" rx="6"/>
    <rect x="10" y="100" width="110" height="90" rx="6"/>
    <rect x="130" y="100" width="90" height="90" rx="6"/>
  </g>
  <g class="dg-label" style="font-size:12px">
    <text x="65" y="50">%s</text>
    <text x="175" y="50">%s</text>
    <text x="280" y="100">%s</text>
    <text x="65" y="145">%s</text>
    <text x="175" y="145">%s</text>
  </g>
  <g stroke="var(--c-graph)" stroke-width="5" stroke-linecap="round">
    <line x1="122" y1="50" x2="128" y2="50"/>
    <line x1="222" y1="50" x2="228" y2="50"/>
    <line x1="65" y1="92" x2="65" y2="98"/>
    <line x1="175" y1="92" x2="175" y2="98"/>
    <line x1="122" y1="145" x2="128" y2="145"/>
    <line x1="222" y1="145" x2="228" y2="145"/>
  </g>
</svg>""" % tuple(L(ko, en) for ko, en in
                  [("로비", "Lobby"), ("도서실", "Library"), ("실습실", "Lab"),
                   ("작업실", "Studio"), ("매점", "Cafe")])

GMATRIX = '''
class GraphMatrix:
    """Adjacency matrix: an n x n table where cell [i][j] describes edge i -> j."""

    def __init__(self, n):
        self.n = n
        self.matrix = [[0] * n for _ in range(n)]

    def add_edge(self, a, b, weight=1, directed=False):
        self.matrix[a][b] = weight
        if not directed:
            self.matrix[b][a] = weight      # symmetric table for an undirected graph

    def has_edge(self, a, b):
        return self.matrix[a][b] != 0       # O(1) - the whole point of a matrix

    def neighbours(self, v):
        return [j for j in range(self.n) if self.matrix[v][j]]   # O(n), even for 1 neighbour

    def degree(self, v):
        return sum(1 for x in self.matrix[v] if x)               # out-degree if directed

    def in_degree(self, v):
        return sum(1 for row in self.matrix if row[v])


g = GraphMatrix(4)                          # 0=A 1=B 2=C 3=D
for a, b in [(0, 1), (0, 2), (1, 3), (2, 3)]:
    g.add_edge(a, b)
for row in g.matrix:
    print(row)
# [0, 1, 1, 0]
# [1, 0, 0, 1]
# [1, 0, 0, 1]
# [0, 1, 1, 0]
'''

GLIST = '''
from collections import defaultdict, deque


class GraphList:
    """Adjacency list: each vertex maps to the vertices it connects to."""

    def __init__(self):
        self.adjacent = defaultdict(list)

    def add_edge(self, a, b, directed=False):
        self.adjacent[a].append(b)
        if not directed:
            self.adjacent[b].append(a)

    def neighbours(self, v):
        return self.adjacent[v]             # O(1) to reach, O(deg(v)) to read

    def degree(self, v):
        return len(self.adjacent[v])

    def reachable(self, start, goal):
        """Breadth-first search: is there a path from `start` to `goal`?"""
        seen = {start}
        queue = deque([start])              # the queue from Unit 02, doing real work
        while queue:
            v = queue.popleft()
            if v == goal:
                return True
            for nxt in self.adjacent[v]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        return False


g = GraphList()
for a, b in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]:
    g.add_edge(a, b)
print(dict(g.adjacent))       # {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'D'], 'D': ['B', 'C']}
print(g.degree("A"), g.reachable("A", "D"))    # 2 True
'''

GRAPH = head("그래프 (Graph) — DSA 연습 허브",
             "정점과 간선, 차수와 경로, 네 가지 그래프 종류, 그리고 인접 행렬과 인접 리스트의 파이썬 구현.",
             "graph") + page_head(
    "graph",
    "리스트는 자료를 한 줄로, 트리는 계층으로 묶습니다. 그래프는 두 제약을 모두 버립니다. 무엇이든 무엇과도 연결될 수 있습니다. "
    "그래서 도로망, 친구 관계, 선수 과목, 웹 링크를 모두 그래프로 표현합니다.",
    "Lists and trees force data into a line or a hierarchy. A graph drops both constraints: anything may "
    "connect to anything. That is why graphs model roads, friendships, prerequisites and web links."
) + toc("graph", [("origin", "어디서 시작했나", "Where it started"),
                  ("basics", "G = (V, E)", "G = (V, E)"),
                  ("types", "네 가지 그래프", "Four kinds of graph"),
                  ("terms", "용어 정리", "Vocabulary"),
                  ("repr", "두 가지 표현법", "Two representations"),
                  ("exercise", "직접 해 보기", "Try it yourself"),
                  ("practice", "연습 문제", "Practice problems")]) + """

<section id="origin" style="--grad: var(--grad-graph)">
  """ + section_title("어디서 시작했나", "Where it started") + """
  <p>""" + L(
    "18세기 쾨니히스베르크는 강의 양쪽 기슭과 두 개의 섬 위에 세워진 도시였고, 그 네 땅덩이를 일곱 개의 다리가 잇고 있었습니다. "
    "동네에는 이런 문제가 돌았습니다. 모든 다리를 정확히 한 번씩만 건너는 산책이 가능할까?",
    "Eighteenth-century Königsberg was built across both banks of a river and two islands, joined by seven "
    "bridges. A local puzzle asked: can you take a walk that crosses every bridge exactly once?") + """</p>
  <p>""" + L(
    "사람들이 몇 년 동안 온갖 경로를 시도했지만 매번 실패했습니다. 그러나 계속 실패하는 것은 증명이 아닙니다. "
    "1736년 레온하르트 오일러는 지도를 아예 버리는 방법으로 이 문제를 끝냈습니다. 거리도, 다리의 길이도, 골목의 배치도 중요하지 않았습니다. "
    "중요한 것은 단 두 가지, 땅덩이가 몇 개인지와 어떤 쌍이 이어져 있는지뿐이었습니다. 그는 도시를 점 네 개와 연결선 일곱 개로 다시 그렸습니다.",
    "People tried routes for years and always failed, but failing repeatedly is not a proof. In 1736 Leonhard "
    "Euler settled it by throwing the map away. Distances, bridge lengths, street layouts — none of it "
    "mattered. Only two things did: how many land masses there were, and which pairs of them were joined. "
    "He redrew the city as four dots and seven connections.") + """</p>
  <p>""" + L(
    "그렇게 단순해진 그림에서는 답이 저절로 떨어집니다. 산책이 어떤 땅덩이로 들어갔다면 반드시 나와야 하므로, 각 땅덩이에는 짝수 개의 다리가 붙어 있어야 합니다. "
    "출발점과 도착점만 예외입니다. 그런데 쾨니히스베르크에서는 <em>네 땅덩이 모두</em> 홀수 개의 다리를 갖고 있었습니다. 그런 산책은 존재할 수 없고, 아무리 시도해도 찾을 수 없었을 것입니다.",
    "In that stripped-down picture the answer falls out. Every time your walk enters a land mass it must also "
    "leave, so each land mass needs an even number of bridges — except possibly where you start and where you "
    "finish. In Königsberg <em>all four</em> land masses had an odd number of bridges. Such a walk cannot "
    "exist, and no amount of trying would ever have found one.") + """</p>
  <div class="note">
    <b>""" + L("기억해 둘 아이디어", "The idea worth keeping.") + """</b>
    <p>""" + L(
      "오일러가 한 일이 곧 그래프 이론의 시작이었습니다. 기하를 버리고 연결만 남기는 것. 문제가 \"무엇이 무엇과 이어져 있는가\"로 줄어들고 나면, "
      "점이 다리든 지하철역이든 선수 과목이든 사람이든 같은 몇 가지 알고리즘으로 풀립니다.",
      "Euler's move was the invention of graph theory: discard the geometry, keep the connections. Once a "
      "problem is reduced to \"what is connected to what\", the same handful of algorithms solves it — whether "
      "the dots are bridges, subway stations, course prerequisites or people.") + """</p>
  </div>
</section>

<section id="basics" style="--grad: var(--grad-graph)">
  """ + section_title("G = (V, E)", "G = (V, E)") + """
  <p>""" + L(
    "그래프는 <code>G = (V, E)</code>로 씁니다. <strong>정점</strong>(점, 노드라고도 합니다)의 집합과 <strong>간선</strong>(연결)의 집합입니다. "
    "그 외에는 아무 조건도 없습니다. 루트도, 순서도, 한 정점에 붙을 수 있는 간선 수의 제한도 없습니다.",
    "A graph is written <code>G = (V, E)</code>: a set of <strong>vertices</strong> (the dots, also called "
    "nodes) and a set of <strong>edges</strong> (the connections). Nothing else is required — no root, no "
    "order, no limit on how many edges a vertex may have.") + """</p>
  <p>""" + L("아래에 그린 정점 네 개짜리 그래프를 집합 기호로 쓰면 이렇습니다.",
             "For the four-vertex graph drawn below, the set notation is:") + """</p>
  <div class="kv">
    <div><b>""" + L("무방향", "Undirected") + """</b><span><code>V(G) = {A, B, C, D}</code><br><code>E(G) = {(A,B), (A,C), (B,D), (C,D)}</code></span></div>
    <div><b>""" + L("방향", "Directed") + """</b><span><code>V(G) = {A, B, C, D}</code><br><code>E(G) = {&lt;A,B&gt;, &lt;A,C&gt;, &lt;B,D&gt;, &lt;C,D&gt;}</code></span></div>
  </div>
  <p>""" + L(
    "괄호 모양이 뜻을 담고 있습니다. 소괄호 <code>(A,B)</code>는 <em>순서 없는</em> 쌍입니다. 간선이 양방향이므로 <code>(A,B)</code>와 <code>(B,A)</code>는 같은 간선입니다. "
    "꺾쇠 <code>&lt;A,B&gt;</code>는 <em>순서 있는</em> 쌍입니다. A에서 B로만 가는 간선이고, <code>&lt;B,A&gt;</code>는 있을 수도 없을 수도 있는 다른 간선입니다.",
    "The brackets carry the meaning. Round brackets <code>(A,B)</code> are an <em>unordered</em> pair — the "
    "edge runs both ways, so <code>(A,B)</code> and <code>(B,A)</code> are the same edge. Angle brackets "
    "<code>&lt;A,B&gt;</code> are an <em>ordered</em> pair — the edge goes from A to B only, and "
    "<code>&lt;B,A&gt;</code> would be a different edge that may or may not exist.") + """</p>
</section>

<section id="types" style="--grad: var(--grad-graph)">
  """ + section_title("네 가지 그래프", "Four kinds of graph") + """
  <p>""" + L(
    "서로 독립적인 예/아니오 질문 두 개 — 간선이 한 방향인가, 간선에 수가 붙는가 — 로 네 가지 조합이 나옵니다. 네 그림 모두 같은 정점을 씁니다.",
    "Two independent yes/no choices — are edges one-way, and do edges carry a number? — give four "
    "combinations. Same four vertices in each picture:") + """</p>
""" + DIAGRAMS + """
  <ul>
    <li>""" + L("<strong>무방향 그래프:</strong> 관계가 서로에게 성립합니다. 친구 관계, 맞닿은 국경, 양방향 도로.",
                "<strong>Undirected:</strong> the relation is mutual. Friendship, shared borders, a two-way street.") + """</li>
    <li>""" + L("<strong>방향 그래프:</strong> 관계에 출발점과 도착점이 있습니다. 팔로우, 선수 과목, 일방통행 도로.",
                "<strong>Directed:</strong> the relation has a source and a target. Following an account, a prerequisite course, a one-way street.") + """</li>
    <li>""" + L("<strong>비가중치:</strong> 간선이 있거나 없거나 둘 중 하나입니다.",
                "<strong>Unweighted:</strong> an edge either exists or it does not.") + """</li>
    <li>""" + L("<strong>가중치 그래프:</strong> 간선마다 수가 붙습니다. 거리, 비용, 시간, 용량 같은 것입니다. 최단 경로 알고리즘에는 이것이 필요합니다.",
                "<strong>Weighted:</strong> each edge carries a number — distance, cost, time, capacity. Shortest-path algorithms need this.") + """</li>
  </ul>
</section>

<section id="terms" style="--grad: var(--grad-graph)">
  """ + section_title("용어 정리", "Vocabulary") + """
  <div class="kv">
    <div><b>인접 · Adjacent</b><span>""" + L(
      "간선으로 이어진 두 정점은 서로 인접하다고 하고, 각자 상대의 <em>이웃</em>입니다. 위 그림에서 A와 B는 인접하지만 A와 D는 그렇지 않습니다.",
      "Two vertices joined by an edge are adjacent, and each is a <em>neighbour</em> of the other. In the diagrams above, A and B are adjacent; A and D are not.") + """</span></div>
    <div><b>부속 · Incident</b><span>""" + L(
      "간선은 자신이 잇는 두 정점에 부속됩니다. 정점끼리는 서로 인접하고, 간선은 정점에 부속된다고 구분해서 씁니다.",
      "An edge is incident to the two vertices it joins. Vertices are adjacent to each other; edges are incident to vertices.") + """</span></div>
    <div><b>차수 · Degree</b><span>""" + L(
      "한 정점에 붙어 있는 간선의 개수입니다. 예시 그래프에서는 모든 정점의 차수가 2입니다.",
      "How many edges touch a vertex. Every vertex in the example graph has degree 2.") + """</span></div>
    <div><b>진입 차수 / 진출 차수</b><span>""" + L(
      "방향 그래프에서는 개수가 둘로 나뉩니다. 들어오는 간선과 나가는 간선입니다. 방향 그래프 예시에서 A는 진입 차수 0, 진출 차수 2이고, D는 진입 차수 2, 진출 차수 0입니다.",
      "For directed graphs the count splits: edges arriving versus edges leaving. In the directed example, A has in-degree 0 and out-degree 2; D has in-degree 2 and out-degree 0.") + """</span></div>
    <div><b>경로 · Path</b><span>""" + L(
      "이웃한 쌍이 모두 간선으로 이어져 있는 정점의 나열입니다. A → B → D 같은 것이죠. 길이는 정점 수가 아니라 간선 수로 셉니다.",
      "A sequence of vertices where each consecutive pair is joined by an edge, such as A → B → D. Its length is the number of edges, not vertices.") + """</span></div>
    <div><b>사이클 · Cycle</b><span>""" + L(
      "간선을 다시 쓰지 않고 출발한 정점으로 돌아오는 경로입니다. A → B → D → C → A가 사이클입니다.",
      "A path that returns to where it started without reusing an edge. A → B → D → C → A is a cycle.") + """</span></div>
    <div><b>연결 · Connected</b><span>""" + L(
      "모든 정점 쌍 사이에 경로가 있으면 연결 그래프입니다. 그렇지 않으면 여러 개의 <em>연결 요소</em>로 나뉩니다.",
      "A graph is connected if a path exists between every pair of vertices. Otherwise it splits into separate <em>components</em>.") + """</span></div>
    <div><b>""" + L("악수 정리", "Handshake rule") + """</b><span>""" + L(
      "간선 하나가 양 끝 정점의 차수를 각각 1씩 올리므로, 모든 정점의 차수를 더하면 간선 수의 정확히 두 배가 됩니다.",
      "Each edge adds 1 to the degree of both endpoints, so the degrees of all vertices sum to exactly twice the number of edges.") + """</span></div>
  </div>
</section>

<section id="repr" style="--grad: var(--grad-graph)">
  """ + section_title("두 가지 표현법", "Two representations") + """
  <p>""" + L(
    "그래프를 그림으로 그리는 것은 사람을 위한 일입니다. 프로그램에는 간선 집합을 담을 자료구조가 필요하고, 표준적인 선택지는 두 가지입니다.",
    "Drawing a graph is for humans. A program needs the edge set in a data structure, and there are two "
    "standard choices.") + """</p>

  <h3>""" + L("인접 행렬 · Adjacency matrix", "Adjacency matrix · 인접 행렬") + """</h3>
  <p>""" + L(
    "<code>n × n</code> 크기의 표입니다. <code>[i][j]</code> 칸은 <code>i</code>에서 <code>j</code>로 가는 간선이 있으면 1, 없으면 0입니다. "
    "가중치 그래프라면 그 자리에 가중치를 넣습니다. 무방향 그래프의 표는 대칭입니다. 항상 <code>matrix[i][j] == matrix[j][i]</code>입니다.",
    "An <code>n × n</code> table. Cell <code>[i][j]</code> is 1 when an edge runs from <code>i</code> to "
    "<code>j</code>, or 0 when it does not — or the edge's weight, for a weighted graph. An undirected graph "
    "gives a symmetric table: <code>matrix[i][j] == matrix[j][i]</code> always.") + """</p>
""" + code("graph_matrix.py", GMATRIX) + """
  <h3>""" + L("인접 리스트 · Adjacency list", "Adjacency list · 인접 리스트") + """</h3>
  <p>""" + L(
    "각 정점에 대해 실제로 이어진 정점들만 저장합니다. 파이썬에서는 리스트를 값으로 갖는 딕셔너리면 충분합니다. 존재하지 않는 간선에는 아무것도 저장하지 않습니다.",
    "Store, for each vertex, only the vertices it actually connects to. A dictionary of lists does the job in "
    "Python. Nothing is stored for edges that do not exist.") + """</p>
""" + code("graph_list.py", GLIST) + """
  <h3>""" + L("어느 쪽을 쓸까?", "Which one?") + """</h3>
  <div class="table-scroll">
  <table class="data">
    <thead><tr><th>&nbsp;</th><th>""" + L("인접 행렬", "Adjacency matrix") + """</th><th>""" + L("인접 리스트", "Adjacency list") + """</th></tr></thead>
    <tbody>
      <tr><td><strong>""" + L("메모리", "Memory") + """</strong></td><td>""" + L("간선 수와 무관하게 O(V²)", "O(V²) regardless of edge count") + """</td><td>O(V + E)</td></tr>
      <tr><td><strong>""" + L("\"i–j 간선이 있나?\"", "\"Is there an edge i–j?\"") + """</strong></td><td>O(1)</td><td>""" + L("O(i의 차수)", "O(degree of i)") + """</td></tr>
      <tr><td><strong>""" + L("i의 이웃 전부 나열", "List all neighbours of i") + """</strong></td><td>""" + L("O(V) — 한 행 전체를 훑습니다", "O(V) — scan the whole row") + """</td><td>""" + L("O(i의 차수)", "O(degree of i)") + """</td></tr>
      <tr><td><strong>""" + L("간선 추가", "Add an edge") + """</strong></td><td>O(1)</td><td>O(1)</td></tr>
      <tr><td><strong>""" + L("유리한 경우", "Best for") + """</strong></td><td>""" + L("밀집 그래프, 상수 시간 간선 확인이 필요할 때", "Dense graphs, constant-time edge tests") + """</td><td>""" + L("희소 그래프 — 실제 자료는 대부분 이쪽입니다", "Sparse graphs — which is most real data") + """</td></tr>
    </tbody>
  </table>
  </div>
  <p>""" + L(
    "사용자가 100만 명이고 각자 친구가 100명인 소셜 네트워크는 희소 그래프입니다. 리스트로는 약 10⁸개의 항목이면 되지만, 행렬로는 10¹²개의 칸이 필요하고 그 대부분이 0입니다. "
    "저지에서 만나는 그래프 문제를 거의 전부 인접 리스트를 만드는 것으로 시작하는 이유입니다.",
    "A social network with a million users and a hundred friends each is sparse: the list needs ~10⁸ entries, "
    "the matrix needs 10¹² cells, almost all zero. That is why nearly every graph problem you will solve on a "
    "judge starts by building an adjacency list.") + """</p>
</section>

<section id="exercise" style="--grad: var(--grad-graph)">
  """ + section_title("직접 해 보기", "Try it yourself") + """
  <p>""" + L(
    "작은 건물의 평면도입니다. 방은 공간이고, 색칠된 표시는 두 방을 잇는 출입구입니다. 이것을 그래프로 모델링하고 두 가지 표현을 모두 써 보세요.",
    "Here is a floor plan of a small building. Rooms are spaces; the coloured marks are doorways connecting "
    "two rooms. Model it as a graph and write out both representations.") + """</p>
  <div class="card diagram" style="max-width:420px">""" + FLOORPLAN + """</div>
  <ol>
    <li>""" + L("정점은 무엇인가요? (힌트: 출입구가 아니라 방입니다.)", "What are the vertices? (Hint: it is the rooms, not the doors.)") + """</li>
    <li>""" + L("간선은 무엇인가요? 이 그래프는 방향 그래프여야 할까요, 무방향이어야 할까요 — 출입구는 양쪽으로 지날 수 있나요?",
                "What are the edges? Should this graph be directed or undirected — can you walk through a doorway in both directions?") + """</li>
    <li>""" + L("<code>V(G)</code>와 <code>E(G)</code>를 집합 기호로 써 보세요.", "Write <code>V(G)</code> and <code>E(G)</code> in set notation.") + """</li>
    <li>""" + L("5 × 5 인접 행렬을 만들어 보세요. 방 순서는 로비, 도서실, 실습실, 작업실, 매점으로 하세요.",
                "Build the 5 × 5 adjacency matrix. Order the rooms Lobby, Library, Lab, Studio, Cafe.") + """</li>
    <li>""" + L("인접 리스트도 만들어 보세요.", "Build the adjacency list.") + """</li>
    <li>""" + L("각 방의 차수는 얼마인가요? 가장 많이 연결된 방은 어디인가요?", "What is the degree of each room? Which room is the most connected?") + """</li>
    <li>""" + L("악수 정리를 확인해 보세요. 차수의 합이 출입구 수의 두 배가 되나요?", "Check the handshake rule: do the degrees sum to twice the number of doorways?") + """</li>
    <li>""" + L("이제 출입구 하나를 한 방향으로만 통하는 비상구로 바꿔 보세요. 어느 표현이 달라지고, 행렬은 어떻게 대칭을 잃나요?",
                "Now change one doorway into a one-way fire exit. Which representation changes, and how does the matrix stop being symmetric?") + """</li>
  </ol>
  <div class="note">
    <b>""" + L("정답 확인", "Check your answer.") + """</b>
    <p>""" + L(
      "출입구 6개, 방 5개, 무방향입니다. 차수는 로비 2, 도서실 3, 실습실 2, 작업실 2, 매점 3이고 합은 12로, 간선 6개의 두 배입니다. ✔",
      "Six doorways, five rooms, undirected. Degrees: Lobby 2, Library 3, Lab 2, Studio 2, Cafe 3 — summing "
      "to 12, which is 2 × 6 edges. ✔") + """</p>
  </div>
</section>

""" + practice_section("graph",
    "쉬움 두 문제부터 시작하세요. 둘 다 인접 구조를 만들어 읽기만 하면 되는 순수한 연습입니다. 보통 난이도부터는 그 위에 순회가 얹힙니다.",
    "Start with the two Easy problems — both are pure 'build the adjacency structure and read it' drills. "
    "The Medium ones add a traversal on top.") + pager(("linked-list.html", "연결 리스트", "Linked List"), ("tree.html", "트리", "Tree")) + """
</div>
</div>
</main>
""" + foot()
write("graph.html", GRAPH)
