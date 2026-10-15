import math
import re
import tkinter as tk
from tkinter import font

# Palette: graphite body, amber operators, coral clear key
BG = "#121418"
BODY = "#1a1d23"
SCREEN = "#0c0e11"
SCREEN_EDGE = "#262a32"
TEXT = "#f3eee4"
MUTED = "#7c8492"
AMBER = "#ffb547"
CORAL = "#ff7a6e"
ERROR = "#ff8a7a"

KEY_STYLES = {
    "fn": {"bg": "#20242c", "fg": "#9fc2dc", "hover": "#2a2f39", "press": "#333945"},
    "num": {"bg": "#2b3039", "fg": TEXT, "hover": "#353b46", "press": "#414854"},
    "op": {"bg": "#3a3020", "fg": AMBER, "hover": "#463926", "press": "#54442a"},
    "clear": {"bg": "#3a2424", "fg": CORAL, "hover": "#462b2b", "press": "#553333"},
    "edit": {"bg": "#262a32", "fg": "#c9ced6", "hover": "#30353e", "press": "#3a404a"},
    "eq": {"bg": AMBER, "fg": "#1d1407", "hover": "#ffc46c", "press": "#e9a23a"},
}

SCI_KEYS = [
    ["sin", "cos", "tan", "π", "e"],
    ["asin", "acos", "atan", "(", ")"],
    ["ln", "log₁₀", "log₂", "x²", "x³"],
    ["√", "1/x", "n!", "xʸ", "mod"],
]

NUM_KEYS = [
    [("AC", "clear"), ("CE", "edit"), ("⌫", "edit"), ("÷", "op")],
    [("7", "num"), ("8", "num"), ("9", "num"), ("×", "op")],
    [("4", "num"), ("5", "num"), ("6", "num"), ("−", "op")],
    [("1", "num"), ("2", "num"), ("3", "num"), ("+", "op")],
    [("0", "num"), (".", "num"), ("±", "num"), ("=", "eq")],
]

OPERATORS = ["÷", "×", "−", "+", "^", "%"]
UNARY = ["sin", "cos", "tan", "asin", "acos", "atan", "ln", "log₁₀", "log₂", "x²", "x³", "√", "1/x", "n!"]


def pick_family(root, choices, fallback):
    available = set(font.families(root))
    for name in choices:
        if name in available:
            return name
    return fallback


class Key(tk.Canvas):
    """A rounded calculator key drawn on a canvas so colours look the same on every OS."""

    def __init__(self, parent, text, style, command, key_font, radius=12):
        super().__init__(parent, bg=BODY, highlightthickness=0, bd=0, height=46, width=60, cursor="hand2", takefocus=0)
        self.text = text
        self.colors = KEY_STYLES[style]
        self.command = command
        self.key_font = key_font
        self.radius = radius
        self.fill = self.colors["bg"]
        self.bind("<Configure>", lambda e: self.draw())
        self.bind("<Enter>", lambda e: self.set_fill(self.colors["hover"]))
        self.bind("<Leave>", lambda e: self.set_fill(self.colors["bg"]))
        self.bind("<ButtonPress-1>", lambda e: self.set_fill(self.colors["press"]))
        self.bind("<ButtonRelease-1>", self.release)

    def rounded(self, x1, y1, x2, y2, r):
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, fill=self.fill, outline="")

    def draw(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 4 or h < 4:
            return
        self.rounded(1, 1, w - 1, h - 1, min(self.radius, h // 2))
        self.create_text(w / 2, h / 2, text=self.text, fill=self.colors["fg"], font=self.key_font)

    def set_fill(self, color):
        self.fill = color
        self.draw()

    def flash(self):
        self.set_fill(self.colors["press"])
        self.after(110, lambda: self.set_fill(self.colors["bg"]))

    def release(self, event):
        inside = 0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height()
        self.set_fill(self.colors["hover"] if inside else self.colors["bg"])
        if inside:
            self.command(self.text)


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.configure(bg=BG)
        self.root.minsize(380, 640)

        self.display_var = tk.StringVar(value="0")
        self.expr_var = tk.StringVar(value="")
        self.mode_var = tk.StringVar(value="DEG")
        self.degrees = True
        self.last_was_operator = False
        self.is_error = False
        self.just_evaluated = False
        self.history = []
        self.history_open = False
        self.keys = {}

        ui = pick_family(root, ["Segoe UI Variable Text", "Segoe UI", "SF Pro Text", "Helvetica Neue", "Inter", "Ubuntu", "Cantarell", "DejaVu Sans"], "Helvetica")
        mono = pick_family(root, ["Cascadia Mono", "SF Mono", "Menlo", "Consolas", "JetBrains Mono", "Ubuntu Mono", "DejaVu Sans Mono"], "Courier")
        self.mono = mono
        self.display_size = 34
        self.display_font = font.Font(family=mono, size=self.display_size, weight="bold")
        self.expr_font = font.Font(family=mono, size=12)
        self.key_font = font.Font(family=ui, size=15, weight="bold")
        self.fn_font = font.Font(family=ui, size=12, weight="bold")
        self.small_font = font.Font(family=ui, size=10, weight="bold")
        self.tape_font = font.Font(family=mono, size=11)

        self.build()
        self.bind_keys()

    # ---------- layout ----------

    def build(self):
        self.shell = tk.Frame(self.root, bg=BG)
        self.shell.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        self.body = tk.Frame(self.shell, bg=BODY, padx=14, pady=14, highlightbackground="#272b33", highlightthickness=1)
        self.body.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        header = tk.Frame(self.body, bg=BODY)
        header.pack(fill=tk.X, pady=(0, 10))
        tk.Label(header, text="SCIENTIFIC", bg=BODY, fg=MUTED, font=self.small_font).pack(side=tk.LEFT)
        self.history_btn = tk.Label(header, text="History", bg="#262a32", fg="#c9ced6", font=self.small_font, padx=10, pady=3, cursor="hand2")
        self.history_btn.pack(side=tk.RIGHT)
        self.history_btn.bind("<Button-1>", lambda e: self.toggle_history())
        self.mode_btn = tk.Label(header, textvariable=self.mode_var, bg="#3a3020", fg=AMBER, font=self.small_font, padx=10, pady=3, cursor="hand2")
        self.mode_btn.pack(side=tk.RIGHT, padx=(0, 6))
        self.mode_btn.bind("<Button-1>", lambda e: self.toggle_mode())

        screen = tk.Frame(self.body, bg=SCREEN, padx=16, pady=12, highlightbackground=SCREEN_EDGE, highlightthickness=1)
        screen.pack(fill=tk.X)
        tk.Label(screen, textvariable=self.expr_var, bg=SCREEN, fg=MUTED, font=self.expr_font, anchor="e").pack(fill=tk.X)
        self.display = tk.Label(screen, textvariable=self.display_var, bg=SCREEN, fg=TEXT, font=self.display_font, anchor="e", height=1)
        self.display.pack(fill=tk.X, pady=(2, 0))
        self.display_var.trace_add("write", lambda *a: self.fit_display())
        screen.bind("<Configure>", lambda e: self.fit_display())

        sci = tk.Frame(self.body, bg=BODY)
        sci.pack(fill=tk.BOTH, expand=True, pady=(14, 8))
        for r, row in enumerate(SCI_KEYS):
            sci.grid_rowconfigure(r, weight=1, uniform="sci")
            for c, text in enumerate(row):
                sci.grid_columnconfigure(c, weight=1, uniform="sci")
                key = Key(sci, text, "fn", self.on_button_press, self.fn_font, radius=10)
                key.configure(height=38)
                key.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)
                self.keys[text] = key

        tk.Frame(self.body, bg="#272b33", height=1).pack(fill=tk.X, pady=4)

        pad = tk.Frame(self.body, bg=BODY)
        pad.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
        for r, row in enumerate(NUM_KEYS):
            pad.grid_rowconfigure(r, weight=1, uniform="pad")
            for c, (text, style) in enumerate(row):
                pad.grid_columnconfigure(c, weight=1, uniform="pad")
                key = Key(pad, text, style, self.on_button_press, self.key_font, radius=14)
                key.configure(height=54)
                key.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)
                self.keys[text] = key

        self.tape = tk.Frame(self.shell, bg=BODY, padx=14, pady=14, highlightbackground="#272b33", highlightthickness=1, width=240)
        top = tk.Frame(self.tape, bg=BODY)
        top.pack(fill=tk.X, pady=(0, 10))
        tk.Label(top, text="HISTORY", bg=BODY, fg=MUTED, font=self.small_font).pack(side=tk.LEFT)
        clear = tk.Label(top, text="Clear", bg="#262a32", fg="#c9ced6", font=self.small_font, padx=10, pady=3, cursor="hand2")
        clear.pack(side=tk.RIGHT)
        clear.bind("<Button-1>", lambda e: self.clear_history())
        self.tape_list = tk.Frame(self.tape, bg=BODY)
        self.tape_list.pack(fill=tk.BOTH, expand=True)
        self.render_history()

    def fit_display(self):
        text = self.display_var.get()
        width = max(self.display.winfo_width(), 200) - 8
        size = 34
        self.display_font.configure(size=size)
        while size > 14 and self.display_font.measure(text) > width:
            size -= 2
            self.display_font.configure(size=size)
        self.display.configure(fg=ERROR if self.is_error else TEXT)

    def toggle_history(self):
        self.history_open = not self.history_open
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        self.root.geometry(f"{w + 252 if self.history_open else max(420, w - 252)}x{h}")
        if self.history_open:
            self.tape.pack(side=tk.LEFT, fill=tk.Y, padx=(12, 0))
            self.tape.pack_propagate(False)
            self.history_btn.configure(bg="#3a3020", fg=AMBER)
            self.render_history()
        else:
            self.tape.pack_forget()
            self.history_btn.configure(bg="#262a32", fg="#c9ced6")

    def render_history(self):
        for child in self.tape_list.winfo_children():
            child.destroy()
        if not self.history:
            tk.Label(self.tape_list, text="Results appear here.\nClick one to reuse it.", bg=BODY, fg=MUTED, font=self.tape_font, justify=tk.LEFT, anchor="w").pack(fill=tk.X)
            return
        for expr, result in reversed(self.history[-12:]):
            row = tk.Frame(self.tape_list, bg=BODY, cursor="hand2", pady=6)
            row.pack(fill=tk.X)
            a = tk.Label(row, text=expr + " =", bg=BODY, fg=MUTED, font=self.tape_font, anchor="e")
            a.pack(fill=tk.X)
            b = tk.Label(row, text=result, bg=BODY, fg=TEXT, font=font.Font(family=self.mono, size=15, weight="bold"), anchor="e")
            b.pack(fill=tk.X)
            for w in (row, a, b):
                w.bind("<Button-1>", lambda e, value=result: self.reuse(value))
            tk.Frame(self.tape_list, bg="#272b33", height=1).pack(fill=tk.X)

    def clear_history(self):
        self.history = []
        self.render_history()

    def reuse(self, value):
        self.display_var.set(value)
        self.expr_var.set("")
        self.is_error = False
        self.last_was_operator = False
        self.just_evaluated = True
        self.fit_display()

    def toggle_mode(self):
        self.degrees = not self.degrees
        self.mode_var.set("DEG" if self.degrees else "RAD")

    # ---------- keyboard ----------

    def bind_keys(self):
        mapping = {
            "<Return>": "=", "<KP_Enter>": "=", "<BackSpace>": "⌫", "<Escape>": "AC", "<Delete>": "CE",
            "<KP_Add>": "+", "<KP_Subtract>": "−", "<KP_Multiply>": "×", "<KP_Divide>": "÷", "<KP_Decimal>": ".",
        }
        for seq, key in mapping.items():
            self.root.bind(seq, lambda e, k=key: self.press_from_keyboard(k))
        self.root.bind("<Key>", self.on_key)

    def on_key(self, event):
        ch = event.char
        table = {"*": "×", "/": "÷", "-": "−", "+": "+", "^": "xʸ", "%": "mod", "=": "=", "(": "(", ")": ")", ".": ".", "!": "n!", "p": "π", "e": "e"}
        if ch.isdigit():
            self.press_from_keyboard(ch)
        elif ch in table:
            self.press_from_keyboard(table[ch])

    def press_from_keyboard(self, text):
        key = self.keys.get(text)
        if key:
            key.flash()
        self.on_button_press(text)

    # ---------- logic ----------

    def set_error(self, message):
        self.display_var.set(message)
        self.is_error = True
        self.just_evaluated = False
        self.fit_display()

    def set_result(self, label, value):
        shown = self.format_number(value)
        self.expr_var.set(label + " =")
        self.history.append((label, shown))
        if self.history_open:
            self.render_history()
        self.display_var.set(shown)
        self.is_error = False
        self.last_was_operator = False
        self.just_evaluated = True
        self.fit_display()

    @staticmethod
    def format_number(value):
        if isinstance(value, int):
            return str(value)
        value = round(value, 10)
        if value == int(value) and abs(value) < 1e15:
            return str(int(value))
        return repr(value)

    def current_value(self):
        """The number on screen, evaluating the expression first if needed."""
        current = self.display_var.get()
        try:
            return float(current)
        except ValueError:
            result = self.evaluate(current)
            if isinstance(result, str):
                raise ValueError(result)
            return float(result)

    def on_button_press(self, text):
        current = self.display_var.get()

        if self.is_error and text not in ["AC", "CE", "⌫"]:
            self.display_var.set("0")
            self.is_error = False
            current = "0"
            if text in OPERATORS or text in ["xʸ", "mod", ")"]:
                return

        if text == "AC":
            self.display_var.set("0")
            self.expr_var.set("")
            self.last_was_operator = False
            self.is_error = False
            self.just_evaluated = False
        elif text == "CE":
            trimmed = re.sub(r"[0-9.]+$", "", current) if not self.is_error else ""
            self.display_var.set(trimmed or "0")
            self.last_was_operator = bool(trimmed) and trimmed[-1] in OPERATORS
            self.is_error = False
        elif text == "⌫":
            if self.is_error or len(current) <= 1 or self.just_evaluated:
                self.display_var.set("0")
            else:
                self.display_var.set(current[:-1])
            self.last_was_operator = self.display_var.get()[-1] in OPERATORS
            self.is_error = False
            self.just_evaluated = False
        elif text == "=":
            if current in ["0", ""] or current[-1] in OPERATORS + ["("]:
                self.set_error("Error: Incomplete")
            else:
                result = self.evaluate(current)
                if isinstance(result, str):
                    self.expr_var.set(current + " =")
                    self.set_error(result)
                else:
                    self.set_result(current, result)
        elif text in UNARY:
            self.apply_function(text, current)
        elif text in ["π", "e"]:
            value = math.pi if text == "π" else math.e
            if current == "0" or self.just_evaluated:
                self.display_var.set(repr(value))
            elif current[-1] in OPERATORS or current[-1] == "(":
                self.display_var.set(current + repr(value))
            else:
                self.display_var.set(repr(value))
            self.last_was_operator = False
            self.just_evaluated = False
        elif text == "±":
            if re.fullmatch(r"-?[0-9.]+(e[-+]?\d+)?", current) and current != "0":
                self.display_var.set(current[1:] if current.startswith("-") else "-" + current)
            elif current != "0":
                self.display_var.set("-(" + current + ")")
        elif text in ["xʸ", "mod"]:
            symbol = "^" if text == "xʸ" else "%"
            if not self.last_was_operator and current != "0":
                self.display_var.set(current + symbol)
                self.last_was_operator = True
                self.just_evaluated = False
        elif text == "(":
            self.display_var.set("(" if current == "0" or self.just_evaluated else current + "(")
            self.last_was_operator = False
            self.just_evaluated = False
        elif text == ")":
            if current.count("(") > current.count(")") and current[-1] not in OPERATORS + ["("]:
                self.display_var.set(current + ")")
            self.last_was_operator = False
        elif text in ["÷", "×", "−", "+"]:
            if self.last_was_operator:
                self.display_var.set(current[:-1] + text)
            elif current == "0" and text == "−":
                self.display_var.set("-")
            else:
                self.display_var.set(current + text)
            self.last_was_operator = True
            self.just_evaluated = False
        else:
            if self.just_evaluated:
                current = "0"
                self.just_evaluated = False
            last_number = re.split(r"[÷×−+^%()]", current)[-1]
            if text == "." and "." in last_number:
                pass
            elif current == "0" and text != ".":
                self.display_var.set(text)
            else:
                self.display_var.set(current + text)
            self.last_was_operator = False
            self.is_error = False
        self.fit_display()

    def apply_function(self, name, current):
        try:
            x = self.current_value()
        except ValueError as err:
            message = str(err)
            self.set_error(message if message.startswith("Error") else "Error: Invalid input")
            return

        shown = self.format_number(x)
        to_rad = math.radians if self.degrees else (lambda v: v)
        from_rad = math.degrees if self.degrees else (lambda v: v)
        labels = {"x²": f"{shown}²", "x³": f"{shown}³", "√": f"√({shown})", "1/x": f"1/{shown}", "n!": f"{shown}!"}
        label = labels.get(name, f"{name}({shown})")
        if name in ["sin", "cos", "tan", "asin", "acos", "atan"]:
            label += " " + self.mode_var.get().lower()

        try:
            if name == "sin":
                value = math.sin(to_rad(x))
            elif name == "cos":
                value = math.cos(to_rad(x))
            elif name == "tan":
                if self.degrees and (x - 90) % 180 == 0:
                    return self.set_error("Error: tan undefined")
                value = math.tan(to_rad(x))
            elif name in ["asin", "acos"]:
                if x < -1 or x > 1:
                    return self.set_error("Error: Range [-1,1]")
                value = from_rad(math.asin(x) if name == "asin" else math.acos(x))
            elif name == "atan":
                value = from_rad(math.atan(x))
            elif name in ["ln", "log₁₀", "log₂"]:
                if x <= 0:
                    return self.set_error("Error: Log domain")
                value = {"ln": math.log, "log₁₀": math.log10, "log₂": math.log2}[name](x)
            elif name == "x²":
                value = x ** 2
            elif name == "x³":
                value = x ** 3
            elif name == "√":
                if x < 0:
                    return self.set_error("Error: Negative sqrt")
                value = math.sqrt(x)
            elif name == "1/x":
                if x == 0:
                    return self.set_error("Error: Div by zero")
                value = 1 / x
            elif name == "n!":
                if x < 0:
                    return self.set_error("Error: Negative !")
                if x != int(x):
                    return self.set_error("Error: Must be integer")
                if x > 170:
                    return self.set_error("Error: Too large")
                value = math.factorial(int(x))
            else:
                return
        except (OverflowError, ValueError):
            return self.set_error("Error: Out of range")

        if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
            return self.set_error("Error: Out of range")
        self.set_result(label, value)

    def evaluate(self, expression):
        """Safely evaluate an arithmetic expression."""
        try:
            expression = expression.replace("÷", "/").replace("×", "*").replace("−", "-").replace("^", "**")

            if not expression or expression in ["+", "-", "*", "/", "**", "(", ")"]:
                return "Error: Incomplete"
            if expression.count("(") != expression.count(")"):
                return "Error: Mismatched ( )"
            if re.search(r"\*\*\s*\d{4,}", expression):
                return "Error: Too large"

            result = eval(expression, {"__builtins__": {}}, {})

            if isinstance(result, complex):
                return "Error: Complex result"
            if isinstance(result, float):
                if math.isinf(result):
                    return "Error: Div by zero"
                if math.isnan(result):
                    return "Error: Invalid result"
            if isinstance(result, int) and abs(result) > 10 ** 30:
                return float(result)
            return result
        except ZeroDivisionError:
            return "Error: Div by zero"
        except OverflowError:
            return "Error: Too large"
        except SyntaxError:
            return "Error: Invalid syntax"
        except Exception:
            return "Error: Invalid expression"


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("420x720")
    ScientificCalculator(root)
    root.mainloop()
