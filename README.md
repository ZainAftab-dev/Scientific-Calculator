# Scientific Calculator

A feature-rich scientific calculator application with a modern GUI built in Python using Tkinter. Supports basic arithmetic operations, trigonometric functions, logarithms, and advanced mathematical operations.

**Created by:** Zain Aftab

---

## Features

### Basic Operations
- Addition, Subtraction, Multiplication, Division
- Percentage calculations
- Clear (C) and Clear Entry (CE) functions
- Backspace for removing last digit

### Scientific Functions
- **Trigonometry:** sin, cos, tan, asin, acos, atan
- **Logarithms:** log₂, log₁₀, natural logarithm (ln)
- **Powers & Roots:** x², x³, x^n (custom power), √ (square root)
- **Advanced:** Reciprocal (1/x), Factorial (!)
- **Constants:** π (pi) and e

### Advanced Features
- Support for parentheses in expressions
- Input validation for all operations
- Error handling for edge cases (division by zero, invalid domain values)
- Full error messages for better user experience
- Prevention of consecutive operators
- Decimal point validation

### User Interface
- Dark theme with color-coded buttons
- Large, readable display with green text on dark background
- Responsive grid layout
- Button categories:
  - **Red buttons:** Clear and Equals operations
  - **Teal buttons:** Arithmetic operators
  - **Gray buttons:** Scientific functions
  - **White buttons:** Numbers and decimal

---

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes pre-installed with Python)

### Verify Tkinter Installation
```bash
python -m tkinter
```
If a small window opens, Tkinter is installed.

---

## Installation & Setup

### Method 1: Direct Download
1. Download or clone the project
2. Ensure Python is installed on your system
3. No additional packages needed - Tkinter is included with Python

### Method 2: Using Virtual Environment (Recommended)
```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

---

## How to Run in VS Code

### Quick Start
1. Open the project folder in VS Code
2. Press `Ctrl + `` (backtick) to open the Terminal
3. Run the calculator:
   ```bash
   python scripts/scientific_calculator.py
   ```

### Alternative Method
1. Right-click on `scientific_calculator.py` in the file explorer
2. Select **"Run Python File in Terminal"**

### Using Python Interpreter
1. Click on the Python file
2. Click the **▶ Run** button in the top-right corner
3. Select your Python interpreter if prompted

---

## Usage Guide

### Input Methods

**Using Mouse:**
- Click any button to add it to the display
- Click equals (=) to calculate the result

**Using Keyboard:**
- Type numbers: 0-9
- Type operators: `+`, `-`, `*`, `/`, `%`
- Type parentheses: `(`, `)`
- Press `Enter` or `=` to calculate
- Press `Backspace` to delete last digit
- Press `Escape` to clear all (like C button)

### Example Calculations

1. **Basic:** `5 + 3 =` → Result: `8`
2. **Powers:** `2 x^n 10 =` → Result: `1024`
3. **Trigonometry:** `sin(π/2) =` → Result: `1.0`
4. **Logarithms:** `log₁₀(100) =` → Result: `2.0`
5. **Complex:** `(√16 + 5) × 2 =` → Result: `18.0`

### Keyboard Shortcuts

| Key | Function |
|-----|----------|
| `0-9` | Enter digits |
| `+`, `-`, `*`, `/`, `%` | Operators |
| `(`, `)` | Parentheses |
| `Enter` or `=` | Calculate |
| `Backspace` | Delete last digit |
| `Escape` | Clear all (C) |

---

## Error Handling

The calculator gracefully handles:
- **Division by zero:** Shows "Error: Cannot divide by zero"
- **Invalid trigonometric input:** Shows "Error: asin/acos input must be between -1 and 1"
- **Negative logarithms:** Shows "Error: Cannot take log of non-positive number"
- **Negative square root:** Shows "Error: Cannot take sqrt of negative number"
- **Large factorials:** Limited to 170 to prevent overflow
- **Mismatched parentheses:** Shows "Error: Mismatched parentheses"
- **Incomplete expressions:** Shows "Error: Incomplete expression"

---

## Technical Details

### Architecture
- **Class-based design:** `ScientificCalculator` class encapsulates all functionality
- **Safe evaluation:** Uses restricted namespace for eval() to prevent security issues
- **State tracking:** Tracks operator state to prevent invalid inputs
- **Error propagation:** All errors are caught and displayed to the user

### Color Scheme
- **Background:** `#1e1e1e` (Dark Gray)
- **Display:** `#2d2d2d` (Darker Gray) with `#00ff00` (Green text)
- **Buttons:** 
  - Standard: `#3d3d3d` (Medium Gray)
  - Operators: `#17a2b8` (Teal)
  - Clear/Equals: `#dc3545` (Red)
  - Scientific: `#6c757d` (Dark Gray)

### Mathematical Libraries Used
- **math module:** For trigonometric, logarithmic, and factorial functions

---

## Troubleshooting

### Issue: Tkinter not found
**Solution:** Install tkinter
```bash
# Windows
pip install tk

# macOS
brew install python-tk

# Linux
sudo apt-get install python3-tk
```

### Issue: Calculator window doesn't open
**Solution:** Check Python path in VS Code
1. Go to View → Command Palette (Ctrl+Shift+P)
2. Type "Python: Select Interpreter"
3. Choose the correct Python version

### Issue: Buttons not responding
**Solution:** Click the calculator window to ensure it has focus, then try again

---

## File Structure

```
scientific-calculator/
├── scripts/
│   └── scientific_calculator.py    # Main calculator application
├── README.md                        # This file
└── [other project files]
```

---

## License

This project is open-source and available for educational and personal use.

---

## Contact & Support

**Author:** Zain Aftab

For issues, questions, or suggestions, feel free to reach out.

---

## Changelog

### Version 1.0
- Initial release
- 40+ scientific functions
- Full error handling
- Dark theme GUI
- Keyboard support

---

## Future Enhancements

- [ ] History of calculations
- [ ] Conversion tools (units, bases)
- [ ] Custom variables
- [ ] Graphing functions
- [ ] Scientific notation display
- [ ] Undo/Redo functionality

---

**Enjoy your scientific calculator! Happy calculating! 🧮**
