#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         🔑 PASSWORD STRENGTH ANALYZER v1.0                  ║
║         By: Karthigeyan Ravindranathan (karthik-sec)        ║
║         GitHub: github.com/karthik9810                      ║
║         Purpose: Educational & Ethical Use Only             ║
╚══════════════════════════════════════════════════════════════╝
"""

import re
import string
import getpass

# ── ANSI Colors ───────────────────────────────────────────────
class Color:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    BLUE   = '\033[94m'
    PURPLE = '\033[95m'
    CYAN   = '\033[96m'
    WHITE  = '\033[97m'
    BOLD   = '\033[1m'
    RESET  = '\033[0m'

# ── COMMON WEAK PASSWORDS ─────────────────────────────────────
COMMON_PASSWORDS = [
    "password", "123456", "password123", "admin", "letmein",
    "welcome", "monkey", "dragon", "master", "sunshine",
    "princess", "football", "shadow", "superman", "michael",
    "qwerty", "abc123", "iloveyou", "111111", "1234567",
    "password1", "123123", "12345678", "654321", "pass123",
    "test", "root", "toor", "karthik", "admin123"
]

def banner():
    print(f"""
{Color.PURPLE}{Color.BOLD}
╔══════════════════════════════════════════════════════════════╗
║        🔑  PASSWORD STRENGTH ANALYZER  v1.0  🔑             ║
║        ────────────────────────────────────────             ║
║        🔵 Blue Team  💜 Purple Team  🔴 Red Team            ║
║        By: Karthigeyan Ravindranathan | karthik-sec         ║
╚══════════════════════════════════════════════════════════════╝
{Color.RESET}""")

# ── STRENGTH CHECKS ───────────────────────────────────────────
def analyze_password(password):
    score  = 0
    issues = []
    tips   = []

    # ── Length check ──────────────────────────────────────────
    length = len(password)
    if length == 0:
        return None
    elif length < 6:
        issues.append("Too short (less than 6 characters)")
        tips.append("Use at least 12 characters")
    elif length < 8:
        score += 1
        issues.append("Short (less than 8 characters)")
        tips.append("Use at least 12 characters for better security")
    elif length < 12:
        score += 2
        tips.append("Try using 16+ characters for maximum security")
    elif length < 16:
        score += 3
    else:
        score += 4

    # ── Character type checks ──────────────────────────────────
    has_lower   = bool(re.search(r'[a-z]', password))
    has_upper   = bool(re.search(r'[A-Z]', password))
    has_digit   = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~`]', password))

    if has_lower:
        score += 1
    else:
        issues.append("No lowercase letters")
        tips.append("Add lowercase letters (a-z)")

    if has_upper:
        score += 1
    else:
        issues.append("No uppercase letters")
        tips.append("Add uppercase letters (A-Z)")

    if has_digit:
        score += 1
    else:
        issues.append("No numbers")
        tips.append("Add numbers (0-9)")

    if has_special:
        score += 2
    else:
        issues.append("No special characters")
        tips.append("Add special characters (!@#$%^&*)")

    # ── Common password check ──────────────────────────────────
    if password.lower() in COMMON_PASSWORDS:
        score = 0
        issues.append("⚠️  This is a VERY COMMON password!")
        tips.append("Never use common passwords like 'password123'")

    # ── Repeated characters check ──────────────────────────────
    if re.search(r'(.)\1{2,}', password):
        score -= 1
        issues.append("Has repeated characters (e.g. 'aaa', '111')")
        tips.append("Avoid repeating the same character multiple times")

    # ── Sequential characters check ───────────────────────────
    sequences = ['abcdef', 'qwerty', '123456', '654321', 'abcd', '1234']
    for seq in sequences:
        if seq in password.lower():
            score -= 1
            issues.append(f"Contains sequential pattern '{seq}'")
            tips.append("Avoid keyboard patterns like 'qwerty' or '12345'")
            break

    # ── Clamp score ───────────────────────────────────────────
    score = max(0, min(score, 9))

    return {
        'password'    : password,
        'length'      : length,
        'score'       : score,
        'has_lower'   : has_lower,
        'has_upper'   : has_upper,
        'has_digit'   : has_digit,
        'has_special' : has_special,
        'issues'      : issues,
        'tips'        : tips,
    }

# ── VERDICT ───────────────────────────────────────────────────
def get_verdict(score):
    if score <= 1:
        return Color.RED,    "VERY WEAK   💀", "Extremely easy to crack!"
    elif score <= 3:
        return Color.RED,    "WEAK        ⚠️ ", "Easy to crack!"
    elif score <= 5:
        return Color.YELLOW, "MODERATE    🟡", "Could be stronger"
    elif score <= 7:
        return Color.CYAN,   "STRONG      ✅", "Good password!"
    else:
        return Color.GREEN,  "VERY STRONG 🔥", "Excellent password!"

# ── CRACK TIME ESTIMATE ───────────────────────────────────────
def estimate_crack_time(password):
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'\d', password):    charset += 10
    if re.search(r'[^a-zA-Z0-9]', password): charset += 32

    combinations = charset ** len(password)
    # Assume 10 billion guesses per second (modern GPU)
    guesses_per_sec = 10_000_000_000
    seconds = combinations / guesses_per_sec

    if seconds < 1:
        return Color.RED, "Instantly!"
    elif seconds < 60:
        return Color.RED, f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return Color.RED, f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return Color.YELLOW, f"{seconds/3600:.1f} hours"
    elif seconds < 2592000:
        return Color.YELLOW, f"{seconds/86400:.1f} days"
    elif seconds < 31536000:
        return Color.CYAN, f"{seconds/2592000:.1f} months"
    elif seconds < 3153600000:
        return Color.GREEN, f"{seconds/31536000:.1f} years"
    else:
        return Color.GREEN, "Millions of years! 🔥"

# ── DISPLAY RESULTS ───────────────────────────────────────────
def display_results(result):
    if not result:
        print(f"{Color.RED}No password entered!{Color.RESET}")
        return

    password = result['password']
    score    = result['score']
    s_color, verdict, verdict_msg = get_verdict(score)
    ct_color, crack_time = estimate_crack_time(password)

    print(f"\n{Color.PURPLE}{'═'*62}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}  📊 ANALYSIS RESULTS{Color.RESET}")
    print(f"{Color.PURPLE}{'═'*62}{Color.RESET}")

    # Score bar
    bar_filled = int((score / 9) * 20)
    bar = '█' * bar_filled + '░' * (20 - bar_filled)
    print(f"\n  {Color.WHITE}Strength    : {s_color}[{bar}] {score}/9{Color.RESET}")
    print(f"  {Color.WHITE}Verdict     : {s_color}{verdict}{Color.RESET}")
    print(f"  {Color.WHITE}Summary     : {s_color}{verdict_msg}{Color.RESET}")
    print(f"  {Color.WHITE}Length      : {Color.YELLOW}{result['length']} characters{Color.RESET}")
    print(f"  {Color.WHITE}Crack Time  : {ct_color}{crack_time}{Color.RESET}")

    # Character types
    print(f"\n{Color.PURPLE}{'─'*62}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}  🔍 CHARACTER ANALYSIS{Color.RESET}")
    print(f"{Color.PURPLE}{'─'*62}{Color.RESET}")

    checks = [
        ("Lowercase (a-z)",  result['has_lower']),
        ("Uppercase (A-Z)",  result['has_upper']),
        ("Numbers (0-9)",    result['has_digit']),
        ("Special (!@#$..)", result['has_special']),
    ]
    for label, passed in checks:
        icon  = f"{Color.GREEN}✅" if passed else f"{Color.RED}❌"
        color = Color.GREEN if passed else Color.RED
        print(f"  {icon} {color}{label}{Color.RESET}")

    # Issues
    if result['issues']:
        print(f"\n{Color.PURPLE}{'─'*62}{Color.RESET}")
        print(f"{Color.BOLD}{Color.RED}  ⚠️  ISSUES FOUND{Color.RESET}")
        print(f"{Color.PURPLE}{'─'*62}{Color.RESET}")
        for issue in result['issues']:
            print(f"  {Color.RED}→ {issue}{Color.RESET}")

    # Tips
    if result['tips']:
        print(f"\n{Color.PURPLE}{'─'*62}{Color.RESET}")
        print(f"{Color.BOLD}{Color.YELLOW}  💡 TIPS TO IMPROVE{Color.RESET}")
        print(f"{Color.PURPLE}{'─'*62}{Color.RESET}")
        for tip in result['tips']:
            print(f"  {Color.YELLOW}→ {tip}{Color.RESET}")

    print(f"\n{Color.PURPLE}{'═'*62}{Color.RESET}\n")

# ── SUGGEST STRONG PASSWORD ───────────────────────────────────
def suggest_password():
    import random
    chars = (
        string.ascii_lowercase +
        string.ascii_uppercase +
        string.digits +
        "!@#$%^&*"
    )
    while True:
        pwd = ''.join(random.choices(chars, k=16))
        result = analyze_password(pwd)
        if result and result['score'] >= 8:
            return pwd

# ── MAIN ──────────────────────────────────────────────────────
def main():
    banner()

    while True:
        print(f"{Color.CYAN}Options:{Color.RESET}")
        print(f"  {Color.WHITE}[1] Analyze a password")
        print(f"  {Color.WHITE}[2] Generate a strong password")
        print(f"  {Color.WHITE}[3] Exit")
        print()

        choice = input(f"{Color.PURPLE}Enter choice (1/2/3): {Color.RESET}").strip()

        if choice == '1':
            print()
            try:
                password = getpass.getpass(
                    f"{Color.YELLOW}Enter password (hidden): {Color.RESET}"
                )
            except Exception:
                password = input(f"{Color.YELLOW}Enter password: {Color.RESET}")

            result = analyze_password(password)
            display_results(result)

        elif choice == '2':
            print(f"\n{Color.CYAN}Generating strong password...{Color.RESET}")
            pwd = suggest_password()
            print(f"\n  {Color.GREEN}✅ Suggested Password: {Color.BOLD}{Color.WHITE}{pwd}{Color.RESET}")
            print(f"  {Color.YELLOW}💡 Save this in a password manager!{Color.RESET}\n")

        elif choice == '3':
            print(f"\n{Color.PURPLE}Stay secure buddy! 💜 — karthik-sec{Color.RESET}\n")
            break
        else:
            print(f"{Color.RED}Invalid choice! Try again.{Color.RESET}\n")

if __name__ == '__main__':
    main()
