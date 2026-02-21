import tkinter as tk
from tkinter import messagebox, Toplevel, simpledialog
import random
from collections import OrderedDict
import sys
import math
import os
import json

# -------------------------
# Kombatant Roster (Alphabetically Sorted)
# -------------------------
kombatants = OrderedDict(
    sorted({
        1: 'Baraka', 2: 'Cassie Cage', 3: 'Cetrion', 4: "D'Vorah",
        5: 'Erron Black', 6: 'Frost', 7: 'Geras', 8: 'Jacqui Briggs',
        9: 'Jade', 10: 'Jax Briggs', 11: 'Johnny Cage', 12: 'Kabal',
        13: 'Kano', 14: 'Kitana', 15: 'Kotal Kahn', 16: 'Kung Lao',
        17: 'Liu Kang', 18: 'Noob Saibot', 19: 'Raiden', 20: 'Scorpion',
        21: 'Shao Kahn', 22: 'Skarlet', 23: 'Sonya Blade', 24: 'Sub-Zero',
        25: 'Shang Tsung', 26: 'Nightwolf', 27: 'Sindel', 28: 'Joker',
        29: 'Spawn', 30: 'Terminator T-800', 31: 'Fujin', 32: 'Sheeva',
        33: 'Robocop', 34: 'Mileena', 35: 'Rain', 36: 'Rambo',
        37: 'Kollector'
    }.items(), key=lambda x: x[1])
)

# -------------------------
# Tree Node
# -------------------------
class TreeNode:
    def __init__(self, name, player_name=None, left=None, right=None):
        self.name = name
        self.player_name = player_name
        self.left = left
        self.right = right
        self.winner = None
        self.x = 0
        self.y = 0
        self.canvas_rect = None
        self.canvas_text = None

# -------------------------
# Tree Serialization
# -------------------------
def tree_to_dict(node):
    if node is None:
        return None
    return {
        "name": node.name,
        "player_name": node.player_name,
        "winner": node.winner,
        "left": tree_to_dict(node.left),
        "right": tree_to_dict(node.right)
    }

def dict_to_tree(data):
    if data is None:
        return None
    node = TreeNode(data["name"], data.get("player_name"))
    node.winner = data.get("winner")
    node.left = dict_to_tree(data.get("left"))
    node.right = dict_to_tree(data.get("right"))
    return node

# -------------------------
# Tournament Tree Generation
# -------------------------
def next_power_of_two(n):
    return 2 ** math.ceil(math.log2(n))

def generate_tree(entries):
    if len(entries) < 2:
        raise ValueError("Tournament must have at least 2 entries.")
    total = len(entries)
    required = next_power_of_two(total)
    for _ in range(required - total):
        entries.append(TreeNode("BYE"))
    random.shuffle(entries)
    round_nodes = entries
    while len(round_nodes) > 1:
        next_round = []
        i = 0
        while i < len(round_nodes):
            left = round_nodes[i]
            right = round_nodes[i+1] if i+1 < len(round_nodes) else TreeNode("BYE")
            if left.player_name and right.player_name and left.player_name == right.player_name:
                for j in range(i+2, len(round_nodes)):
                    if round_nodes[j].player_name != left.player_name:
                        right, round_nodes[j] = round_nodes[j], right
                        break
            parent = TreeNode("TBD", left=left, right=right)
            next_round.append(parent)
            i += 2
        round_nodes = next_round
    return round_nodes[0]

# -------------------------
# Audio Player (macOS afplay)
# -------------------------
import subprocess
import threading

class AudioPlayer:
    def __init__(self):
        self._proc = None
        self._lock = threading.Lock()

    def play(self, path, loop=False):
        self.stop()
        if not os.path.exists(path):
            return
        def _run():
            while True:
                with self._lock:
                    if self._proc is not None and self._proc.poll() is not None:
                        break
                try:
                    p = subprocess.Popen(
                        ["afplay", path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    with self._lock:
                        self._proc = p
                    p.wait()
                except Exception:
                    break
                if not loop:
                    break
        t = threading.Thread(target=_run, daemon=True)
        t.start()

    def stop(self):
        with self._lock:
            if self._proc and self._proc.poll() is None:
                self._proc.terminate()
            self._proc = None

# Global audio player instance
_audio = AudioPlayer()


# -------------------------
# "Test Your Might" Fire Screen
# -------------------------
class TestYourMightScreen:
    FIRE_COLORS = [
        "#FF0000", "#FF2200", "#FF4400", "#FF6600",
        "#FF8800", "#FFAA00", "#FFCC00", "#FFEE33",
    ]
    FIRE_CORE_COLORS = ["#FFD27A", "#FFC85A", "#FFB52B", "#FF9F1C"]

    def __init__(self, parent, on_done, position="center"):
        self.parent = parent
        self.on_done = on_done
        self.position = position
        self.win = Toplevel(parent)
        self.win.title("")
        self.win.configure(bg="black")
        self.win.resizable(False, False)
        self.win.overrideredirect(True)  # borderless

        self.W, self.H = 700, 460
        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        x = (sw - self.W) // 2
        if self.position == "bottom":
            y = max(0, sh - self.H - 28)
        else:
            y = (sh - self.H) // 2
        self.win.geometry(f"{self.W}x{self.H}+{x}+{y}")

        self.canvas = tk.Canvas(
            self.win, width=self.W, height=self.H,
            bg="black", highlightthickness=0
        )
        self.canvas.pack()

        self._alive = True
        self.frame = 0
        self.flames = []
        self.embers = []
        self._timer = 0          # counts frames until auto-close
        self._total_frames = 120 # ~4 seconds at 30ms
        self._text_ids = []

        self._draw_text()
        self._animate()

    def _draw_text(self):
        cx, cy = self.W // 2, self.H // 2

        # Shadow
        self.canvas.create_text(
            cx + 3, cy - 47,
            text="TEST YOUR MIGHT",
            font=("Impact", 42, "bold"),
            fill="#330000"
        )
        # Main title — stored for color animation
        self.title_id = self.canvas.create_text(
            cx, cy - 50,
            text="TEST YOUR MIGHT",
            font=("Impact", 42, "bold"),
            fill="#FF4400"
        )
        # Subtitle
        self.sub_id = self.canvas.create_text(
            cx, cy + 20,
            text="— M O R T A L   K O M B A T —",
            font=("Arial", 13, "bold"),
            fill="#882200"
        )
        # Floating skull — starts at rest position, will bob in _animate
        self.skull_y = float(cy + 80)
        self.skull_id = self.canvas.create_text(
            cx, self.skull_y,
            text="💀",
            font=("Arial", 38),
            fill="white"
        )

    def _animate(self):
        if not self._alive:
            return
        t = self.frame
        self.frame += 1
        self._timer += 1

        self._spawn_flames()
        self._update_flames(t)
        self._spawn_embers()
        self._update_embers(t)

        # Raise text above particles
        self.canvas.tag_raise(self.title_id)
        self.canvas.tag_raise(self.sub_id)
        self.canvas.tag_raise(self.skull_id)

        # Title color flicker
        fc = self.FIRE_COLORS[(t // 2) % len(self.FIRE_COLORS)]
        self.canvas.itemconfig(self.title_id, fill=fc)

        # Skull: float up and down, spin color between white and orange
        cx = self.W // 2
        cy = self.H // 2
        skull_bob = cy + 80 + math.sin(t * 0.12) * 14
        self.canvas.coords(self.skull_id, cx, skull_bob)
        skull_color = self.FIRE_COLORS[(t // 3) % len(self.FIRE_COLORS)]
        self.canvas.itemconfig(self.skull_id, fill=skull_color)

        if self._timer >= self._total_frames:
            self._finish()
            return

        self.win.after(33, self._animate)

    def _spawn_flames(self):
        # Build broad, teardrop-shaped "licks" from the floor for a less "dotty" fire effect.
        for _ in range(4):
            x = random.randint(25, self.W - 25)
            w = random.uniform(12, 22)
            h = random.uniform(90, 180)
            outer = self.canvas.create_polygon(0, 0, 0, 0, 0, 0, fill="#FF3300", outline="")
            core = self.canvas.create_polygon(0, 0, 0, 0, 0, 0, fill="#FFCC55", outline="")
            self.flames.append({
                "outer": outer,
                "core": core,
                "x": float(x),
                "base_y": float(self.H - random.randint(0, 12)),
                "height": h,
                "width": w,
                "life": random.randint(16, 28),
                "max_life": 28,
                "drift": random.uniform(-0.6, 0.6),
                "phase": random.uniform(0, math.tau),
            })

    def _update_flames(self, t):
        alive = []
        for f in self.flames:
            f["life"] -= 1
            f["x"] += f["drift"] + math.sin(t * 0.17 + f["phase"]) * 0.8
            f["height"] *= 0.982
            if f["life"] <= 0 or f["height"] < 25:
                self.canvas.delete(f["outer"])
                self.canvas.delete(f["core"])
                continue

            ratio = f["life"] / f["max_life"]
            width = max(4, f["width"] * (0.7 + ratio * 0.4))
            height = f["height"] * (0.8 + ratio * 0.4)
            tip_sway = math.sin(t * 0.21 + f["phase"]) * width * 0.55
            x, by = f["x"], f["base_y"]

            outer_pts = [
                x - width, by,
                x + width, by,
                x + width * 0.36, by - height * 0.48,
                x + tip_sway, by - height,
                x - width * 0.36, by - height * 0.48,
            ]
            core_w = width * 0.48
            core_h = height * 0.72
            core_pts = [
                x - core_w, by,
                x + core_w, by,
                x + core_w * 0.28, by - core_h * 0.46,
                x + tip_sway * 0.55, by - core_h,
                x - core_w * 0.28, by - core_h * 0.46,
            ]
            self.canvas.coords(f["outer"], *outer_pts)
            self.canvas.coords(f["core"], *core_pts)

            oc = self.FIRE_COLORS[min(len(self.FIRE_COLORS) - 1, int((1 - ratio) * 6) + 1)]
            cc = self.FIRE_CORE_COLORS[min(len(self.FIRE_CORE_COLORS) - 1, int((1 - ratio) * 3))]
            self.canvas.itemconfig(f["outer"], fill=oc)
            self.canvas.itemconfig(f["core"], fill=cc)
            alive.append(f)
        self.flames = alive

    def _spawn_embers(self):
        for _ in range(3):
            x = random.randint(22, self.W - 22)
            ember = self.canvas.create_rectangle(0, 0, 0, 0, fill="#FFAA33", outline="")
            self.embers.append({
                "id": ember,
                "x": float(x),
                "y": float(self.H - random.randint(4, 20)),
                "vx": random.uniform(-0.55, 0.55),
                "vy": random.uniform(-3.4, -1.8),
                "life": random.randint(18, 36),
                "max_life": 36,
                "size": random.uniform(1.4, 3.5),
                "phase": random.uniform(0, math.tau),
            })

    def _update_embers(self, t):
        alive = []
        for e in self.embers:
            e["life"] -= 1
            e["x"] += e["vx"] + math.sin(t * 0.14 + e["phase"]) * 0.2
            e["y"] += e["vy"]
            e["vy"] *= 0.985
            if e["life"] <= 0:
                self.canvas.delete(e["id"])
                continue

            ratio = e["life"] / e["max_life"]
            size = max(1.0, e["size"] * ratio)
            color = self.FIRE_COLORS[min(len(self.FIRE_COLORS) - 1, int((1 - ratio) * 7))]
            self.canvas.coords(e["id"], e["x"] - size, e["y"] - size, e["x"] + size, e["y"] + size)
            self.canvas.itemconfig(e["id"], fill=color)
            alive.append(e)
        self.embers = alive

    def _finish(self):
        self._alive = False
        self.win.destroy()
        self.on_done()


# -------------------------
# Skull-on-Fire Popup
# -------------------------
class SkullFirePopup:
    FIRE_COLORS = ["#FF3300", "#FF5500", "#FF7700", "#FFAA00", "#FFD45A"]

    def __init__(self, parent):
        self.parent = parent
        self.win = Toplevel(parent)
        self.win.title("")
        self.win.configure(bg="#000000")
        self.win.resizable(False, False)
        self.win.overrideredirect(True)

        self.W, self.H = 300, 220
        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        x = (sw - self.W) // 2
        y = max(0, sh - self.H - 18)
        self.win.geometry(f"{self.W}x{self.H}+{x}+{y}")

        self.canvas = tk.Canvas(self.win, width=self.W, height=self.H, bg="#000000", highlightthickness=0)
        self.canvas.pack()

        self.frame = 0
        self._alive = True
        self.flames = []
        self.skull = self.canvas.create_text(self.W // 2, self.H - 70, text="💀", font=("Arial", 60), fill="white")
        self.label = self.canvas.create_text(self.W // 2, self.H - 24, text="F I N I S H   H I M", font=("Impact", 16), fill="#CC0000")
        self._animate()

    def _spawn_flame(self):
        x = random.randint(35, self.W - 35)
        self.flames.append({
            "id": self.canvas.create_polygon(0, 0, 0, 0, 0, 0, fill="#FF5500", outline=""),
            "x": float(x),
            "base_y": float(self.H - 28),
            "w": random.uniform(8, 18),
            "h": random.uniform(45, 95),
            "life": random.randint(11, 20),
            "max_life": 20,
            "phase": random.uniform(0, math.tau),
        })

    def _animate(self):
        if not self._alive:
            return
        t = self.frame
        self.frame += 1

        for _ in range(4):
            self._spawn_flame()

        alive = []
        for f in self.flames:
            f["life"] -= 1
            if f["life"] <= 0:
                self.canvas.delete(f["id"])
                continue
            ratio = f["life"] / f["max_life"]
            tip = math.sin(t * 0.23 + f["phase"]) * f["w"] * 0.6
            x, by = f["x"], f["base_y"]
            h = f["h"] * (0.75 + ratio * 0.45)
            w = f["w"] * (0.55 + ratio * 0.6)
            pts = [
                x - w, by,
                x + w, by,
                x + w * 0.3, by - h * 0.45,
                x + tip, by - h,
                x - w * 0.3, by - h * 0.45,
            ]
            color = self.FIRE_COLORS[min(len(self.FIRE_COLORS) - 1, int((1 - ratio) * 4))]
            self.canvas.coords(f["id"], *pts)
            self.canvas.itemconfig(f["id"], fill=color)
            alive.append(f)
        self.flames = alive

        bob = math.sin(t * 0.19) * 5
        self.canvas.coords(self.skull, self.W // 2, self.H - 72 + bob)
        skull_color = self.FIRE_COLORS[(t // 3) % len(self.FIRE_COLORS)]
        self.canvas.itemconfig(self.skull, fill=skull_color)

        if self.frame >= 54:
            self._alive = False
            self.win.destroy()
            return

        self.win.after(33, self._animate)


# -------------------------
# Animated Winner Screen
# -------------------------
class WinnerScreen:
    # Base crown coordinates (relative to cx=0, cy_base=0)
    # Format: list of (rel_x, rel_y) pairs
    CROWN_BASE = [
        (-130,   0),   # BL base
        ( 130,   0),   # BR base
        ( 130, -110),  # right spike tip
        (  55,  -60),  # right inner dip
        (   0, -160),  # centre spike
        ( -55,  -60),  # left inner dip
        (-130, -110),  # left spike tip
    ]
    # Which indices are the three spike tips (for jewel placement)
    SPIKE_INDICES = [4, 6, 2]  # centre, left, right

    GOLD_SHIMMER = [
        "#FFD700", "#FFC200", "#FFE44D", "#FFEC8B",
        "#DAA520", "#FFF0A0", "#FFD700", "#FFA500",
        "#FFCC00", "#FFB700",
    ]
    JEWEL_COLORS = ["#EE3333", "#4444EE", "#22CC44"]

    def __init__(self, parent, winner_name):
        self.win = Toplevel(parent)
        self.win.title("🏆 Tournament Champion 🏆")
        self.win.configure(bg="#0a0a0a")
        self.win.resizable(False, False)

        self.W, self.H = 640, 540
        self.canvas = tk.Canvas(
            self.win, width=self.W, height=self.H,
            bg="#0a0a0a", highlightthickness=0
        )
        self.canvas.pack()

        self.winner_name = winner_name
        self.frame = 0
        self.sparkles = []
        self._alive = True
        self.win.protocol("WM_DELETE_WINDOW", self._on_close)

        # Crown anchor (centre-x, base-y) — this bobs up/down
        self.cx = self.W // 2
        self.cy_base_origin = 320  # resting position of crown base
        self.cy_base = float(self.cy_base_origin)

        self._draw_background()
        self._build_crown()
        self._draw_text()

        tk.Button(
            self.win, text="X  Close", command=self._on_close,
            bg="#1a1a1a", fg="#FFD700", activebackground="#333300",
            activeforeground="white", font=("Impact", 11),
            relief="flat", padx=14, pady=4
        ).pack(pady=6)

        self._animate()

    def _on_close(self):
        self._alive = False
        self.win.destroy()

    def _draw_background(self):
        cx, cy = self.W // 2, self.H // 2 - 30
        for r, c in [
            (300, "#191300"), (230, "#131000"), (170, "#0d0a00"),
            (110, "#080600"), (55,  "#040300"),
        ]:
            self.canvas.create_oval(
                cx - r*2, cy - r, cx + r*2, cy + r, fill=c, outline=""
            )

    def _crown_pts(self, bob=0.0, sway=0.0, wobble=0.0):
        """Compute animated crown polygon points."""
        cx = self.cx + sway
        cy = self.cy_base_origin + bob
        pts = []
        for i, (rx, ry) in enumerate(self.CROWN_BASE):
            # Spike tips get extra vertical wobble
            extra = wobble * math.sin(i * 1.3) if i in (2, 4, 6) else 0
            pts.extend([cx + rx, cy + ry + extra])
        return pts

    def _build_crown(self):
        """Create all crown canvas items at their initial positions."""
        cx, cy = self.cx, self.cy_base_origin

        # Halo rings (drawn first, behind crown)
        self.halo_outer = self.canvas.create_oval(
            cx-158, cy-195, cx+158, cy+22,
            outline="#443300", width=1, fill=""
        )
        self.halo_inner = self.canvas.create_oval(
            cx-145, cy-182, cx+145, cy+12,
            outline="#886600", width=2, fill=""
        )

        # Crown body polygon
        pts = self._crown_pts()
        self.crown_body = self.canvas.create_polygon(
            pts, fill="#FFD700", outline="#B8860B", width=2, smooth=False
        )

        # Decorative band (lower portion of crown)
        self.band_y_rel = -38   # relative to cy_base
        self.band_w = 130
        bx0, bx1 = cx - self.band_w, cx + self.band_w
        by0, by1 = cy + self.band_y_rel, cy
        self.crown_band = self.canvas.create_rectangle(
            bx0, by0, bx1, by1,
            fill="#DAA520", outline="#8B6914", width=1
        )

        # Rivets on band
        self.rivets = []
        for rx in range(cx - 105, cx + self.band_w + 1, 35):
            ov = self.canvas.create_oval(
                rx-5, by0+6, rx+5, by0+18,
                fill="#B8860B", outline="#FFD700", width=1
            )
            self.rivets.append((ov, rx - cx))  # store rel_x

        # Jewels — positions relative to crown base
        jewel_rel = [
            (0,   -162, 11),   # centre spike
            (-120, -112,  9),  # left spike
            ( 120, -112,  9),  # right spike
        ]
        self.jewels = []
        for (rjx, rjy, jr), jc in zip(jewel_rel, self.JEWEL_COLORS):
            ov = self.canvas.create_oval(
                cx+rjx-jr, cy+rjy-jr, cx+rjx+jr, cy+rjy+jr,
                fill=jc, outline="white", width=1
            )
            self.jewels.append({"id": ov, "color": jc, "rx": rjx, "ry": rjy, "r": jr})

        # Gleam flicker dots
        self.gleam_dots = []
        for i in range(12):
            grx = random.randint(-118, 118)
            gry = random.randint(-158, -4)
            d = self.canvas.create_oval(
                cx+grx-2, cy+gry-2, cx+grx+2, cy+gry+2,
                fill="white", outline=""
            )
            self.gleam_dots.append({"id": d, "rx": grx, "ry": gry, "phase": i * 7})

    def _draw_text(self):
        cx = self.W // 2
        self.canvas.create_text(
            cx, 378, text="T O U R N A M E N T   C H A M P I O N",
            font=("Impact", 11, "bold"), fill="#775500"
        )
        self.winner_text = self.canvas.create_text(
            cx, 415, text=self.winner_name,
            font=("Impact", 26, "bold"), fill="#FFD700"
        )
        self.canvas.create_text(
            cx, 453, text="*  F L A W L E S S   V I C T O R Y  *",
            font=("Impact", 11), fill="#CC0000"
        )

    def _animate(self):
        if not self._alive:
            return
        t = self.frame
        self.frame += 1

        # -- Crown physics: smooth bob + gentle sway + spike wobble --
        bob   = math.sin(t * 0.06) * 9          # main vertical bob
        sway  = math.sin(t * 0.04) * 3          # left-right sway
        wobble = math.sin(t * 0.09) * 5         # spike tip oscillation

        # Update crown body polygon
        pts = self._crown_pts(bob, sway, wobble)
        self.canvas.coords(self.crown_body, *pts)

        # Update band position
        cx = self.cx + sway
        cy = self.cy_base_origin + bob
        self.canvas.coords(
            self.crown_band,
            cx - self.band_w, cy + self.band_y_rel,
            cx + self.band_w, cy
        )

        # Update rivets
        by0 = cy + self.band_y_rel
        for ov, rel_x in self.rivets:
            rx = cx + rel_x
            self.canvas.coords(ov, rx-5, by0+6, rx+5, by0+18)

        # Update jewels
        for j in self.jewels:
            jx = cx + j["rx"]
            jy = cy + j["ry"]
            r  = j["r"]
            self.canvas.coords(j["id"], jx-r, jy-r, jx+r, jy+r)
            # flash white occasionally
            flash = (t % 30) < 2
            self.canvas.itemconfig(j["id"], fill="#FFFFFF" if flash else j["color"])

        # Update gleam dots
        for g in self.gleam_dots:
            gx = cx + g["rx"]
            gy = cy + g["ry"]
            on = ((t + g["phase"]) % 35) < 4
            fill = "white" if on else ""
            self.canvas.coords(g["id"], gx-2, gy-2, gx+2, gy+2)
            self.canvas.itemconfig(g["id"], fill=fill)

        # Update halos (bob with crown)
        hcx, hcy = cx, cy
        self.canvas.coords(self.halo_inner, hcx-145, hcy-182, hcx+145, hcy+12)
        self.canvas.coords(self.halo_outer, hcx-158, hcy-195, hcx+158, hcy+22)
        halo_cols = ["#AA8800", "#775500", "#332200", "#775500"]
        self.canvas.itemconfig(self.halo_inner, outline=halo_cols[(t // 7) % 4])

        # Crown shimmer colour
        ci = (t // 2) % len(self.GOLD_SHIMMER)
        self.canvas.itemconfig(self.crown_body, fill=self.GOLD_SHIMMER[ci])

        # Winner text pulse
        wc = self.GOLD_SHIMMER[(t // 3) % len(self.GOLD_SHIMMER)]
        self.canvas.itemconfig(self.winner_text, fill=wc)

        # Sparkles around the crown
        if t % 2 == 0:
            self._spawn_sparkle(cx, cy)
        self._update_sparkles()

        self.win.after(33, self._animate)   # ~30 fps

    def _spawn_sparkle(self, cx, cy):
        x = cx + random.randint(-140, 140)
        y = cy + random.randint(-165, 10)
        size = random.randint(1, 5)
        color = random.choice(["#FFD700", "#FFF0A0", "#FFFFFF", "#FFA500", "#FFCC44"])
        dot = self.canvas.create_oval(
            x-size, y-size, x+size, y+size, fill=color, outline=""
        )
        self.sparkles.append({
            "id": dot, "life": random.randint(12, 22), "max_life": 22,
            "x": float(x), "y": float(y),
            "vy": random.uniform(-1.4, -0.3),
            "vx": random.uniform(-0.4, 0.4),
        })

    def _update_sparkles(self):
        alive = []
        for s in self.sparkles:
            s["life"] -= 1
            s["x"] += s["vx"]
            s["y"] += s["vy"]
            if s["life"] > 0:
                ratio = s["life"] / s["max_life"]
                r = int(255 * ratio)
                g = int(180 * ratio)
                color = f"#{r:02x}{g:02x}00"
                sz = max(1, int(4 * ratio))
                x, y = s["x"], s["y"]
                self.canvas.coords(s["id"], x-sz, y-sz, x+sz, y+sz)
                self.canvas.itemconfig(s["id"], fill=color)
                alive.append(s)
            else:
                self.canvas.delete(s["id"])
        self.sparkles = alive


# -------------------------
# Character colour / icon palette (MK11 faction colours)
# -------------------------
CHAR_STYLE = {
    'Baraka':           ("#3d0a0a", "#8b1a1a", ">>"),
    'Cassie Cage':      ("#0a1a0a", "#2d5a1e", "USF"),
    'Cetrion':          ("#0a2a15", "#1a6b3a", "***"),
    "D'Vorah":          ("#1a2a00", "#4a6600", "~~~"),
    'Erron Black':      ("#2a1a00", "#6b4200", "[ ]"),
    'Frost':            ("#001a2a", "#0066aa", "***"),
    'Fujin':            ("#001a2a", "#0055bb", ">>>"),
    'Geras':            ("#1a1200", "#7a5c00", ":::"),
    'Jacqui Briggs':    ("#0a0a2a", "#2a2a8b", "[X]"),
    'Jade':             ("#002a10", "#007a30", "|||"),
    'Jax Briggs':       ("#1a0f00", "#5a3800", "==="),
    'Joker':            ("#1a0030", "#6600bb", "???"),
    'Johnny Cage':      ("#1a1500", "#7a6800", "JC"),
    'Kabal':            ("#0f0f0f", "#3a3a3a", "---"),
    'Kano':             ("#2a0000", "#880000", "(O)"),
    'Kitana':           ("#001030", "#002288", ">>>"),
    'Kollector':        ("#120a1a", "#4a2a6b", "$$$"),
    'Kotal Kahn':       ("#2a0800", "#993300", "[*]"),
    'Kung Lao':         ("#1a1000", "#665500", "(^)"),
    'Liu Kang':         ("#2a0000", "#880000", "~~>"),
    'Mileena':          ("#2a0020", "#880066", "><>"),
    'Nightwolf':        ("#0a150a", "#2a5a1a", "/|\\"),
    'Noob Saibot':      ("#050508", "#1a1a2a", ":::"),
    'Raiden':           ("#001530", "#003388", "~~~"),
    'Rain':             ("#000a2a", "#002299", "vvv"),
    'Rambo':            ("#1a0a00", "#553300", "->-"),
    'Robocop':          ("#0a0f15", "#2a4a5a", "[R]"),
    'Scorpion':         ("#2a1500", "#cc5500", "->-"),
    'Shang Tsung':      ("#0a1500", "#2a5500", ">>>"),
    'Shao Kahn':        ("#1a0005", "#660022", "[K]"),
    'Sheeva':           ("#1a001a", "#660066", "VVV"),
    'Sindel':           ("#15001a", "#550077", "~~~"),
    'Skarlet':          ("#2a0000", "#990000", "vvv"),
    'Sonya Blade':      ("#001a08", "#006622", "[S]"),
    'Spawn':            ("#050505", "#220000", "X"),
    'Sub-Zero':         ("#001525", "#004488", "***"),
    'Terminator T-800': ("#0f0f0f", "#333333", "[T]"),
}

# -------------------------
# MK11-style Character Select Screen
# -------------------------
class CharacterSelectScreen:
    COLS = 6
    TILE_W = 112
    TILE_H = 130
    PAD = 6
    GRID_LAYOUT = [
        [None, "Shang Tsung", "Shao Kahn", "Frost", "Nightwolf", None],
        ["Joker", "Johnny Cage", "Cassie Cage", "Sonya Blade", "Jax Briggs", "Spawn"],
        ["Scorpion", "Noob Saibot", "Baraka", "Raiden", "Jacqui Briggs", "Sub-Zero"],
        ["Kano", "Kabal", "Liu Kang", "Kitana", "Kung Lao", "Jade"],
        ["Robocop", "Skarlet", "Erron Black", "D'Vorah", "Kotal Kahn", "Sheeva"],
        ["Rambo", "Terminator T-800", "Geras", "Kollector", "Cetrion", "Mileena"],
        [None, "Sindel", "Fujin", "Rain", None, None],
    ]
    BG = "#0a0a0a"
    BORDER_DEFAULT = "#2a1500"
    BORDER_HOVER   = "#cc7700"
    BORDER_SEL     = "#ffd700"
    BORDER_TAKEN   = "#1a1a1a"

    def __init__(self, parent, player_number, kombatant_count,
                 globally_taken, on_submit, on_back=None):
        self.parent = parent
        self.player_number = player_number
        self.kombatant_count = kombatant_count
        self.globally_taken = globally_taken
        self.on_submit = on_submit
        self.on_back = on_back

        self.selected = []
        self.char_list = [c for c in kombatants.values() if isinstance(c, str)]
        self.portraits = {}

        # FIX 1: initialise confirm_btn to None BEFORE _build_ui draws tiles
        # so _on_tile_click never hits AttributeError mid-draw
        self.confirm_btn = None
        self.status_var  = None

        self._load_portraits()
        self._build_ui()

    def _load_portraits(self):
        try:
            from PIL import Image, ImageTk
            img_dir = "images"
            if os.path.isdir(img_dir):
                for name in self.char_list:
                    for ext in ("png", "jpg", "jpeg"):
                        path = os.path.join(img_dir, f"{name}.{ext}")
                        if os.path.exists(path):
                            img = Image.open(path).resize(
                                (self.TILE_W, self.TILE_H - 30), Image.LANCZOS
                            )
                            self.portraits[name] = ImageTk.PhotoImage(img)
                            break
        except ImportError:
            pass

    def _build_ui(self):
        for w in self.parent.winfo_children():
            w.destroy()
        self.parent.configure(bg=self.BG)

        # ── Row 1: Title bar ──────────────────────────────────────────────
        hdr = tk.Frame(self.parent, bg="#0d0d0d", pady=6)
        hdr.pack(fill="x")
        tk.Label(
            hdr,
            text=f"PLAYER {self.player_number}  —  SELECT {self.kombatant_count} "
                 f"FIGHTER{'S' if self.kombatant_count > 1 else ''}",
            font=("Impact", 16), fg="#cc3300", bg="#0d0d0d"
        ).pack()

        # ── Row 2: Name entry (always fully visible) ──────────────────────
        name_bar = tk.Frame(self.parent, bg="#0d0d0d", pady=6)
        name_bar.pack(fill="x")
        tk.Label(name_bar, text="PLAYER NAME:", font=("Impact", 15, "bold"),
                 fg="#8b0000", bg="#0d0d0d").pack(side="left", padx=(16, 8))
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(
            name_bar, textvariable=self.name_var, width=22,
            bg="#1a0a00", fg="#8b0000", insertbackground="#8b0000",
            font=("Impact", 16, "bold"), relief="solid", bd=1
        )
        name_entry.pack(side="left")
        name_entry.focus_set()

        # ── Row 3: Selection status ───────────────────────────────────────
        self.status_var = tk.StringVar(value=self._status_text())
        status_bar = tk.Frame(self.parent, bg="#110000", pady=4)
        status_bar.pack(fill="x")
        tk.Label(
            status_bar, textvariable=self.status_var,
            font=("Impact", 11), fg="#ff6600", bg="#110000"
        ).pack()

        # ── Row 4: Bottom action bar (packed BEFORE canvas so it's always visible)
        btn_bar = tk.Frame(self.parent, bg="#0a0000", pady=6)
        btn_bar.pack(fill="x", side="bottom")
        btn_bar.grid_columnconfigure(0, weight=1)
        btn_bar.grid_columnconfigure(1, weight=1)
        btn_bar.grid_columnconfigure(2, weight=1)

        if self.on_back:
            tk.Button(
                btn_bar, text="< BACK TO PREV PLAYER", command=self._back,
                bg="#1a0a00", fg="#cc5500", activebackground="#330e00",
                activeforeground="#ff8800", font=("Impact", 12),
                relief="flat", padx=14, pady=6, cursor="hand2"
            ).grid(row=0, column=0, sticky="w", padx=12)

        self.confirm_btn = tk.Button(
            btn_bar, text="CONFIRM SELECTION  >",
            command=self._submit,
            bg="#3a0000", fg="#ff6600", activebackground="#660000",
            activeforeground="#ffffff", font=("Impact", 14),
            relief="flat", padx=20, pady=6, cursor="hand2",
            state="disabled"
        )
        self.confirm_btn.grid(row=0, column=1)

        # ── Row 5: Scrollable character grid (expands to fill remaining space)
        self.layout_rows = [list(row) for row in self.GRID_LAYOUT]
        known_chars = set(self.char_list)
        placed = {name for row in self.layout_rows for name in row if name}
        missing = [name for name in self.char_list if name not in placed]
        while missing:
            chunk = missing[:self.COLS]
            missing = missing[self.COLS:]
            self.layout_rows.append(chunk + [None] * (self.COLS - len(chunk)))

        rows = len(self.layout_rows)
        grid_w = self.COLS * (self.TILE_W + self.PAD) + self.PAD
        grid_h = rows * (self.TILE_H + self.PAD) + self.PAD

        outer = tk.Frame(self.parent, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=8, pady=2)

        self.canvas = tk.Canvas(
            outer, bg="#050505", highlightthickness=0,
            scrollregion=(0, 0, grid_w, grid_h)
        )
        vsb = tk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)
        hsb = tk.Scrollbar(outer, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Ensure window is wide enough to show all columns without clipping
        min_w = grid_w + 30
        self.parent.minsize(min_w, 520)

        # FIX 2: single canvas-level click handler using coordinate maths
        # so the ENTIRE tile area (not just rect outline or text) is clickable
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Motion>",   self._on_canvas_motion)
        self.canvas.bind("<Leave>",    self._on_canvas_leave)
        self.canvas.bind("<MouseWheel>", self._on_scroll)
        self.canvas.bind("<Button-4>",   self._on_scroll)
        self.canvas.bind("<Button-5>",   self._on_scroll)

        self._hover_name = None   # track which tile the cursor is over

        # Stone-slab grid lines
        for col in range(self.COLS + 1):
            x = col * (self.TILE_W + self.PAD) + self.PAD // 2
            self.canvas.create_line(x, 0, x, grid_h, fill="#1a0800", width=1)
        for row_i in range(rows + 1):
            y = row_i * (self.TILE_H + self.PAD) + self.PAD // 2
            self.canvas.create_line(0, y, grid_w, y, fill="#1a0800", width=1)

        # Build position lookup: name -> (x0, y0)
        self._tile_positions = {}
        self.tile_ids = {}
        self._slot_lookup = {}
        for row_i, row in enumerate(self.layout_rows):
            for col, name in enumerate(row):
                if not name:
                    continue
                if name not in known_chars:
                    continue
                x0 = col * (self.TILE_W + self.PAD) + self.PAD
                y0 = row_i * (self.TILE_H + self.PAD) + self.PAD
                self._tile_positions[name] = (x0, y0)
                self._slot_lookup[(row_i, col)] = name
                self._draw_tile(name, x0, y0)

    # ── Coordinate-based hit testing ─────────────────────────────────────

    def _canvas_xy_to_name(self, event):
        """Convert a canvas mouse event to a character name (or None)."""
        # Account for canvas scroll offset
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        col = int(cx // (self.TILE_W + self.PAD))
        row = int(cy // (self.TILE_H + self.PAD))
        # Check we're inside the tile rectangle (not in padding)
        x0 = col * (self.TILE_W + self.PAD) + self.PAD
        y0 = row * (self.TILE_H + self.PAD) + self.PAD
        if x0 <= cx <= x0 + self.TILE_W and y0 <= cy <= y0 + self.TILE_H:
            return self._slot_lookup.get((row, col))
        return None

    def _on_canvas_click(self, event):
        name = self._canvas_xy_to_name(event)
        if name:
            self._on_tile_click(name)

    def _on_canvas_motion(self, event):
        name = self._canvas_xy_to_name(event)
        if name == self._hover_name:
            return
        # Un-hover old
        if self._hover_name:
            self._on_hover(self._hover_name, False)
        self._hover_name = name
        # Hover new
        if name:
            self._on_hover(name, True)

    def _on_canvas_leave(self, event):
        if self._hover_name:
            self._on_hover(self._hover_name, False)
            self._hover_name = None

    # ── Tile drawing ──────────────────────────────────────────────────────

    def _draw_tile(self, name, x0, y0):
        taken = name in self.globally_taken
        sel   = name in self.selected
        style = CHAR_STYLE.get(name, ("#0a0a15", "#222244", "?"))
        dark_bg, light_bg, icon = style

        if taken:
            bg_top, bg_bot, border = "#111111", "#0a0a0a", self.BORDER_TAKEN
        elif sel:
            bg_top, bg_bot, border = light_bg, dark_bg, self.BORDER_SEL
        else:
            bg_top, bg_bot, border = light_bg, dark_bg, self.BORDER_DEFAULT

        rect = self.canvas.create_rectangle(
            x0, y0, x0 + self.TILE_W, y0 + self.TILE_H,
            fill=bg_top, outline=border, width=2 if (sel or taken) else 1
        )

        if name in self.portraits:
            self.canvas.create_image(
                x0 + self.TILE_W // 2, y0 + (self.TILE_H - 30) // 2,
                image=self.portraits[name]
            )
        else:
            self.canvas.create_rectangle(
                x0 + 6, y0 + 6, x0 + self.TILE_W - 6, y0 + self.TILE_H - 36,
                fill=bg_bot, outline=""
            )
            self.canvas.create_text(
                x0 + self.TILE_W // 2, y0 + (self.TILE_H - 32) // 2,
                text=icon, font=("Arial", 28),
                fill="white" if not taken else "#333333"
            )

        # Name banner
        self.canvas.create_rectangle(
            x0, y0 + self.TILE_H - 36, x0 + self.TILE_W, y0 + self.TILE_H,
            fill="#0d0000" if not taken else "#080808", outline=""
        )
        self.canvas.create_text(
            x0 + self.TILE_W // 2, y0 + self.TILE_H - 18,
            text=name.upper(), font=("Impact", 9 if len(name) > 13 else 11),
            fill="#ff6600" if sel else ("#444444" if taken else "#dddddd"),
            width=self.TILE_W - 6
        )

        # Taken overlay
        if taken:
            self.canvas.create_line(
                x0+8, y0+8, x0+self.TILE_W-8, y0+self.TILE_H-34, fill="#550000", width=2)
            self.canvas.create_line(
                x0+self.TILE_W-8, y0+8, x0+8, y0+self.TILE_H-34, fill="#550000", width=2)
            self.canvas.create_text(
                x0+self.TILE_W//2, y0+(self.TILE_H-30)//2,
                text="TAKEN", font=("Impact", 13), fill="#550000")

        # Gold corner accents when selected
        if sel:
            sz = 10
            corners = [
                (x0,               y0,               x0+sz,             y0              ),
                (x0,               y0,               x0,                y0+sz           ),
                (x0+self.TILE_W-sz,y0,               x0+self.TILE_W,    y0              ),
                (x0+self.TILE_W,   y0,               x0+self.TILE_W,    y0+sz           ),
                (x0,               y0+self.TILE_H-sz,x0,                y0+self.TILE_H  ),
                (x0,               y0+self.TILE_H,   x0+sz,             y0+self.TILE_H  ),
                (x0+self.TILE_W-sz,y0+self.TILE_H,   x0+self.TILE_W,    y0+self.TILE_H  ),
                (x0+self.TILE_W,   y0+self.TILE_H-sz,x0+self.TILE_W,    y0+self.TILE_H  ),
            ]
            for c in corners:
                self.canvas.create_line(*c, fill="#ffd700", width=3)

        self.tile_ids[name] = {"rect": rect, "x0": x0, "y0": y0}

    # ── Interaction handlers ──────────────────────────────────────────────

    def _on_tile_click(self, name):
        if name in self.globally_taken:
            return
        if name in self.selected:
            self.selected.remove(name)
        else:
            if len(self.selected) >= self.kombatant_count:
                return
            self.selected.append(name)
        self._redraw_tile(name)
        if self.status_var:
            self.status_var.set(self._status_text())
        if self.confirm_btn:
            self.confirm_btn.config(
                state="normal" if len(self.selected) == self.kombatant_count else "disabled"
            )

    def _on_hover(self, name, entering):
        if name in self.globally_taken or name in self.selected:
            return
        ids = self.tile_ids.get(name, {})
        rect = ids.get("rect")
        if rect:
            self.canvas.itemconfig(
                rect, outline=self.BORDER_HOVER if entering else self.BORDER_DEFAULT
            )

    def _redraw_tile(self, name):
        ids = self.tile_ids.get(name, {})
        x0, y0 = ids.get("x0", 0), ids.get("y0", 0)
        for item in self.canvas.find_enclosed(x0-1, y0-1, x0+self.TILE_W+1, y0+self.TILE_H+1):
            self.canvas.delete(item)
        self._draw_tile(name, x0, y0)

    def _status_text(self):
        picks = ", ".join(self.selected) if self.selected else "--"
        return f"Selected ({len(self.selected)}/{self.kombatant_count}):  {picks}"

    def _on_scroll(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            delta = -1 if event.delta > 0 else 1
            self.canvas.yview_scroll(delta, "units")

    def _submit(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a player name.")
            return
        if len(self.selected) != self.kombatant_count:
            messagebox.showerror("Error", f"Select exactly {self.kombatant_count} fighter(s).")
            return
        self.on_submit(name, list(self.selected))

    def _back(self):
        if self.on_back:
            self.on_back()


# -------------------------
# Tournament GUI
# -------------------------
class TournamentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mortal Kombat Tournament Builder")
        self.player_data = []
        self.current_player_index = 0
        self.player_count = 0
        self.kombatant_count = 0
        self.root_node = None
        self.entries = []
        self.canvas = None
        self.canvas_frame = None
        self.current_save_file = None
        os.makedirs("tournament_saves", exist_ok=True)
        self.canvas_font = ("Beast", 10)
        self.audio = _audio
        self.main_menu_image_path = os.path.join("images", "main_menu.png")
        self._menu_logo_source = None
        self._menu_logo_cache = {}
        self._menu_logo_tk = None
        self._load_main_menu_logo_source()
        self.setup_initial_screen()

    def _load_main_menu_logo_source(self):
        self._menu_logo_source = None
        self._menu_logo_cache.clear()
        if not os.path.exists(self.main_menu_image_path):
            return
        try:
            from PIL import Image
            self._menu_logo_source = Image.open(self.main_menu_image_path).convert("RGBA")
        except Exception:
            self._menu_logo_source = None

    def _get_main_menu_logo(self, max_w, max_h):
        if self._menu_logo_source is None:
            return None
        max_w = max(1, int(max_w))
        max_h = max(1, int(max_h))
        key = (max_w, max_h)
        if key in self._menu_logo_cache:
            return self._menu_logo_cache[key]
        try:
            from PIL import ImageTk
            img = self._menu_logo_source.copy()
            img.thumbnail((max_w, max_h))
            tk_img = ImageTk.PhotoImage(img)
            self._menu_logo_cache[key] = tk_img
            return tk_img
        except Exception:
            return None

    # -------------------------
    # Initial Screen
    # -------------------------
    def setup_initial_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#000000")
        self.root.minsize(500, 380)
        self.audio.play(os.path.join("mp3", "main_menu.mp3"), loop=True)

        canvas = tk.Canvas(self.root, bg="#000000", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        def _draw(event=None):
            canvas.delete("all")
            W = canvas.winfo_width()
            H = canvas.winfo_height()
            if W < 2 or H < 2:   # not yet realised
                return
            cx, cy = W // 2, H // 2
            top_title_y = max(28, int(H * 0.08))
            top_subtitle_y = top_title_y + max(18, int(H * 0.04))
            # Background layered red glow
            for r, c in [(int(H*0.75),"#0d0000"),(int(H*0.57),"#110000"),
                         (int(H*0.40),"#160000"),(int(H*0.25),"#1c0000"),
                         (int(H*0.12),"#220000")]:
                canvas.create_oval(cx-r*2, cy-r, cx+r*2, cy+r, fill=c, outline="")

            # Decorative horizontal bars
            bw = int(W * 0.88)
            for dy, col in [(-int(H*0.18),"#cc0000"),(-int(H*0.175),"#880000"),
                             ( int(H*0.19),"#cc0000"),( int(H*0.185),"#880000")]:
                canvas.create_rectangle(cx-bw//2, cy+dy, cx+bw//2, cy+dy+3, fill=col, outline="")

            # Top text stays clear of menu art in both windowed and fullscreen layouts
            canvas.create_text(
                cx, top_title_y,
                text="MORTAL KOMBAT TOURNAMENT BUILDER",
                font=("Impact", max(16, int(H * 0.035)), "bold"),
                fill="#cc0000"
            )
            canvas.create_text(
                cx, top_subtitle_y,
                text="SELECT YOUR DESTINY",
                font=("Impact", max(10, int(H * 0.018))),
                fill="#ff8800"
            )
            logo = self._get_main_menu_logo(int(W * 0.72), int(H * 0.62))
            if logo:
                self._menu_logo_tk = logo  # keep reference alive
                canvas.create_image(cx, cy - int(H * 0.03), image=logo)
            else:
                # Logo box
                bx, by = int(W*0.26), int(H*0.17)
                canvas.create_rectangle(cx-bx, cy-by, cx+bx, cy+by,
                                         fill="#0a0000", outline="#cc0000", width=2)
                canvas.create_rectangle(cx-bx+4, cy-by+4, cx+bx-4, cy+by-4,
                                         fill="", outline="#550000", width=1)

                # Gold corner accents
                sz = 14
                for p0, p1 in [
                    ((cx-bx,    cy-by),(cx-bx+sz,cy-by)),  ((cx-bx,   cy-by),(cx-bx,   cy-by+sz)),
                    ((cx+bx-sz, cy-by),(cx+bx,   cy-by)),  ((cx+bx,   cy-by),(cx+bx,   cy-by+sz)),
                    ((cx-bx,    cy+by-sz),(cx-bx, cy+by)), ((cx-bx,   cy+by),(cx-bx+sz,cy+by)),
                    ((cx+bx-sz, cy+by),(cx+bx,   cy+by)),  ((cx+bx,   cy+by-sz),(cx+bx,cy+by)),
                ]:
                    canvas.create_line(*p0, *p1, fill="#ff6600", width=3)

                canvas.create_text(
                    cx, cy + int(H * 0.16),
                    text=f"Place menu art at: {self.main_menu_image_path}",
                    font=("Arial", 9), fill="#664444"
                )

            # Button frame — anchored lower-middle so text never collides with menu art
            buttons_y = min(H - 80, cy + int(H * 0.30))
            canvas.delete("btn_win")
            canvas.create_window(cx, buttons_y, window=btn_frame, tags="btn_win")

        # Build buttons once (outside _draw so they're not recreated on every resize)
        btn_frame = tk.Frame(canvas, bg="#000000")
        tk.Button(
            btn_frame, text="NEW TOURNAMENT", width=22,
            command=self.new_tournament_screen,
            bg="#1a0000", fg="#ff6600", activebackground="#330000",
            activeforeground="#ffffff", font=("Impact", 14),
            relief="flat", padx=10, pady=6, cursor="hand2"
        ).pack(pady=4)
        tk.Button(
            btn_frame, text="LOAD TOURNAMENT", width=22,
            command=self.load_saved_tournament,
            bg="#0d0000", fg="#cc4400", activebackground="#220000",
            activeforeground="#ff8800", font=("Impact", 14),
            relief="flat", padx=10, pady=6, cursor="hand2"
        ).pack(pady=4)

        canvas.bind("<Configure>", _draw)
        # Trigger an initial draw after widget is realised
        self.root.after(10, _draw)

    def new_tournament_screen(self):
        self.audio.stop()
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#0a0000")

        center = tk.Frame(self.root, bg="#0a0000")
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="NEW TOURNAMENT", font=("Beast", 16, "bold"),
                 fg="#cc0000", bg="#0a0000").pack(pady=(0, 18))

        tk.Label(center, text="Number of Players:", font=("Beast", 11),
                 fg="#ff6600", bg="#0a0000").pack(anchor="w")
        self.player_count_entry = tk.Entry(
            center, font=("Beast", 13), width=12,
            bg="#2a0000", fg="#ffffff", insertbackground="#ff6600",
            relief="solid", bd=2, highlightthickness=2,
            highlightcolor="#cc0000", highlightbackground="#550000"
        )
        self.player_count_entry.pack(pady=(2, 12), ipady=4)

        tk.Label(center, text="Kombatants per Player:", font=("Beast", 11),
                 fg="#ff6600", bg="#0a0000").pack(anchor="w")
        self.kombatant_count_entry = tk.Entry(
            center, font=("Beast", 13), width=12,
            bg="#2a0000", fg="#ffffff", insertbackground="#ff6600",
            relief="solid", bd=2, highlightthickness=2,
            highlightcolor="#cc0000", highlightbackground="#550000"
        )
        self.kombatant_count_entry.pack(pady=(2, 18), ipady=4)
        tk.Button(center, text="CONTINUE", command=self.start_player_input,
          bg="#cc0000", fg="#000000", activebackground="#ff0000",
          activeforeground="#000000", font=("Beast", 12),
          relief="flat", padx=20, pady=7, cursor="hand2").pack(pady=(0, 8))
        tk.Button(center, text="< BACK", command=self.setup_initial_screen,
                  bg="#0d0000", fg="#cc4400", activebackground="#1a0000",
                  activeforeground="#ff6600", font=("Beast", 10),
                  relief="flat", padx=10, pady=4, cursor="hand2").pack()

    def load_saved_tournament(self):
        self.audio.stop()
        folder = "tournament_saves"
        files = [f for f in os.listdir(folder) if f.endswith(".json")]
        if not files:
            messagebox.showinfo("Info", "No saved tournaments found.")
            return
        file_choice = tk.Toplevel(self.root)
        file_choice.title("Load Tournament")
        file_choice.configure(bg="#0a0000")
        tk.Label(file_choice, text="SELECT A TOURNAMENT:", font=("Beast", 12),
                 fg="#ff6600", bg="#0a0000").pack(pady=(14,4))
        var = tk.StringVar(file_choice)
        var.set(files[0])
        tk.OptionMenu(file_choice, var, *files).pack(pady=5)
        def load_file():
            path = os.path.join(folder, var.get())
            with open(path, "r") as f:
                data = json.load(f)
            self.root_node = dict_to_tree(data)
            self.current_save_file = path
            file_choice.destroy()
            self.show_bracket()
        tk.Button(file_choice, text="LOAD", command=load_file,
                  bg="#2a0000", fg="#ff6600", activebackground="#550000",
                  activeforeground="white", font=("Beast", 11),
                  relief="flat", padx=12, pady=5, cursor="hand2").pack(pady=8)

    # -------------------------
    # Player Input
    # -------------------------
    def start_player_input(self):
        try:
            self.player_count = int(self.player_count_entry.get())
            self.kombatant_count = int(self.kombatant_count_entry.get())
            if self.player_count < 1 or self.kombatant_count < 1:
                raise ValueError
        except:
            messagebox.showerror("Error", "Enter valid positive integers.")
            return
        self.player_data = []
        self.current_player_index = 0
        self.entries = []
        self.show_player_input()

    def show_player_input(self):
        # Start main theme on first player screen
        if self.current_player_index == 0:
            self.audio.play(os.path.join("mp3", "main_theme.mp3"), loop=True)
        CharacterSelectScreen(
            self.root,
            player_number=self.current_player_index + 1,
            kombatant_count=self.kombatant_count,
            globally_taken=set(),   # each player picks freely from full roster
            on_submit=self._on_player_submitted,
            on_back=self._on_player_back if self.current_player_index > 0 else None,
        )

    def _on_player_submitted(self, player_name, selected_list):
        """Called by CharacterSelectScreen when player confirms selection."""
        for val in selected_list:
            self.entries.append(TreeNode(f"{player_name} - {val}", player_name))
        self.player_data.append({"name": player_name, "kombatants": list(selected_list)})
        self.current_player_index += 1
        if self.current_player_index < self.player_count:
            self.show_player_input()
        else:
            self.audio.stop()
            self.generate_tournament()

    def _on_player_back(self):
        """Called by CharacterSelectScreen when player hits Back."""
        # Undo previous player's submission
        self.current_player_index -= 1
        prev = self.player_data.pop()
        # Remove that player's entries from self.entries
        count = len(prev["kombatants"])
        self.entries = self.entries[:-count]
        self.show_player_input()

    def _show_test_your_might(self, on_done, position="center"):
        TestYourMightScreen(self.root, on_done, position=position)

    # -------------------------
    # Generate Tournament
    # -------------------------
    def generate_tournament(self):
        try:
            self.root_node = generate_tree(self.entries)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self.show_bracket()

    # -------------------------
    # Scrollable Bracket & BYE Auto-Advance
    # -------------------------
    def show_bracket(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#0a0000")
        button_frame = tk.Frame(self.root, bg="#0a0000")
        button_frame.pack(pady=6)
        tk.Button(button_frame, text="START LIVE TRACKER",
                  command=self.open_live_tracker,
                  bg="#2a0000", fg="#ff6600", activebackground="#550000",
                  activeforeground="white", font=("Beast", 11),
                  relief="flat", padx=10, pady=5, cursor="hand2").pack(side="left", padx=6)
        tk.Button(button_frame, text="SAVE TOURNAMENT",
                  command=self.save_tournament,
                  bg="#0d0000", fg="#cc4400", activebackground="#220000",
                  activeforeground="#ff8800", font=("Beast", 11),
                  relief="flat", padx=10, pady=5, cursor="hand2").pack(side="left", padx=6)
        tk.Button(button_frame, text="RETURN TO MAIN MENU",
                  command=self.setup_initial_screen,
                  bg="#120000", fg="#ff8800", activebackground="#330000",
                  activeforeground="#ffffff", font=("Beast", 11),
                  relief="flat", padx=10, pady=5, cursor="hand2").pack(side="left", padx=6)
        tk.Label(self.root, text="TOURNAMENT BRACKET",
                 font=("Beast", 14, "bold"), fg="#cc0000", bg="#0a0000").pack(pady=4)

        leaf_nodes = []
        self.get_leaf_nodes(self.root_node, leaf_nodes)
        total_leaves = len(leaf_nodes)
        canvas_height = max(600, total_leaves * 80)
        depth = self.get_tree_depth(self.root_node)
        canvas_width = max(800, depth * 150 + 200)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, width=min(canvas_width, 1200), height=600, bg="black")
        hbar = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        vbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        hbar.grid(row=1, column=0, sticky="ew")
        vbar.grid(row=0, column=1, sticky="ns")
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        self.draw_tree_horizontal(self.root_node, self.canvas, 50, canvas_height/2, canvas_height/2)
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self._bind_scroll_events(self.canvas)

        self.auto_advance_byes(self.root_node)

    def _bind_scroll_events(self, canvas):
        def _on_mousewheel(event):
            if sys.platform == "darwin":
                canvas.yview_scroll(int(-1 * event.delta), "units")
            else:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        def _on_shift_mousewheel(event):
            if sys.platform == "darwin":
                canvas.xview_scroll(int(-1 * event.delta), "units")
            else:
                canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Shift-MouseWheel>", _on_shift_mousewheel)

    def get_leaf_nodes(self, node, leaf_list):
        if node is None:
            return
        if node.left is None and node.right is None:
            leaf_list.append(node)
        self.get_leaf_nodes(node.left, leaf_list)
        self.get_leaf_nodes(node.right, leaf_list)

    def get_tree_depth(self, node):
        if node is None:
            return 0
        return 1 + max(self.get_tree_depth(node.left), self.get_tree_depth(node.right))

    def draw_tree_horizontal(self, node, canvas, x, y, vertical_gap):
        if node is None:
            return
        if node.left:
            y_left = y - vertical_gap / 2 if vertical_gap > 20 else y - 20
            self.draw_tree_horizontal(node.left, canvas, x + 150, y_left, vertical_gap / 2)
            canvas.create_line(x + 100, y, node.left.x, node.left.y, fill="white")
        if node.right:
            y_right = y + vertical_gap / 2 if vertical_gap > 20 else y + 20
            self.draw_tree_horizontal(node.right, canvas, x + 150, y_right, vertical_gap / 2)
            canvas.create_line(x + 100, y, node.right.x, node.right.y, fill="white")
        node.x = x
        node.y = y
        text_width = max(100, len(node.name)*7)
        fill_color = "red" if node.name=="BYE" else "white"
        node.canvas_rect = canvas.create_rectangle(x, y-15, x+text_width, y+15, fill=fill_color)
        node.canvas_text = canvas.create_text(x + text_width/2, y, text=node.name, fill="black", font=self.canvas_font)

    def auto_advance_byes(self, node):
        if node is None or (node.left is None and node.right is None):
            return
        self.auto_advance_byes(node.left)
        self.auto_advance_byes(node.right)

        left_name = node.left.name if node.left else None
        right_name = node.right.name if node.right else None

        if left_name == "BYE" and right_name == "BYE":
            node.name = "BYE"
            node.winner = "BYE"
            self.update_node_color(node, "red")
        elif left_name == "BYE" and right_name != "BYE":
            node.name = right_name
            node.winner = right_name
            self.update_node_color(node, "green")
            self.update_node_color(node.right, "green")  # color the advancing leaf
        elif left_name != "BYE" and right_name == "BYE":
            node.name = left_name
            node.winner = left_name
            self.update_node_color(node, "green")
            self.update_node_color(node.left, "green")   # color the advancing leaf

    def update_node_color(self, node, color):
        if node.canvas_rect:
            self.canvas.itemconfig(node.canvas_rect, fill=color)
        if node.canvas_text:
            self.canvas.itemconfig(node.canvas_text, text=node.name)

    # -------------------------
    # Live Tracker
    # -------------------------
    def open_live_tracker(self):
        self._show_test_your_might(self._open_live_tracker_window, position="bottom")

    def _open_live_tracker_window(self):
        tracker = Toplevel(self.root)
        tracker.title("Live Tournament Tracker")
        tracker.configure(bg="#0a0a0a")
        self.live_frame = tk.Frame(tracker, bg="#0a0a0a")
        self.live_frame.pack(padx=20, pady=20)
        self.update_live(tracker)

    def get_next_match_nodes(self, node, matches):
        if node.left and node.right:
            left_ready = node.left.winner or not node.left.left
            right_ready = node.right.winner or not node.right.left
            if not node.winner and left_ready and right_ready and node.left.name != "TBD" and node.right.name != "TBD":
                matches.append(node)
        if node.left:
            self.get_next_match_nodes(node.left, matches)
        if node.right:
            self.get_next_match_nodes(node.right, matches)

    def update_live(self, tracker_window):
        for widget in self.live_frame.winfo_children():
            widget.destroy()

        matches = []
        self.get_next_match_nodes(self.root_node, matches)

        if not matches:
            self.audio.play(os.path.join("mp3", "victory.mp3"), loop=False)
            self.show_winner_screen(self.root_node.name)
            tracker_window.destroy()
            return

        self.current_node = matches[0]
        left_node = self.current_node.left
        right_node = self.current_node.right

        tk.Label(
            self.live_frame,
            text=f"NEXT MATCH",
            font=("Beast", 11, "bold"), fg="#cc3300", bg="#0a0a0a"
        ).pack(pady=(0, 2))
        tk.Label(
            self.live_frame,
            text=f"{left_node.name}  vs  {right_node.name}",
            font=("Beast", 13, "bold"), fg="#ff6600", bg="#0a0a0a"
        ).pack(pady=(0, 12))

        frame = tk.Frame(self.live_frame, bg="#0a0a0a")
        frame.pack()
        tk.Button(
            frame, text=left_node.name, width=22,
            command=lambda: self.select_winner(left_node, right_node, tracker_window),
            bg="#2a0000", fg="#ff6600", activebackground="#550000",
            activeforeground="white", font=("Beast", 11), relief="flat",
            padx=8, pady=6, cursor="hand2"
        ).pack(side="left", padx=10)
        tk.Button(
            frame, text=right_node.name, width=22,
            command=lambda: self.select_winner(right_node, left_node, tracker_window),
            bg="#2a0000", fg="#ff6600", activebackground="#550000",
            activeforeground="white", font=("Beast", 11), relief="flat",
            padx=8, pady=6, cursor="hand2"
        ).pack(side="left", padx=10)

    def select_winner(self, winner_node, loser_node, tracker_window):
        self.audio.play(os.path.join("mp3", "bracket.mp3"), loop=False)
        SkullFirePopup(self.root)
        self.current_node.winner = winner_node.name
        self.current_node.name = winner_node.name
        self.update_node_color(self.current_node, "green")
        if winner_node.canvas_rect:
            self.canvas.itemconfig(winner_node.canvas_rect, fill="green")
        if loser_node.canvas_rect:
            self.canvas.itemconfig(loser_node.canvas_rect, fill="red")
        self.update_live(tracker_window)

    # -------------------------
    # Winner Screen
    # -------------------------
    def show_winner_screen(self, winner_name):
        WinnerScreen(self.root, winner_name)

    # -------------------------
    # Save/Load Tournament
    # -------------------------
    def save_tournament(self):
        data = tree_to_dict(self.root_node)
        if not self.current_save_file:
            name = simpledialog.askstring("Save Tournament", "Enter tournament name:")
            if not name:
                return
            path = os.path.join("tournament_saves", f"{name}.json")
            self.current_save_file = path
        else:
            path = self.current_save_file
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Saved", f"Tournament saved to {path}")

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentGUI(root)
    root.mainloop()
