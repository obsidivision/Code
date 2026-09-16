# -*- coding: utf-8 -*-
import math
from _common import *

def tree_svg(width, height, nodes, edges, r=20, label="binary tree"):
    parts = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:%dpx">'
             % (width, height, label, width)]
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a][1:], nodes[b][1:]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy) or 1
        parts.append('<line class="dg-edge" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                     % (x1 + dx / d * r, y1 + dy / d * r, x2 - dx / d * r, y2 - dy / d * r))
    for name, x, y in nodes:
        parts.append('<circle class="dg-node" cx="%d" cy="%d" r="%d"/>' % (x, y, r))
        parts.append('<text class="dg-label" x="%d" y="%d">%s</text>' % (x, y + 1, name))
    parts.append('</svg>')
    return "".join(parts)


BST_SVG = tree_svg(330, 200,
    [("8", 165, 32), ("3", 82, 100), ("10", 248, 100), ("1", 36, 168), ("6", 128, 168), ("14", 294, 168)],
    [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)], label="binary search tree")

EXPR_SVG = tree_svg(420, 300,
    [("*", 160, 34), ("4", 70, 110), ("-", 250, 110), ("5", 190, 186), ("+", 330, 186),
     ("7", 285, 262), ("2", 380, 262)],
    [(0, 1), (0, 2), (2, 3), (2, 4), (4, 5), (4, 6)], label="expression tree")

TREENODE = '''
class TreeNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left          # a TreeNode, or None
        self.right = right        # a TreeNode, or None


#        8
#      /   \\
#     3     10
#    / \\      \\
#   1   6      14
root = TreeNode(8,
                TreeNode(3, TreeNode(1), TreeNode(6)),
                TreeNode(10, None, TreeNode(14)))


def height(node):
    """Number of levels. An empty tree has height 0 - straight from the definition."""
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def count(node):
    if node is None:
        return 0
    return 1 + count(node.left) + count(node.right)


print(count(root), height(root))      # 6 3
'''

TRAVERSALS = '''
def preorder(node, out=None):
    """VLR - visit the node, then the left subtree, then the right."""
    if out is None:
        out = []
    if node is not None:
        out.append(node.data)          # V
        preorder(node.left, out)       # L
        preorder(node.right, out)      # R
    return out


def inorder(node, out=None):
    """LVR - on a binary search tree this comes out sorted."""
    if out is None:
        out = []
    if node is not None:
        inorder(node.left, out)        # L
        out.append(node.data)          # V
        inorder(node.right, out)       # R
    return out


def postorder(node, out=None):
    """LRV - both children are finished before the node itself is visited."""
    if out is None:
        out = []
    if node is not None:
        postorder(node.left, out)      # L
        postorder(node.right, out)     # R
        out.append(node.data)          # V
    return out


print(preorder(root))    # [8, 3, 1, 6, 10, 14]
print(inorder(root))     # [1, 3, 6, 8, 10, 14]   <- sorted, because this is a BST
print(postorder(root))   # [1, 6, 3, 14, 10, 8]
'''

ARRAYREP = '''
# 1-indexed array representation; index 0 is left unused so the arithmetic stays clean.
tree = [None, 8, 3, 10, 1, 6, None, 14]
#              1  2   3  4  5     6   7

def parent(i):      return i // 2
def left_child(i):  return 2 * i
def right_child(i): return 2 * i + 1

print(tree[left_child(2)], tree[right_child(2)])   # 1 6   (children of the node holding 3)
print(tree[parent(5)])                             # 3     (parent of the node holding 6)
'''

EXPR = '''
import operator

OPERATORS = {"+": operator.add, "-": operator.sub,
             "*": operator.mul, "/": operator.truediv}


def build_from_postfix(tokens):
    """Build an expression tree from postfix tokens, using a stack of subtrees."""
    stack = []
    for token in tokens:
        if token in OPERATORS:
            right = stack.pop()            # popped in reverse: the second operand comes off first
            left = stack.pop()
            stack.append(TreeNode(token, left, right))
        else:
            stack.append(TreeNode(float(token)))
    return stack.pop()                     # exactly one subtree is left: the root


def evaluate(node):
    """Postorder evaluation: both operands must be known before the operator runs."""
    if node.left is None and node.right is None:
        return node.data                   # a leaf is an operand
    return OPERATORS[node.data](evaluate(node.left), evaluate(node.right))


tree = build_from_postfix(["4", "5", "7", "2", "+", "-", "*"])
print(inorder(tree))    # [4.0, '*', 5.0, '-', 7.0, '+', 2.0]  - infix, minus the brackets
print(evaluate(tree))   # -16.0    which is 4 * (5 - (7 + 2))
'''

BST = '''
def bst_search(node, key):
    """Iterative search - one comparison decides the whole direction."""
    while node is not None:
        if key == node.data:
            return node
        node = node.left if key < node.data else node.right
    return None                            # fell off the tree: not present


def bst_insert(node, key):
    """Insert exactly where a failed search would have stopped. Returns the subtree root."""
    if node is None:
        return TreeNode(key)               # this is where the search ran out
    if key < node.data:
        node.left = bst_insert(node.left, key)
    elif key > node.data:
        node.right = bst_insert(node.right, key)
    return node                            # key == node.data -> duplicate, ignored


def bst_min(node):
    while node.left is not None:           # smallest key = leftmost node
        node = node.left
    return node


def bst_delete(node, key):
    """Delete `key` and return the new subtree root."""
    if node is None:
        return None
    if key < node.data:
        node.left = bst_delete(node.left, key)
    elif key > node.data:
        node.right = bst_delete(node.right, key)
    else:
        # case (a) leaf, and case (b) one child, collapse into these two lines:
        if node.left is None:
            return node.right              # None for a leaf, else splice the right child up
        if node.right is None:
            return node.left
        # case (c) two children: copy the in-order successor's value, then delete it below
        successor = bst_min(node.right)
        node.data = successor.data
        node.right = bst_delete(node.right, successor.data)
    return node


tree = None
for key in [8, 3, 10, 1, 6, 14, 4, 7]:
    tree = bst_insert(tree, key)
print(inorder(tree))                       # [1, 3, 4, 6, 7, 8, 10, 14]
print(bst_search(tree, 6) is not None)     # True
tree = bst_delete(tree, 3)                 # two children -> replaced by successor 4
print(inorder(tree))                       # [1, 4, 6, 7, 8, 10, 14]
'''

TREE = head("트리 (Tree) — DSA 연습 허브",
            "이진 트리, 배열 표현과 연결 표현, 세 가지 순회, 수식 트리, 그리고 이진 탐색 트리의 탐색·삽입·삭제.",
            "tree") + page_head(
    "tree",
    "트리는 사이클이 없고 시작점이 정해져 있는 그래프입니다. 이 제약 하나로 계층 구조를 얻고, 여기에 순서 규칙을 하나 더 얹으면 O(log n) 탐색까지 얻습니다.",
    "A tree is a graph with no cycles and a designated starting point. That single restriction buys you a "
    "hierarchy — and, once you add an ordering rule, searching in O(log n)."
) + toc("tree", [("binary", "이진 트리", "Binary trees"),
                 ("shapes", "특별한 모양", "Special shapes"),
                 ("repr", "두 가지 표현법", "Two representations"),
                 ("traversal", "세 가지 순회", "The three traversals"),
                 ("expr", "수식 트리", "Expression trees"),
                 ("bst", "이진 탐색 트리", "Binary search trees"),
                 ("practice", "연습 문제", "Practice problems")]) + """

<section id="binary" style="--grad: var(--grad-tree)">
  """ + section_title("이진 트리", "Binary trees") + """
  <p>""" + L(
    "정의가 재귀적입니다. 이 페이지의 모든 알고리즘이 결국 이 정의를 코드로 옮긴 것이므로, 두 번 읽어 둘 값어치가 있습니다.",
    "The definition is recursive, and it is worth reading twice because every algorithm on this page is just "
    "the definition turned into code:") + """</p>
  <div class="note">
    <b>""" + L("이진 트리는 공집합이거나, 루트 노드 하나와 그 자체로 이진 트리인 두 개의 부분 트리(왼쪽·오른쪽)로 이루어진다.",
               "A binary tree is either empty, or it is a root node together with two binary trees — its left subtree and its right subtree.") + """</b>
    <p>""" + L(
      "\"공집합\"도 엄연한 이진 트리이지 나중에 땜질할 예외가 아닙니다. 아래 모든 함수가 <code>if node is None</code>으로 시작하는 이유입니다.",
      "\"Empty\" is a real binary tree, not a special case to patch later. That is why every function below "
      "starts with <code>if node is None</code>.") + """</p>
  </div>
  <p>""" + L("이 정의에서 따라 나오는 것들:", "Consequences of that definition:") + """</p>
  <ul>
    <li>""" + L("모든 노드의 자식은 <strong>최대 두 개</strong>입니다 — 차수 ≤ 2.", "Every node has <strong>at most two</strong> children — degree ≤ 2.") + """</li>
    <li>""" + L("<strong>왼쪽과 오른쪽은 구별됩니다.</strong> 왼쪽 자식 하나를 가진 루트와 오른쪽 자식 하나를 가진 루트는 둘 다 노드가 두 개지만 서로 다른 트리입니다.",
                "<strong>Left and right are distinguishable.</strong> A root with one left child is a different tree from a root with one right child, even though both have two nodes.") + """</li>
    <li>""" + L("루트를 뺀 모든 노드에 부모가 정확히 하나씩 있으므로, <strong>노드가 n개인 트리의 간선은 정확히 n − 1개</strong>입니다. 노드마다 위로 가는 간선이 하나씩인데 루트만 없는 셈입니다.",
                "Every node except the root has exactly one parent, so an <strong>n-node tree has exactly n − 1 edges</strong> — one edge per node, minus the root which has none above it.") + """</li>
    <li>""" + L("사이클이 없으므로 루트에서 어떤 노드로 가는 경로는 단 하나뿐입니다.", "There are no cycles, so there is exactly one path from the root to any node.") + """</li>
  </ul>
  <div class="card diagram" style="max-width:380px">""" + BST_SVG + """
  <p style="margin-top:.5rem">""" + L("노드 6개, 간선 5개, 높이 3", "6 nodes, 5 edges, height 3") + """</p></div>
</section>

<section id="shapes" style="--grad: var(--grad-tree)">
  """ + section_title("특별한 모양과 높이의 한계", "Special shapes and height limits") + """
  <div class="kv">
    <div><b>포화 이진 트리 · Full / perfect</b><span>""" + L(
      "모든 레벨이 빈틈없이 꽉 찬 트리입니다. 높이가 <em>h</em>인 포화 이진 트리의 노드 수는 정확히 2<sup>h</sup> − 1개이고, <em>k</em>번째 레벨에는 2<sup>k−1</sup>개가 있습니다.",
      "Every level is completely filled. A perfect tree of height <em>h</em> holds exactly 2<sup>h</sup> − 1 nodes, and level <em>k</em> holds 2<sup>k−1</sup> of them.") + """</span></div>
    <div><b>완전 이진 트리 · Complete</b><span>""" + L(
      "마지막 레벨을 뺀 모든 레벨이 꽉 차 있고, 마지막 레벨은 왼쪽부터 빈틈없이 채워진 트리입니다. 배열에 딱 맞게 저장되는 모양입니다.",
      "Every level is filled except possibly the last, and the last fills strictly left to right with no gaps. This is the shape that stores perfectly in an array.") + """</span></div>
    <div><b>편향 이진 트리 · Skewed</b><span>""" + L(
      "모든 노드가 자식을 하나씩만 가져서 사실상 연결 리스트가 된 트리입니다. 이진 탐색 트리의 성능을 망치는 최악의 경우입니다.",
      "Every node has only one child, so the tree degenerates into a linked list. This is the worst case that ruins a BST's performance.") + """</span></div>
  </div>
  <p>""" + L(
    "노드가 <em>n</em>개일 때 <strong>가능한 최소 높이</strong>는 ⌈log₂(n + 1)⌉로, 트리가 최대한 옆으로 퍼졌을 때입니다. <strong>최대 높이</strong>는 <em>n</em>으로, 한 줄로 편향되었을 때입니다. "
    "트리 기반 탐색이 주는 이점은 전부 이 최소 높이 근처에 머무는 데 달려 있습니다.",
    "For <em>n</em> nodes, the <strong>minimum</strong> possible height is ⌈log₂(n + 1)⌉ — achieved when the "
    "tree is as bushy as possible — and the <strong>maximum</strong> is <em>n</em>, when the tree is a single "
    "skewed chain. The whole promise of tree-based searching rests on staying near the minimum.") + """</p>
""" + code("tree_node.py", TREENODE) + """
</section>

<section id="repr" style="--grad: var(--grad-tree)">
  """ + section_title("두 가지 표현법", "Two representations") + """
  <h3>""" + L("배열 표현", "Array-based") + """</h3>
  <p>""" + L(
    "노드에 레벨 순서로, 각 레벨은 왼쪽에서 오른쪽으로, 1부터 번호를 매기고 그 번호를 인덱스로 씁니다. 그러면 구조가 전부 산술 계산이 됩니다. 포인터가 아예 없습니다.",
    "Number the nodes level by level, left to right, starting at 1, and store each node at that index. Then "
    "the structure is pure arithmetic — no pointers at all:") + """</p>
  <div class="kv">
    <div><b>""" + L("i의 부모", "Parent of i") + """</b><span><code>i // 2</code></span></div>
    <div><b>""" + L("i의 왼쪽 자식", "Left child of i") + """</b><span><code>2 * i</code></span></div>
    <div><b>""" + L("i의 오른쪽 자식", "Right child of i") + """</b><span><code>2 * i + 1</code></span></div>
  </div>
""" + code("array_tree.py", ARRAYREP) + """
  <p>""" + L(
    "<em>완전</em> 이진 트리에는 간결하고 빠릅니다. 힙을 저장하는 방식이 정확히 이것입니다. 반면 성기거나 편향된 트리에는 최악입니다. 노드 10개짜리 편향 트리에 배열 2¹⁰칸이 필요하고 대부분이 빈칸입니다.",
    "Compact and fast for a <em>complete</em> tree — this is exactly how heaps are stored. For a sparse or "
    "skewed tree it is terrible: a skewed tree of 10 nodes needs an array of 2¹⁰ slots, nearly all empty.") + """</p>
  <h3>""" + L("연결 표현", "Linked") + """</h3>
  <p>""" + L(
    "각 노드가 <code>data</code>, <code>left</code>, <code>right</code>를 갖는 객체입니다. 위의 <code>TreeNode</code> 클래스가 그것입니다. "
    "모양과 상관없이 실제 노드 수에 비례하는 메모리만 쓰고, 삽입할 때 크기를 다시 잡을 필요도 없습니다. 실제 코드는 거의 전부 이 방식을 쓰고, 아래 저지 문제들도 모두 이 형태로 트리를 건네줍니다.",
    "Each node is an object holding <code>data</code>, <code>left</code> and <code>right</code> — the "
    "<code>TreeNode</code> class above. Memory is proportional to the number of real nodes regardless of "
    "shape, and inserting does not require resizing anything. This is what almost all real code uses, and "
    "what every judge problem below hands you.") + """</p>
</section>

<section id="traversal" style="--grad: var(--grad-tree)">
  """ + section_title("세 가지 순회", "The three traversals") + """
  <p>""" + L(
    "리스트에는 당연한 순서가 하나 있지만 트리에는 없습니다. 그래서 골라야 합니다. 세 순회 모두 오른쪽보다 왼쪽 부분 트리를 먼저 방문하고, "
    "차이는 오직 <em>노드 자신을 언제 방문하는가</em>뿐입니다.",
    "A list has one obvious order. A tree does not, so you pick one. All three traversals visit the left "
    "subtree before the right; they differ only in <em>when the node itself is visited</em>.") + """</p>
  <div class="kv">
    <div><b>전위 순회 · Preorder (VLR)</b><span>""" + L(
      "노드 먼저, 그다음 왼쪽, 그다음 오른쪽. 트리를 복사하거나 구조를 위에서부터 출력할 때 씁니다.",
      "Node first, then left, then right. Use it to copy a tree or to print a structure top-down.") + """</span></div>
    <div><b>중위 순회 · Inorder (LVR)</b><span>""" + L(
      "왼쪽, 노드, 오른쪽. 이진 탐색 트리에서는 키가 정렬된 순서로 나옵니다.",
      "Left, node, right. On a BST this emits the keys in sorted order.") + """</span></div>
    <div><b>후위 순회 · Postorder (LRV)</b><span>""" + L(
      "자식 둘을 모두 끝낸 뒤 노드를 방문합니다. 노드의 결과가 자식에 의존할 때 — 계산이나 메모리 해제 같은 경우 — 쓰는 순서입니다.",
      "Both children first, node last. Use it whenever a node's result depends on its children — evaluating, or freeing memory.") + """</span></div>
  </div>
""" + code("traversals.py", TRAVERSALS) + """
  <p style="font-size:.9rem;color:var(--text-faint)">""" + L(
    "외우는 요령: V(방문)가 어디에 오는지가 이름입니다. 전위는 V가 맨 앞, 중위는 가운데, 후위는 맨 뒤. L은 언제나 R보다 앞입니다.",
    "Reading trick: the letter V tells you where the node goes. Pre = V first, In = V in the middle, "
    "Post = V last. L always comes before R.") + """</p>
</section>

<section id="expr" style="--grad: var(--grad-tree)">
  """ + section_title("수식 트리", "Expression trees") + """
  <p>""" + L(
    "수식 트리는 산술식을 트리로 저장한 것입니다. <strong>연산자는 내부 노드에, 피연산자는 잎에</strong> 놓입니다. 아래 트리는 <code>4 * (5 - (7 + 2))</code>입니다.",
    "An expression tree stores an arithmetic expression as a tree: <strong>operators at the internal "
    "nodes, operands at the leaves</strong>. The tree below is <code>4 * (5 - (7 + 2))</code>.") + """</p>
  <div class="card diagram" style="max-width:460px">""" + EXPR_SVG + """
  <p style="margin-top:.5rem">""" + L("후위 표기: <code>4 5 7 2 + - *</code> &nbsp;·&nbsp; 값: −16",
                                      "Postfix: <code>4 5 7 2 + - *</code> &nbsp;·&nbsp; value: −16") + """</p></div>
  <p>""" + L(
    "구조 자체가 우선순위와 묶음을 담고 있으므로 괄호가 필요 없습니다. 트리의 모양이 이미 <code>7 + 2</code>가 뺄셈보다 먼저라고 말하고 있습니다. "
    "이 트리에 세 가지 순회를 돌리면 고전적인 세 가지 표기법이 그대로 나옵니다. 중위는 중위 표기, 전위는 전위 표기, 후위는 후위 표기입니다.",
    "The structure encodes precedence and grouping, so no brackets are needed — the shape of the tree already "
    "says that <code>7 + 2</code> happens before the subtraction. Run the three traversals over it and you get "
    "the three classic notations: inorder gives infix, preorder gives prefix, postorder gives postfix.") + """</p>
  <p>""" + L(
    "<strong>계산이 왜 후위 순회인가:</strong> 연산자는 두 피연산자의 값이 모두 정해지기 전에는 실행될 수 없습니다. 후위 순회는 노드를 방문하기 전에 두 부분 트리를 먼저 끝내므로 정확히 그 조건을 만족합니다. "
    "전위 순회로 계산하려고 하면 양쪽 값이 아직 없는 상태에서 <code>*</code>에 도달하게 됩니다.",
    "<strong>Why evaluation is postorder:</strong> an operator cannot run until both of its operands have "
    "values. Postorder finishes both subtrees before visiting the node, which is exactly that requirement. Try "
    "to evaluate in preorder and you reach <code>*</code> while neither side is known yet.") + """</p>
  <p>""" + L(
    "후위 표기 입력으로 트리를 만들 때는 스택을 씁니다. 3단원에서 본 그 구조입니다. 토큰을 왼쪽부터 읽어서, 피연산자면 잎 노드로 만들어 push하고, "
    "연산자면 가장 최근의 부분 트리 두 개를 pop해 그 부모가 된 뒤 다시 push합니다. pop한 두 개의 순서를 뒤집어 붙여야 뺄셈과 나눗셈이 거꾸로 되지 않습니다.",
    "Building the tree from postfix input uses a stack — the same structure from Unit 03. Read tokens left to "
    "right: an operand becomes a leaf and is pushed; an operator pops the two most recent subtrees, becomes "
    "their parent, and is pushed back. Pop the two in reverse order, or subtraction and division come out "
    "backwards.") + """</p>
""" + code("expression_tree.py", EXPR) + """
</section>

<section id="bst" style="--grad: var(--grad-tree)">
  """ + section_title("이진 탐색 트리", "Binary search trees") + """
  <p>""" + L(
    "이진 탐색 트리는 이진 트리에 순서 규칙 하나를 더합니다. 그리고 이 규칙은 바로 아래 자식이 아니라 <strong>부분 트리 전체</strong>에 적용됩니다.",
    "A BST adds one ordering rule to the binary tree, and the rule applies to <strong>whole subtrees</strong>, "
    "not just to the immediate children:") + """</p>
  <div class="note">
    <b>""" + L("모든 노드에 대해: 왼쪽 부분 트리의 키는 전부 그 노드보다 작고, 오른쪽 부분 트리의 키는 전부 그 노드보다 크다.",
               "For every node: every key in its left subtree is smaller, and every key in its right subtree is larger.") + """</b>
    <p>""" + L(
      "사람들이 자주 틀리는 부분이 바로 이 재귀성입니다. 오른쪽 자식이 더 크다는 것만으로는 부족합니다. 오른쪽 부분 트리 세 단계 아래에 묻힌 값도 그 노드보다 커야 합니다.",
      "That recursion is the part people get wrong. A node's right child being larger is not enough — a value "
      "buried three levels down the right subtree must be larger than the node too.") + """</p>
  </div>
  <p>""" + L(
    "그 대가로 얻는 것: 모든 노드에서 비교 한 번이 부분 트리 하나를 통째로 지웁니다. 균형 잡힌 트리라면 탐색·삽입·삭제가 O(log n)입니다. "
    "편향된 트리에서는 O(n)으로 떨어집니다. 트리가 연결 리스트가 되어 버린 것이죠. (AVL 트리나 레드-블랙 트리 같은 자가 균형 트리는 바로 그것을 막기 위해 존재합니다.)",
    "The payoff: at every node one comparison eliminates an entire subtree. On a balanced tree that is "
    "O(log n) for search, insert and delete. On a skewed tree it degrades to O(n) — the tree has become a "
    "linked list. (Self-balancing variants such as AVL and red-black trees exist to prevent exactly that.)") + """</p>
  <p>""" + L("이것도 외워 두세요. <strong>이진 탐색 트리를 중위 순회하면 키가 정렬된 순서로 나옵니다.</strong>",
             "Also worth memorising: <strong>an inorder traversal of a BST prints the keys in sorted order.</strong>") + """</p>

  <h3>""" + L("탐색", "Search") + """</h3>
  <p>""" + L("현재 노드와 비교합니다. 같으면 찾은 것이고, 작으면 왼쪽으로, 크면 오른쪽으로 갑니다. <code>None</code>에 닿으면 트리에 없는 키입니다.",
             "Compare with the current node. Equal → found. Smaller → go left. Larger → go right. Hit <code>None</code> → the key is not in the tree.") + """</p>

  <h3>""" + L("삽입", "Insert") + """</h3>
  <p>""" + L(
    "그 키를 탐색해 봅니다. 탐색은 실패할 것이고, 실패해서 멈춘 그 <code>None</code> 자리가 바로 키가 있어야 할 자리입니다. 거기에 새 잎을 답니다. 삽입은 기존 노드의 구조를 절대 바꾸지 않습니다.",
    "Search for the key. The search will fail, and the <code>None</code> it fails at is precisely the spot the "
    "key belongs in — attach the new leaf there. Inserting never restructures an existing node.") + """</p>

  <h3>""" + L("삭제 — 세 가지 경우", "Delete — three cases") + """</h3>
  <ol>
    <li>""" + L("<strong>잎 노드.</strong> 구할 자식이 없습니다. 부모와의 링크를 끊으면 끝입니다.",
                "<strong>Leaf node.</strong> No children to rescue. Unlink it from its parent and you are done.") + """</li>
    <li>""" + L("<strong>자식이 하나.</strong> 그 자식을 삭제된 노드의 자리로 끌어올립니다. 부분 트리 전체가 위쪽과의 순서 관계를 그대로 유지합니다.",
                "<strong>One child.</strong> Splice that child up into the deleted node's place. The whole subtree keeps its ordering relative to everything above.") + """</li>
    <li>""" + L(
      "<strong>자식이 둘.</strong> 그냥 지울 수 없습니다. 부분 트리 두 개가 떨어져 나가기 때문입니다. 대신 그 노드의 <em>중위 후속자</em>를 찾습니다. "
      "오른쪽 부분 트리에서 가장 작은 키입니다. (같은 방식으로 왼쪽 부분 트리의 가장 큰 키를 써도 됩니다.) 그 값을 노드에 복사해 넣고, 오른쪽 부분 트리에서 그 후속자를 삭제합니다. "
      "후속자는 그 부분 트리의 가장 왼쪽 노드라 왼쪽 자식이 없으므로, 그 두 번째 삭제는 반드시 1번이나 2번 경우가 되고 재귀가 여기서 끝납니다.",
      "<strong>Two children.</strong> You cannot simply remove it — two subtrees would be orphaned. Instead find the node's <em>in-order successor</em>: the smallest key in its right subtree (equivalently, use the largest key in the left subtree). Copy that value into the node, then delete the successor from the right subtree. The successor is the leftmost node of that subtree, so it has no left child — meaning that second deletion is guaranteed to be case 1 or case 2, and the recursion terminates.") + """</li>
  </ol>
  <p>""" + L(
    "왜 하필 후속자일까요? 후속자는 정렬 순서에서 바로 다음 키이므로, 왼쪽 부분 트리의 모든 값보다 크고 오른쪽 부분 트리의 나머지 모든 값보다 작습니다. "
    "이진 탐색 트리 규칙을 깨지 않고 그 자리에 앉을 수 있는 값은 그것뿐입니다.",
    "Why the successor specifically? It is the next key in sorted order, so it is larger than everything in "
    "the left subtree and smaller than everything else in the right subtree. It is the only value that can sit "
    "in that position without breaking the BST rule.") + """</p>
""" + code("bst.py", BST) + """
</section>

""" + practice_section("tree",
    "순회 세 문제가 맨 앞에 있는 데는 이유가 있습니다. 그 셋이 손에 익으면 이진 탐색 트리 문제는 이미 가진 코드의 작은 변형이 됩니다. "
    "다 풀었다면 다음으로: <a href=\"https://leetcode.com/problems/validate-binary-search-tree/\" target=\"_blank\" rel=\"noopener\">LC 98 Validate Binary Search Tree</a>"
    "(이진 탐색 트리 규칙을 바로 아래 자식에 대한 것으로만 알고 있으면 틀리는 문제입니다)와 "
    "<a href=\"https://www.acmicpc.net/problem/1991\" target=\"_blank\" rel=\"noopener\">백준 1991 트리 순회</a>"
    "(한 프로그램에서 세 순회를 모두 출력합니다)를 권합니다.",
    "The three traversal problems come first for a reason — get those automatic, and the BST problems become "
    "small variations on code you already have. Going further once these are done: "
    "<a href=\"https://leetcode.com/problems/validate-binary-search-tree/\" target=\"_blank\" rel=\"noopener\">LC 98 "
    "Validate Binary Search Tree</a> (it catches you if you think the BST rule is only about direct children) and "
    "<a href=\"https://www.acmicpc.net/problem/1991\" target=\"_blank\" rel=\"noopener\">BOJ 1991 트리 순회</a>, "
    "which asks for all three traversals of one tree in a single program.") + pager(
        ("graph.html", "그래프", "Graph"), None) + """
</div>
</div>
</main>
""" + foot()
write("tree.html", TREE)
