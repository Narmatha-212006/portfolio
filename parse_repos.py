import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index (1).html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find all project-github anchors and their exact text
print("=== EXACT project-github anchor tags ===")
for m in re.finditer(r'<a [^>]*class="project-github"[^>]*>', content):
    print(repr(m.group(0)[:200]))
    print(f"  at pos {m.start()}")
    print()
