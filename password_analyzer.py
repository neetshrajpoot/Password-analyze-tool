import re
import secrets
import string
import tkinter as tk

COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678", "123456789",
    "qwerty", "qwerty123", "admin", "admin123", "letmein",
    "welcome", "iloveyou", "abc123", "000000", "111111"
}

def analyze_password(password):
    checks = {
        "Length (12+ characters)": len(password) >= 12,
        "Uppercase letter": bool(re.search(r"[A-Z]", password)),
        "Lowercase letter": bool(re.search(r"[a-z]", password)),
        "Number": bool(re.search(r"\d", password)),
        "Special character": bool(re.search(r"[^A-Za-z0-9]", password)),
        "Not a common password": password.lower() not in COMMON_PASSWORDS,
        "No repeated pattern": not bool(re.search(r"(.)\1\1", password)),
    }
    score = (1 if len(password) >= 8 else 0) + (1 if len(password) >= 12 else 0)
    score += (1 if len(password) >= 16 else 0)
    score += sum(checks.values())
    if score >= 8: strength = "VERY STRONG"
    elif score >= 6: strength = "STRONG"
    elif score >= 4: strength = "MEDIUM"
    elif score >= 2: strength = "WEAK"
    else: strength = "VERY WEAK"

    suggestions = []
    if len(password) < 12: suggestions.append("Use at least 12 characters.")
    if not checks["Uppercase letter"]: suggestions.append("Add uppercase letters.")
    if not checks["Lowercase letter"]: suggestions.append("Add lowercase letters.")
    if not checks["Number"]: suggestions.append("Add numbers.")
    if not checks["Special character"]: suggestions.append("Add special characters.")
    if not checks["Not a common password"]: suggestions.append("Avoid common passwords.")
    if not checks["No repeated pattern"]: suggestions.append("Avoid repeated characters such as aaa or 111.")
    return score, strength, checks, suggestions

def generate_password(length=16):
    upper, lower, digits, special = string.ascii_uppercase, string.ascii_lowercase, string.digits, "!@#$%^&*()-_=+"
    chars = [secrets.choice(upper), secrets.choice(lower), secrets.choice(digits), secrets.choice(special)]
    chars += [secrets.choice(upper + lower + digits + special) for _ in range(length - 4)]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

class App:
    def __init__(self, root):
        self.root = root
        root.title("Password Strength Analyzer")
        root.geometry("700x650")
        root.configure(bg="#07111f")

        tk.Label(root, text="Password Strength Analyzer", font=("Arial", 26, "bold"),
                 fg="#42dca7", bg="#07111f").pack(pady=(30, 5))
        tk.Label(root, text="Cybersecurity password analysis tool", fg="#9aaabd",
                 bg="#07111f").pack(pady=(0, 25))

        card = tk.Frame(root, bg="#101b2b", padx=24, pady=22)
        card.pack(fill="x", padx=30)

        tk.Label(card, text="Enter Password", font=("Arial", 12, "bold"),
                 fg="white", bg="#101b2b").pack(anchor="w")
        row = tk.Frame(card, bg="#101b2b")
        row.pack(fill="x", pady=10)

        self.var = tk.StringVar()
        self.entry = tk.Entry(row, textvariable=self.var, show="*", font=("Arial", 14),
                              bg="#08111d", fg="white", insertbackground="white", relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, ipady=10)

        self.show = tk.BooleanVar()
        tk.Checkbutton(row, text="Show", variable=self.show, command=self.toggle,
                       fg="white", bg="#101b2b", selectcolor="#101b2b",
                       activebackground="#101b2b").pack(side="left", padx=10)

        tk.Button(card, text="Analyze", command=self.analyze, bg="#42dca7",
                  fg="#06130e", font=("Arial", 11, "bold"), relief="flat",
                  padx=18, pady=8).pack(side="left")
        tk.Button(card, text="Generate Strong Password", command=self.generate,
                  bg="#1d2b3d", fg="white", font=("Arial", 11, "bold"),
                  relief="flat", padx=18, pady=8).pack(side="left", padx=10)

        result = tk.Frame(root, bg="#101b2b", padx=24, pady=20)
        result.pack(fill="both", expand=True, padx=30, pady=18)

        self.strength = tk.Label(result, text="Enter a password to begin",
                                 font=("Arial", 20, "bold"), fg="#9aaabd", bg="#101b2b")
        self.strength.pack(anchor="w")
        self.score = tk.Label(result, text="Score: -", fg="#9aaabd", bg="#101b2b")
        self.score.pack(anchor="w", pady=(4, 12))

        self.checks = tk.Text(result, height=9, font=("Consolas", 11),
                              bg="#08111d", fg="#dce6ef", relief="flat")
        self.checks.pack(fill="both", expand=True)
        self.checks.config(state="disabled")

        tk.Label(result, text="Security Recommendations", font=("Arial", 13, "bold"),
                 fg="white", bg="#101b2b").pack(anchor="w", pady=(14, 7))
        self.suggestions = tk.Label(result, text="", justify="left", anchor="w",
                                    fg="#aebaca", bg="#101b2b")
        self.suggestions.pack(fill="x")

        self.entry.bind("<KeyRelease>", lambda e: self.analyze())

    def toggle(self):
        self.entry.config(show="" if self.show.get() else "*")

    def analyze(self):
        password = self.var.get()
        if not password:
            self.strength.config(text="Enter a password to begin", fg="#9aaabd")
            self.score.config(text="Score: -")
            self.set_text("")
            self.suggestions.config(text="")
            return
        score, strength, checks, suggestions = analyze_password(password)
        colors = {"VERY STRONG":"#42dca7","STRONG":"#67d391","MEDIUM":"#f0c75e",
                  "WEAK":"#f19a55","VERY WEAK":"#ef6b73"}
        self.strength.config(text=f"Strength: {strength}", fg=colors[strength])
        self.score.config(text=f"Score: {score}/10")
        self.set_text("\n".join(("✓" if ok else "✗") + "  " + name for name, ok in checks.items()))
        self.suggestions.config(text="\n".join("• " + x for x in suggestions) if suggestions
                                else "✓ No basic weaknesses detected.")

    def set_text(self, text):
        self.checks.config(state="normal")
        self.checks.delete("1.0", tk.END)
        self.checks.insert("1.0", text)
        self.checks.config(state="disabled")

    def generate(self):
        self.var.set(generate_password())
        self.show.set(True)
        self.toggle()
        self.analyze()

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
