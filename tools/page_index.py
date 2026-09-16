# -*- coding: utf-8 -*-
from _common import *

INDEX = head("DSA 연습 허브 — 자료구조와 알고리즘",
             "정보/정보과학 수업 진도에 맞춘 개념 정리와 LeetCode·백준 연습 문제. 큐, 연결 리스트, 그래프, 트리.") + """
<main class="wrap">

<section class="hero">
  <span class="hero-eyebrow">🇰🇷 정보과학 → 🌐 LeetCode</span>
  <h1>""" + L("수업에서 배우고,<br><span class=\"grad-text\">영어로 연습하기.</span>",
              "Learn it in class.<br><span class=\"grad-text\">Drill it in English.</span>") + """</h1>
  <p class="lead">""" + L(
    "정보과학 수업이 진도를 나가는 순서 그대로 정리했습니다. 단원마다 개념을 짧게 되짚고, "
    "그대로 읽을 수 있는 파이썬 참고 구현을 싣고, 그 개념을 정확히 연습할 수 있는 난이도별 문제를 모았습니다.",
    "The units your Informatics course teaches, in the order it teaches them. Each one gives you a short "
    "concept refresher in plain language, a clean Python reference implementation you can actually read, and "
    "a leveled set of judge problems that practise exactly that idea.") + """</p>
  <div class="hero-actions">
    <a class="btn btn-primary" href="queue.html">""" + L("큐부터 시작하기 →", "Start with Queue →") + """</a>
    <button class="btn" type="button" id="random-problem">🎲 안 푼 문제 랜덤</button>
  </div>
</section>

<section id="topics">
  """ + section_title("이번 학기 진도", "This semester") + """
  <p>""" + L("위에서부터 차례대로 하세요. 각 단원은 앞 단원 위에 쌓입니다.",
             "Work top to bottom — each unit leans on the one before it.") + """</p>
  <div class="topic-grid" id="topic-grid"></div>
</section>

<section class="card summary" id="progress">
  <div class="summary-top">
    <h2>""" + L("학습 진행 상황", "Your progress") + """</h2>
    <span class="big grad-text" data-overall="pct">0%</span>
    <span style="color:var(--text-dim);font-size:.9rem">""" + L(
      '전체 <b data-overall="total">0</b>문제 중 <b data-overall="done">0</b>문제 완료',
      '<b data-overall="done">0</b> of <b data-overall="total">0</b> problems solved') + """</span>
  </div>
  <div class="pbar"><span data-overall="bar"></span></div>
  <div class="stat-row">
    <div class="stat"><b data-overall="done">0</b><span>""" + L("푼 문제", "Problems solved") + """</span></div>
    <div class="stat"><b data-overall="remaining">0</b><span>""" + L("남은 문제", "Still to go") + """</span></div>
    <div class="stat"><b data-overall="topics">0</b><span>""" + L("100% 달성 단원", "Units at 100%") + """</span></div>
    <div class="stat"><b data-overall="units">0</b><span>""" + L("이번 학기 단원", "Units this semester") + """</span></div>
  </div>
  <div>
    <button class="chip" type="button" id="reset-progress">진행 상황 초기화</button>
  </div>
</section>

<section id="how">
  """ + section_title("사용법", "How to use this site") + """
  <div class="kv">
    <div><b>""" + L("1 · 개념 되짚기", "1 · Refresh") + """</b><span>""" + L(
      "수업에서 방금 배운 단원의 개념 정리를 읽습니다. 일부러 짧게 썼습니다.",
      "Read the concept section for the unit you just covered in class. It is short on purpose.") + """</span></div>
    <div><b>""" + L("2 · 코드 읽기", "2 · Read the code") + """</b><span>""" + L(
      "모든 자료구조에 파이썬 참고 구현이 있고, 헷갈리기 쉬운 부분에는 주석을 달아 두었습니다.",
      "Every structure has a reference Python implementation with comments on the parts that trip people up.") + """</span></div>
    <div><b>""" + L("3 · 문제 풀기", "3 · Drill") + """</b><span>""" + L(
      "문제 목록을 위에서부터 차례로 풉니다. 이미 쉬움 → 보통 → 어려움 순으로 정렬해 두었습니다.",
      "Work the problem list top to bottom — it is already ordered Easy → Medium → Hard.") + """</span></div>
    <div><b>""" + L("4 · 기록하기", "4 · Track") + """</b><span>""" + L(
      "푼 문제는 체크해 두세요. 체크는 이 브라우저의 localStorage에만 저장되므로 새로고침해도 남지만 다른 기기와 동기화되지는 않습니다.",
      "Tick each problem off. Checkboxes live in this browser's localStorage, so they survive a refresh but "
      "are not synced anywhere.") + """</span></div>
  </div>
  <div class="note">
    <b>""" + L("한국어와 영어를 같이 쓰는 이유", "Why both Korean and English?") + """</b>
    <p>""" + L(
      "수업에서는 이 자료구조들을 한국어로 부르지만, 연습 문제를 내는 저지는 거의 전부 영어를 씁니다. "
      "그래서 단원마다 두 이름을 함께 보여 줍니다. '연결 리스트'와 'linked list'가 머릿속에서 따로 놀지 않도록요. "
      "오른쪽 위 <b>EN / 한국어</b> 버튼으로 설명 언어를 바꿀 수 있습니다. 문제 제목은 저지에서 검색할 수 있도록 "
      "항상 영어 원문 그대로 둡니다. 한국어식 문제 설명이 더 잘 맞는 개념에는 백준 문제를 섞어 두었습니다.",
      "Your course names these structures in Korean, but almost every practice judge names them in English. "
      "Each unit shows both labels so that \"연결 리스트\" and \"linked list\" stop being two separate things in "
      "your head. Use the <b>EN / 한국어</b> button at the top right to switch the language of the explanations. "
      "Problem titles always stay in English so you can find them on the judge. Baekjoon problems are mixed in "
      "where a Korean-style problem statement fits the concept better.") + """</p>
  </div>
</section>

</main>
""" + foot()
write("index.html", INDEX)
