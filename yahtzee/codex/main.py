#!/usr/bin/env python3
"""Yahtzee probability helper app.

Run:
    python yahtzee/codex/main.py
Then open http://127.0.0.1:8000 in a browser.
"""

from __future__ import annotations

import json
import random
from collections import Counter
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable

CategoryFn = Callable[[list[int]], bool]


def has_n_of_a_kind(dice: list[int], n: int) -> bool:
    return max(Counter(dice).values()) >= n


def is_full_house(dice: list[int]) -> bool:
    counts = sorted(Counter(dice).values())
    return counts == [2, 3]


def is_small_straight(dice: list[int]) -> bool:
    unique = set(dice)
    straights = ({1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6})
    return any(s.issubset(unique) for s in straights)


def is_large_straight(dice: list[int]) -> bool:
    return sorted(set(dice)) in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6])


def is_yahtzee(dice: list[int]) -> bool:
    return len(set(dice)) == 1


CATEGORIES: dict[str, CategoryFn] = {
    "Ones": lambda d: 1 in d,
    "Twos": lambda d: 2 in d,
    "Threes": lambda d: 3 in d,
    "Fours": lambda d: 4 in d,
    "Fives": lambda d: 5 in d,
    "Sixes": lambda d: 6 in d,
    "Three of a Kind": lambda d: has_n_of_a_kind(d, 3),
    "Four of a Kind": lambda d: has_n_of_a_kind(d, 4),
    "Full House": is_full_house,
    "Small Straight": is_small_straight,
    "Large Straight": is_large_straight,
    "Yahtzee": is_yahtzee,
}


def straight_keep_mask(dice: list[int], large: bool) -> list[bool]:
    target_sets = (
        [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
        if large
        else [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
    )
    unique = set(dice)
    best = max(target_sets, key=lambda s: len(s & unique))
    keep_vals = set(best) & unique
    used: Counter[int] = Counter()
    mask = []
    for val in dice:
        if val in keep_vals and used[val] == 0:
            mask.append(True)
            used[val] += 1
        else:
            mask.append(False)
    return mask


def target_keep_mask(dice: list[int], category: str) -> list[bool]:
    counts = Counter(dice)
    if category in {"Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"}:
        face = [1, 2, 3, 4, 5, 6][
            ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"].index(category)
        ]
        return [v == face for v in dice]

    if category in {"Three of a Kind", "Four of a Kind", "Yahtzee"}:
        best_val = max(counts, key=lambda k: (counts[k], k))
        return [v == best_val for v in dice]

    if category == "Full House":
        ordered = sorted(counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        keep_vals = {ordered[0][0]}
        if len(ordered) > 1:
            keep_vals.add(ordered[1][0])
        return [v in keep_vals for v in dice]

    if category == "Small Straight":
        return straight_keep_mask(dice, large=False)

    if category == "Large Straight":
        return straight_keep_mask(dice, large=True)

    return [False] * 5


def simulate_category(
    start_dice: list[int],
    initial_keep: list[bool],
    rolls_remaining: int,
    category: str,
    trials: int,
    rng: random.Random,
) -> float:
    check = CATEGORIES[category]
    hits = 0

    for _ in range(trials):
        dice = list(start_dice)
        keep = list(initial_keep)

        for roll_idx in range(rolls_remaining):
            for i in range(5):
                if not keep[i]:
                    dice[i] = rng.randint(1, 6)

            if roll_idx < rolls_remaining - 1:
                keep = target_keep_mask(dice, category)

        if check(dice):
            hits += 1

    return hits / trials if trials else 0.0


def estimate_probabilities(
    dice: list[int], keep: list[bool], rolls_remaining: int, trials: int = 8000
) -> dict[str, float]:
    rng = random.Random()
    return {
        name: simulate_category(dice, keep, rolls_remaining, name, trials, rng)
        for name in CATEGORIES
    }


INDEX_HTML = """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Yahtzee Probability Predictor</title>
  <script src=\"https://unpkg.com/vue@3/dist/vue.global.prod.js\"></script>
  <script src=\"https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js\"></script>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin:0; background:#141a24; color:#eef2ff; }
    .container { max-width: 980px; margin: 0 auto; padding: 24px; }
    .dice-grid { display:grid; grid-template-columns: repeat(5, minmax(90px, 1fr)); gap: 12px; }
    .die { border:2px solid #334155; border-radius: 12px; padding: 12px; text-align:center; background:#1e293b; cursor:pointer; user-select:none; }
    .die.kept { border-color:#22c55e; box-shadow: 0 0 0 2px rgba(34,197,94,.3); }
    .value { font-size: 2rem; font-weight: 700; margin: 8px 0; }
    .controls { margin-top: 8px; display:flex; justify-content:center; gap:8px; }
    button { border:0; border-radius:10px; padding: 10px 14px; font-weight:600; cursor:pointer; }
    .primary { background:#3b82f6; color:white; }
    .secondary { background:#334155; color:#e2e8f0; }
    table { width:100%; border-collapse: collapse; margin-top: 20px; }
    th, td { padding: 8px; border-bottom:1px solid #334155; text-align:left; }
    .bar { height:10px; border-radius:999px; background:#1f2937; overflow:hidden; }
    .bar > span { display:block; height:100%; background: linear-gradient(90deg, #22c55e, #3b82f6); }
    .row { display:flex; gap: 16px; align-items:center; margin:14px 0; flex-wrap:wrap; }
    select, input { background:#0f172a; color:#e2e8f0; border:1px solid #334155; border-radius:8px; padding:8px; }
  </style>
</head>
<body>
<div id=\"app\" class=\"container\">
  <h1>Yahtzee Probability Predictor</h1>
  <p>Set your dice, click a die to keep/unkeep it, then press <strong>Enter</strong> (or button) to update probabilities.</p>

  <div class=\"row\">
    <label>Current roll:
      <select v-model.number=\"currentRoll\">
        <option :value=\"1\">Roll 1</option>
        <option :value=\"2\">Roll 2</option>
        <option :value=\"3\">Roll 3</option>
      </select>
    </label>
    <span>Rolls remaining: <strong>{{ rollsRemaining }}</strong></span>
  </div>

  <div class=\"dice-grid\">
    <div
      v-for=\"(die, i) in dice\"
      :key=\"i\"
      :class=\"['die', {kept: keep[i]}]\"
      @click=\"toggleKeep(i)\"
      :id=\"`die-${i}`\"
    >
      <div>#{{ i + 1 }}</div>
      <div class=\"value\">{{ die }}</div>
      <div>{{ keep[i] ? 'KEPT' : 'ROLL' }}</div>
      <div class=\"controls\" @click.stop>
        <button class=\"secondary\" @click=\"adjust(i, -1)\">-</button>
        <button class=\"secondary\" @click=\"adjust(i, 1)\">+</button>
      </div>
    </div>
  </div>

  <div class=\"row\">
    <button class=\"primary\" @click=\"submit\">Enter</button>
    <button class=\"secondary\" @click=\"resetKeep\">Clear Keeps</button>
    <span v-if=\"loading\">Calculating...</span>
  </div>

  <table v-if=\"rows.length\">
    <thead><tr><th>Category</th><th>Probability</th><th>Visual</th></tr></thead>
    <tbody>
      <tr v-for=\"r in rows\" :key=\"r.name\">
        <td>{{ r.name }}</td>
        <td>{{ (r.value * 100).toFixed(1) }}%</td>
        <td><div class=\"bar\"><span :style=\"{ width: (r.value * 100) + '%' }\"></span></div></td>
      </tr>
    </tbody>
  </table>
</div>

<script>
const { createApp } = Vue;

createApp({
  data() {
    return {
      dice: [1,2,3,4,5],
      keep: [false,false,false,false,false],
      currentRoll: 1,
      rows: [],
      loading: false,
    }
  },
  computed: {
    rollsRemaining() { return Math.max(0, 3 - this.currentRoll); }
  },
  methods: {
    adjust(i, delta) {
      const next = this.dice[i] + delta;
      this.dice[i] = Math.min(6, Math.max(1, next));
    },
    toggleKeep(i) {
      this.keep[i] = !this.keep[i];
      anime({ targets: `#die-${i}`, scale: [1, 1.06, 1], duration: 220, easing: 'easeInOutSine' });
    },
    resetKeep() {
      this.keep = [false,false,false,false,false];
    },
    animateRoll() {
      this.dice.forEach((v, i) => {
        if (this.keep[i]) return;
        const id = `#die-${i}`;
        let ticks = 0;
        const timer = setInterval(() => {
          this.dice[i] = 1 + Math.floor(Math.random() * 6);
          ticks += 1;
          if (ticks > 8) clearInterval(timer);
        }, 60);
        anime({ targets: id, rotate: [0, 360], duration: 560, easing: 'easeOutBack' });
      });
    },
    async submit() {
      this.animateRoll();
      this.loading = true;
      try {
        const res = await fetch('/api/probabilities', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            dice: this.dice,
            keep: this.keep,
            rollsRemaining: this.rollsRemaining,
          })
        });
        const data = await res.json();
        this.rows = Object.entries(data.probabilities)
          .map(([name, value]) => ({name, value}))
          .sort((a, b) => b.value - a.value);
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') this.submit();
    });
    this.submit();
  }
}).mount('#app');
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/index.html"):
            data = INDEX_HTML.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/probabilities":
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length)

        try:
            body = json.loads(raw)
            dice = [int(x) for x in body["dice"]]
            keep = [bool(x) for x in body["keep"]]
            rolls_remaining = int(body["rollsRemaining"])
        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid payload"})
            return

        if len(dice) != 5 or len(keep) != 5 or any(v < 1 or v > 6 for v in dice):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Dice/keep format invalid"})
            return

        rolls_remaining = max(0, min(2, rolls_remaining))
        probs = estimate_probabilities(dice, keep, rolls_remaining)
        self._send_json(HTTPStatus.OK, {"probabilities": probs})


def run() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Yahtzee predictor running at http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
