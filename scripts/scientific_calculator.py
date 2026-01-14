import tkinter as tk
from tkinter import font
import math
import traceback

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Configure colors and styles
        self.root.configure(bg="#1e1e1e")
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.last_was_operator = False  # Track if last input was operator to prevent consecutive operators
        self.is_error = False  # Track if current display is an error
        
        # Setup fonts
        self.display_font = font.Font(family="Courier", size=24, weight="bold")
        self.button_font = font.Font(family="Arial", size=12)
        self.small_button_font = font.Font(family="Arial", size=10)
        
        # Create widgets
        self.create_display()
        self.create_buttons()
        
    def create_display(self):
        """Create the calculator display"""
        display_frame = tk.Frame(self.root, bg="#1e1e1e", pady=10)
        display_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Display text
        display = tk.Entry(
            display_frame,
            textvar=self.display_var,
            font=self.display_font,
            bg="#2d2d2d",
            fg="#00ff00",
            border=2,
            relief=tk.SUNKEN,
            justify=tk.RIGHT,
            state=tk.NORMAL
        )
        display.pack(fill=tk.BOTH, ipady=15)
        
    def create_buttons(self):
        """Create all calculator buttons"""
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Define button layout
        buttons = [
            ["C", "CE", "Back", "÷", "√"],
            ["7", "8", "9", "×", "x²"],
            ["4", "5", "6", "−", "x³"],
            ["1", "2", "3", "+", "1/x"],
            ["0", ".", "=", "π", "e"],
            ["sin", "cos", "tan", "log", "ln"],
            ["asin", "acos", "atan", "log₁₀", "!"],
            ["(", ")", "%", "^", "deg/rad"]
        ]
        
        # Create buttons with grid layout
        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                self.create_button(button_frame, btn_text, row_idx, col_idx)
    
    def create_button(self, parent, text, row, col):
        """Create individual button"""
        # Determine button properties
        if text in ["=", "C", "CE"]:
            bg_color = "#ff6b6b"
            fg_color = "#ffffff"
        elif text in ["÷", "×", "−", "+", "^", "%"]:
            bg_color = "#4ecdc4"
            fg_color = "#ffffff"
        elif text in ["sin", "cos", "tan", "log", "ln", "asin", "acos", "atan", "log₁₀", "!", "√", "x²", "x³", "1/x", "π", "e", "deg/rad"]:
            bg_color = "#95a5a6"
            fg_color = "#ffffff"
        else:
            bg_color = "#34495e"
            fg_color = "#ecf0f1"
        
        button = tk.Button(
            parent,
            text=text,
            font=self.button_font if len(text) <= 3 else self.small_button_font,
            bg=bg_color,
            fg=fg_color,
            activebackground=bg_color,
            activeforeground=fg_color,
            border=0,
            padx=20,
            pady=20,
            command=lambda: self.on_button_press(text)
        )
        button.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
        
        # Configure grid weights for responsive layout
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
    
    def on_button_press(self, text):
        """Handle button press events"""
        current = self.display_var.get()
        
        try:
            if self.is_error and text not in ["C", "CE", "Back"]:
                if text not in ["÷", "×", "−", "+", "^", "%", ")"]:
                    self.display_var.set("0")
                    self.is_error = False
                    current = "0"
            
            if text == "C":
                # Clear all
                self.display_var.set("0")
                self.last_was_operator = False
                self.is_error = False
            elif text == "CE":
                # Clear entry
                self.display_var.set("0")
                self.last_was_operator = False
                self.is_error = False
            elif text == "Back":
                # Delete last character
                if len(current) > 1:
                    self.display_var.set(current[:-1])
                    self.last_was_operator = False
                else:
                    self.display_var.set("0")
                    self.last_was_operator = False
            elif text == "=":
                # Evaluate expression only if not empty or incomplete
                if current == "0" or current == "" or current[-1] in ["+", "-", "*", "/", "^", "%", "("]:
                    self.display_var.set("Error: Incomplete")
                    self.is_error = True
                else:
                    result = self.evaluate(current)
                    self.display_var.set(str(result))
                    self.last_was_operator = False
                    self.is_error = isinstance(result, str) and "Error" in result
            elif text == "√":
                try:
                    num = float(current)
                    if num < 0:
                        self.display_var.set("Error: Negative sqrt")
                        self.is_error = True
                    else:
                        result = math.sqrt(num)
                        self.display_var.set(str(result))
                        self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "x²":
                try:
                    result = float(current) ** 2
                    self.display_var.set(str(result))
                    self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "x³":
                try:
                    result = float(current) ** 3
                    self.display_var.set(str(result))
                    self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "1/x":
                try:
                    num = float(current)
                    if num == 0:
                        self.display_var.set("Error: Div by zero")
                        self.is_error = True
                    else:
                        result = 1 / num
                        self.display_var.set(str(result))
                        self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "π":
                self.display_var.set(str(math.pi))
                self.is_error = False
                self.last_was_operator = False
            elif text == "e":
                self.display_var.set(str(math.e))
                self.is_error = False
                self.last_was_operator = False
            elif text == "sin":
                try:
                    result = math.sin(math.radians(float(current)))
                    self.display_var.set(str(result))
                    self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "cos":
                try:
                    result = math.cos(math.radians(float(current)))
                    self.display_var.set(str(result))
                    self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "tan":
                try:
                    result = math.tan(math.radians(float(current)))
                    self.display_var.set(str(result))
                    self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "asin":
                try:
                    num = float(current)
                    if num < -1 or num > 1:
                        self.display_var.set("Error: Range [-1,1]")
                        self.is_error = True
                    else:
                        result = math.degrees(math.asin(num))
                        self.display_var.set(str(result))
                        self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "acos":
                try:
                    num = float(current)
                    if num < -1 or num > 1:
                        self.display_var.set("Error: Range [-1,1]")
                        self.is_error = True
                    else:
                        result = math.degrees(math.acos(num))
                        self.display_var.set(str(result))
                        self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "atan":
                try:
                    result = math.degrees(math.atan(float(current)))
                    self.display_var.set(str(result))
                    self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "log":
                try:
                    num = float(current)
                    if num <= 0:
                        self.display_var.set("Error: Log domain")
                        self.is_error = True
                    else:
                        result = math.log2(num)
                        self.display_var.set(str(result))
                        self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "log₁₀":
                try:
                    num = float(current)
                    if num <= 0:
                        self.display_var.set("Error: Log domain")
                        self.is_error = True
                    else:
                        result = math.log10(num)
                        self.display_var.set(str(result))
                        self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "ln":
                try:
                    num = float(current)
                    if num <= 0:
                        self.display_var.set("Error: Ln domain")
                        self.is_error = True
                    else:
                        result = math.log(num)
                        self.display_var.set(str(result))
                        self.is_error = False
                except ValueError:
                    self.display_var.set("Error: Invalid input")
                    self.is_error = True
            elif text == "!":
                try:
                    num = float(current)
                    if num < 0:
                        self.display_var.set("Error: Negative !")
                        self.is_error = True
                    elif num != int(num):
                        self.display_var.set("Error: Must be integer")
                        self.is_error = True
                    elif num > 170:  # Prevent factorial overflow for numbers > 170
                        self.display_var.set("Error: Too large")
                        self.is_error = True
                    else:
                        result = math.factorial(int(num))
                        self.display_var.set(str(result))
                        self.is_error = False
                except (ValueError, OverflowError):
                    self.display_var.set("Error: Invalid factorial")
                    self.is_error = True
            elif text == "%":
                if not self.last_was_operator and current != "0":
                    self.display_var.set(current + "%")
                    self.last_was_operator = True
            elif text == "^":
                if not self.last_was_operator and current != "0":
                    self.display_var.set(current + "^")
                    self.last_was_operator = True
            elif text == "(":
                if current == "0":
                    self.display_var.set("(")
                else:
                    self.display_var.set(current + "(")
                self.last_was_operator = False
            elif text == ")":
                self.display_var.set(current + ")")
                self.last_was_operator = False
            elif text == "deg/rad":
                # Toggle mode (for educational purposes)
                self.display_var.set("Mode: deg")
                self.is_error = False
            elif text in ["÷", "×", "−", "+"]:
                if self.last_was_operator or current == "0":
                    if current == "0":
                        self.display_var.set("0" + text)
                else:
                    self.display_var.set(current + text)
                self.last_was_operator = True
            else:
                # Handle numbers and decimal point
                if current == "0" and text != ".":
                    self.display_var.set(text)
                    self.last_was_operator = False
                elif text == "." and "." in current:
                    pass
                else:
                    self.display_var.set(current + text)
                    self.last_was_operator = False
                self.is_error = False
        except Exception as e:
            self.display_var.set("Error")
            self.is_error = True
            print(f"Unexpected error: {e}")
            traceback.print_exc()
    
    def evaluate(self, expression):
        """Safely evaluate mathematical expression"""
        try:
            # Replace custom operators
            expression = expression.replace("÷", "/")
            expression = expression.replace("×", "*")
            expression = expression.replace("−", "-")
            expression = expression.replace("^", "**")
            expression = expression.replace("%", "%")
            
            if not expression or expression in ["+", "-", "*", "/", "//", "**", "(", ")"]:
                return "Error: Incomplete expression"
            
            if expression.count("(") != expression.count(")"):
                return "Error: Mismatched parentheses"
            
            # Only allow safe math functions
            safe_dict = {
                "__builtins__": {},
                "abs": abs,
                "round": round,
                "pow": pow,
            }
            
            result = eval(expression, safe_dict)
            
            # Check for division by zero and invalid operations
            if isinstance(result, float):
                if math.isinf(result):
                    return "Error: Div by zero"
                if math.isnan(result):
                    return "Error: Invalid result"
            
            return round(result, 10)  # Round to 10 decimal places
        except ZeroDivisionError:
            return "Error: Div by zero"
        except SyntaxError:
            return "Error: Invalid syntax"
        except:
            return "Error: Invalid expression"

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()
