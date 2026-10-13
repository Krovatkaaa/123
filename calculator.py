"""Desktop calculator with a compact Tkinter interface."""

from __future__ import annotations

import math
import tkinter as tk


def calculate(left: float, operator: str, right: float) -> float:
    """Apply a supported arithmetic operator to two numbers."""
    operations = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }
    if operator not in operations:
        raise ValueError("Поддерживаются только операции +, -, * и /.")
    if operator == "/" and right == 0:
        raise ZeroDivisionError("На ноль делить нельзя")
    return operations[operator](left, right)


def format_number(value: float) -> str:
    """Return a readable, compact representation of a result."""
    if not math.isfinite(value):
        raise ValueError("Результат слишком большой")
    if value == 0:
        return "0"
    if value.is_integer() and abs(value) < 1e15:
        return str(int(value))
    return f"{value:.12g}"


class CalculatorApp:
    BG = "#111318"
    PANEL = "#1A1D24"
    NUMBER = "#252A33"
    NUMBER_HOVER = "#303641"
    UTILITY = "#343945"
    UTILITY_HOVER = "#414754"
    ACCENT = "#6C63FF"
    ACCENT_HOVER = "#7D75FF"
    EQUALS = "#00BFA6"
    EQUALS_HOVER = "#15D4BA"
    TEXT = "#F5F7FA"
    MUTED = "#8E96A3"
    ERROR = "#FF6B6B"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.display_value = "0"
        self.stored_value: float | None = None
        self.pending_operator: str | None = None
        self.replace_display = False
        self.error_active = False
        self.display_var = tk.StringVar(value="0")
        self.history_var = tk.StringVar(value="Готов к вычислениям")
        self._configure_window()
        self._build_ui()
        self._bind_keyboard()

    def _configure_window(self) -> None:
        self.root.title("Калькулятор")
        self.root.minsize(330, 520)
        self.root.configure(bg=self.BG)
        self.root.option_add("*Font", ("Segoe UI", 12))
        width, height = 380, 590
        x = max(0, (self.root.winfo_screenwidth() - width) // 2)
        y = max(0, (self.root.winfo_screenheight() - height) // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self) -> None:
        shell = tk.Frame(self.root, bg=self.BG, padx=18, pady=18)
        shell.pack(fill="both", expand=True)

        display = tk.Frame(shell, bg=self.PANEL, padx=18, pady=16)
        display.pack(fill="x", pady=(0, 14))
        tk.Label(
            display, textvariable=self.history_var, bg=self.PANEL, fg=self.MUTED,
            anchor="e", font=("Segoe UI", 11),
        ).pack(fill="x")
        self.result_label = tk.Label(
            display, textvariable=self.display_var, bg=self.PANEL, fg=self.TEXT,
            anchor="e", font=("Segoe UI Semibold", 34), pady=4,
        )
        self.result_label.pack(fill="x")

        keypad = tk.Frame(shell, bg=self.BG)
        keypad.pack(fill="both", expand=True)
        for row in range(5):
            keypad.grid_rowconfigure(row, weight=1, uniform="row")
        for column in range(4):
            keypad.grid_columnconfigure(column, weight=1, uniform="column")

        buttons = [
            ("C", self.clear, 0, 0, "utility"),
            ("±", self.toggle_sign, 0, 1, "utility"),
            ("%", self.percent, 0, 2, "utility"),
            ("÷", lambda: self.choose_operator("/"), 0, 3, "operator"),
            ("7", lambda: self.input_digit("7"), 1, 0, "number"),
            ("8", lambda: self.input_digit("8"), 1, 1, "number"),
            ("9", lambda: self.input_digit("9"), 1, 2, "number"),
            ("×", lambda: self.choose_operator("*"), 1, 3, "operator"),
            ("4", lambda: self.input_digit("4"), 2, 0, "number"),
            ("5", lambda: self.input_digit("5"), 2, 1, "number"),
            ("6", lambda: self.input_digit("6"), 2, 2, "number"),
            ("−", lambda: self.choose_operator("-"), 2, 3, "operator"),
            ("1", lambda: self.input_digit("1"), 3, 0, "number"),
            ("2", lambda: self.input_digit("2"), 3, 1, "number"),
            ("3", lambda: self.input_digit("3"), 3, 2, "number"),
            ("+", lambda: self.choose_operator("+"), 3, 3, "operator"),
            ("⌫", self.backspace, 4, 0, "number"),
            ("0", lambda: self.input_digit("0"), 4, 1, "number"),
            (",", self.input_decimal, 4, 2, "number"),
            ("=", self.equals, 4, 3, "equals"),
        ]
        palettes = {
            "number": (self.NUMBER, self.NUMBER_HOVER),
            "utility": (self.UTILITY, self.UTILITY_HOVER),
            "operator": (self.ACCENT, self.ACCENT_HOVER),
            "equals": (self.EQUALS, self.EQUALS_HOVER),
        }
        for text, command, row, column, kind in buttons:
            color, hover = palettes[kind]
            button = tk.Button(
                keypad, text=text, command=command, bg=color, fg=self.TEXT,
                activebackground=hover, activeforeground=self.TEXT, relief="flat",
                bd=0, cursor="hand2", font=("Segoe UI Semibold", 16), takefocus=False,
            )
            button.grid(row=row, column=column, sticky="nsew", padx=4, pady=4)
            button.bind("<Enter>", lambda _event, b=button, c=hover: b.configure(bg=c))
            button.bind("<Leave>", lambda _event, b=button, c=color: b.configure(bg=c))

        tk.Label(
            shell, text="Клавиатура поддерживается", bg=self.BG, fg=self.MUTED,
            font=("Segoe UI", 9), pady=5,
        ).pack(fill="x")

    def _bind_keyboard(self) -> None:
        self.root.bind("<Key>", self._on_key)

    def _on_key(self, event: tk.Event) -> None:
        if event.char.isdigit():
            self.input_digit(event.char)
        elif event.char in ".,":
            self.input_decimal()
        elif event.char in "+-*/":
            self.choose_operator(event.char)
        elif event.char == "%":
            self.percent()
        elif event.keysym in {"Return", "KP_Enter"}:
            self.equals()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym in {"Escape", "Delete"}:
            self.clear()

    def _set_display(self, value: str) -> None:
        self.display_value = value
        self.display_var.set(value.replace(".", ","))
        self.result_label.configure(fg=self.TEXT)
        self.error_active = False

    def _current_number(self) -> float:
        return float(self.display_value)

    def input_digit(self, digit: str) -> None:
        if self.error_active or self.replace_display:
            self._set_display(digit)
            self.replace_display = False
        elif self.display_value == "0":
            self._set_display(digit)
        elif len(self.display_value.replace("-", "").replace(".", "")) < 14:
            self._set_display(self.display_value + digit)

    def input_decimal(self) -> None:
        if self.error_active or self.replace_display:
            self._set_display("0.")
            self.replace_display = False
        elif "." not in self.display_value:
            self._set_display(self.display_value + ".")

    def choose_operator(self, operator: str) -> None:
        if self.error_active:
            self.clear()
            return
        if self.pending_operator and not self.replace_display:
            self._perform_calculation()
            if self.error_active:
                return
        self.stored_value = self._current_number()
        self.pending_operator = operator
        self.replace_display = True
        self.history_var.set(f"{format_number(self.stored_value)} {self._symbol(operator)}")

    def equals(self) -> None:
        if self.pending_operator is None or self.stored_value is None or self.error_active:
            return
        right = self._current_number()
        history = (
            f"{format_number(self.stored_value)} "
            f"{self._symbol(self.pending_operator)} {format_number(right)} ="
        )
        self._perform_calculation()
        if not self.error_active:
            self.history_var.set(history)
            self.stored_value = None
            self.pending_operator = None
            self.replace_display = True

    def _perform_calculation(self) -> None:
        if self.stored_value is None or self.pending_operator is None:
            return
        try:
            result = calculate(self.stored_value, self.pending_operator, self._current_number())
            self._set_display(format_number(result))
        except (ZeroDivisionError, ValueError) as error:
            self.show_error(str(error))

    def toggle_sign(self) -> None:
        if self.error_active or self.display_value == "0":
            return
        value = self.display_value[1:] if self.display_value.startswith("-") else "-" + self.display_value
        self._set_display(value)

    def percent(self) -> None:
        if not self.error_active:
            self._set_display(format_number(self._current_number() / 100))
            self.replace_display = True

    def backspace(self) -> None:
        if self.error_active:
            self.clear()
        elif not self.replace_display:
            shortened = self.display_value[:-1]
            self._set_display(shortened if shortened not in {"", "-"} else "0")

    def clear(self) -> None:
        self.stored_value = None
        self.pending_operator = None
        self.replace_display = False
        self.history_var.set("Готов к вычислениям")
        self._set_display("0")

    def show_error(self, message: str) -> None:
        self.display_value = "0"
        self.display_var.set(message)
        self.result_label.configure(fg=self.ERROR)
        self.history_var.set("Нажмите C или начните новый ввод")
        self.error_active = True
        self.stored_value = None
        self.pending_operator = None
        self.replace_display = True

    @staticmethod
    def _symbol(operator: str) -> str:
        return {"*": "×", "/": "÷", "-": "−"}.get(operator, operator)


def main() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
