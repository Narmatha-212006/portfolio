import re
import sys

with open('index (1).html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

project_repo_map = {
    'Smart Helpdesk Ticketing Solution for IT Services': 'https://github.com/Narmatha-212006/Smart-Helpdesk-Ticketing-Solution-for-IT-Services',
    'EduNova AI': 'https://github.com/Narmatha-212006/EduNova-AI',
    'SpendDora AI': 'https://github.com/Narmatha-212006/SpendDora-AI',
}

# Find all <h4> tags that match our project titles
for title, url in project_repo_map.items():
    # Find the title
    title_match = re.search(rf'<h4>\s*{re.escape(title)}\s*</h4>', content)
    if title_match:
        start_idx = title_match.end()
        # Find the next project-github link after this title
        link_match = re.search(r'<a[^>]*href="([^"]+)"[^>]*class="project-github"', content[start_idx:])
        if link_match:
            old_url = link_match.group(1)
            full_match = link_match.group(0)
            new_full_match = full_match.replace(f'href="{old_url}"', f'href="{url}"')
            
            # Replace in content
            content = content[:start_idx + link_match.start()] + new_full_match + content[start_idx + link_match.end():]
            print(f"Updated {title!r}:")
            print(f"  Old: {old_url}")
            print(f"  New: {url}")
        else:
            print(f"Could not find link for {title!r}")
    else:
        print(f"Could not find title {title!r}")

with open('index (1).html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nSaved index (1).html")
