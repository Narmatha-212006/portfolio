import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index (1).html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Mapping: project card h4 title -> correct repo URL
project_repo_map = {
    'Smart Helpdesk Ticketing Solution for IT Services': 'https://github.com/Narmatha-212006/Smart-Helpdesk-Ticketing-Solution-for-IT-Services',
    'EduNova AI': 'https://github.com/Narmatha-212006/EduNova-AI',
    'SpendDora AI': 'https://github.com/Narmatha-212006/SpendDora-AI',
}

body_start = content.find('<body>')
header = content[:body_start]
body = content[body_start:]

cards = list(re.finditer(r'<div class="project-card"', body))

result_body = body
offset = 0  # track offset as we make replacements

for m in cards:
    start = m.start() + offset
    end = start + 3000
    block = result_body[start:end]

    # Get the title
    h4 = re.search(r'<h4>(.*?)</h4>', block, re.DOTALL)
    if not h4:
        continue
    title = h4.group(1).strip()

    if title not in project_repo_map:
        print(f"  [SKIP] No repo mapping for: {title!r}")
        continue

    correct_url = project_repo_map[title]

    # Find and replace the project-github anchor href within this card block
    # Pattern: href="https://github.com/Narmatha-212006" ... class="project-github"
    new_block, n = re.subn(
        r'(href=")https://github\.com/Narmatha-212006("(?:[^>]*)?class="project-github")',
        rf'\g<1>{correct_url}\2',
        block
    )
    if n == 0:
        # Try alternate attribute order
        new_block, n = re.subn(
            r'(class="project-github"[^>]*href=")https://github\.com/Narmatha-212006(")',
            rf'\g<1>{correct_url}\2',
            block
        )

    result_body = result_body[:start] + new_block + result_body[start+len(block):]
    old_len = len(block)
    new_len = len(new_block)
    offset += new_len - old_len

    print(f"  [FIXED] {title!r} => {correct_url}")
    print(f"          Replacements made: {n}")

final = header + result_body

with open('index (1).html', 'w', encoding='utf-8') as f:
    f.write(final)

print("\nFile saved successfully.")

# Verify
print("\n=== VERIFICATION ===")
with open('index (1).html', 'r', encoding='utf-8', errors='replace') as f:
    verify = f.read()

body_v = verify[verify.find('<body>'):]
cards_v = list(re.finditer(r'<div class="project-card"', body_v))
for i, m in enumerate(cards_v):
    start = m.start()
    block = body_v[start:start+2500]
    h4 = re.search(r'<h4>(.*?)</h4>', block, re.DOTALL)
    btn = re.search(r'class="project-github"[^>]*href="([^"]+)"|href="([^"]+)"[^>]*class="project-github"', block)
    title = h4.group(1).strip() if h4 else 'unknown'
    link = btn.group(1) or btn.group(2) if btn else 'NOT FOUND'
    print(f"  Card {i+1}: {title!r}")
    print(f"    => {link}")
