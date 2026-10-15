<div align="center">

# 🧮 Scientific Calculator (Python + Tkinter)

A desktop scientific calculator written in pure Python with Tkinter, with a graphite-and-amber design, keyboard input, degree/radian modes and a history tape. No third-party packages.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

<img src="docs/screenshot.png" alt="Scientific calculator with the history tape open" width="560"/>

</div>

---

## Features

| Group | Keys |
|---|---|
| Arithmetic | `+` `−` `×` `÷`, `xʸ` (power), `mod` (remainder), parentheses `(` `)`, `±` |
| Powers and roots | `x²`, `x³`, `√`, `1/x` |
| Trigonometry | `sin`, `cos`, `tan`, `asin`, `acos`, `atan` in degrees or radians |
| Logarithms | `ln`, `log₁₀`, `log₂` |
| Other | `n!` (factorial), constants `π` and `e` |
| Editing | `AC` (clear all), `CE` (clear the last number), `⌫` (delete last character) |

**Interface**
- Graphite body with rounded keys drawn on a canvas, so the colours look the same on Windows, macOS and Linux
- Key groups by colour: blue-grey scientific keys, dark number keys, amber operators, coral `AC` and a solid amber `=`
- Two-line display: the expression you just calculated sits above the result, and long numbers shrink to fit
- **DEG / RAD** chip in the header switches the angle mode
- **History** tape slides out beside the keypad; click any result to reuse it
- Hover and press states on every key; keys flash when you use the keyboard

**Keyboard**

| Key | Action | Key | Action |
|---|---|---|---|
| `0`–`9` `.` | Digits | `Enter` or `=` | Calculate |
| `+` `-` `*` `/` | Operators | `Backspace` | Delete last character |
| `^` | Power | `Delete` | Clear entry |
| `%` | Remainder | `Esc` | Clear all |
| `(` `)` | Brackets | `!` `p` `e` | Factorial, π, e |

**Input checks and error messages**
- Pressing a second operator replaces the first; a number can only have one decimal point; `)` is only added when a bracket is open
- Clear messages for division by zero, square root of a negative, log of a non-positive number, `asin`/`acos` outside [-1, 1], `tan(90°)`, mismatched brackets, incomplete expressions and huge powers
- Factorial limited to whole numbers from 0 to 170 (larger values overflow a float)
- Results rounded to 10 decimal places, with whole numbers shown without `.0`
- Expressions are evaluated with `eval` in a restricted namespace (no built-ins), so only arithmetic can run

## How to use

- Build an expression with the digit, operator and bracket keys, then press `=`.
- The scientific keys (`sin`, `√`, `x²`, `log₁₀`, `n!` …) act on **what is on the display**. If it is an expression, it is worked out first: `2 + 3` then `x²` gives `25`.
- After a result, typing a digit starts a new number, while an operator carries on from the result.

| You press | Display shows |
|---|---|
| `125 × 8 =` | `1000` |
| `2 xʸ 10 =` | `1024` |
| `( 4 + 5 ) × 2 =` | `18` |
| `90` then `sin` (DEG) | `1` |
| `π ÷ 2` then `sin` (RAD) | `1` |
| `100` then `log₁₀` | `2` |
| `5` then `n!` | `120` |

## Getting started

**Requirements:** Python 3.8 or newer with Tkinter (included in the standard Windows and macOS installers).

```bash
git clone https://github.com/ZainAftab-dev/Scientific-Calculator.git
cd Scientific-Calculator
python scripts/scientific_calculator.py
```

If Python says `No module named 'tkinter'`:

| OS | Fix |
|---|---|
| Windows / macOS | Reinstall Python from python.org and keep "tcl/tk and IDLE" ticked |
| Ubuntu / Debian | `sudo apt install python3-tk` |
| Fedora | `sudo dnf install python3-tkinter` |

## Project structure

```
Scientific-Calculator/
├── scripts/
│   └── scientific_calculator.py   # Key (rounded canvas key) and ScientificCalculator: layout, keyboard, history, evaluation
└── docs/
    └── screenshot.png
```

## Known limitations

- Scientific keys act on the whole display value; you can't nest them inside an expression (for example `2 + sin(30)` in one go)
- History is kept for the current session only

## Author

**Zain Aftab** · [GitHub](https://github.com/ZainAftab-dev) · [LinkedIn](https://www.linkedin.com/in/zain-aftab-563727295/)

## License

[MIT](LICENSE)
