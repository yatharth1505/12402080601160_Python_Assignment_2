"""Q1 Email extractor. Run: python 12402080601160_Assignment2_Q1.py emails.txt"""
import re, sys
from collections import defaultdict
from pathlib import Path

EMAIL = re.compile(r"(?<![A-Za-z0-9._+-])[A-Za-z0-9+._-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.(?:com|edu|org)(?![A-Za-z0-9._+-])", re.I)

def main():
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_file():
        raise SystemExit("Usage: python 12402080601160_Assignment2_Q1.py <text_file>")
    unique = set()
    try:
        with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
            for line in f:
                unique.update(m.group().lower() for m in EMAIL.finditer(line))
    except OSError as e:
        raise SystemExit(f"File error: {e}")
    by_domain = defaultdict(set)
    for email in unique:
        by_domain[email.split("@", 1)[1]].add(email)
    for domain in sorted(by_domain):
        print(domain, len(by_domain[domain]), min(by_domain[domain]))

if __name__ == "__main__":
    main()
