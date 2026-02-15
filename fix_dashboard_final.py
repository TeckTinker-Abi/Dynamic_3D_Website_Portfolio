
import re
import os

file_path = r"e:\08- ExplorerX Protfolio Projects\django antigrativy\templates\core\dashboard.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix JS Template Syntax (Critical)
# Using regex for robustness against variable spacing
content = re.sub(r'\|\s*default:\s+([\d\.]+)', r'|default:\1', content)
content = re.sub(r'\|\s*yesno:\s+"true,false"', r'|yesno:"true,false"', content)

# 2. Fix CSS Corruption
# Define the clean :root block
clean_root = """:root {
            /* Dynamic Background Logic */
            --bg-deep: {% if global_config.background_style == 'minimal' %}#F0F2F5{% elif global_config.background_style == 'gradient' %}#0F172A{% else %}#05070A{% endif %};
            
            --bg-panel: #0B0F1A;
            --cyan-core: {{ global_config.primary_color|default:"#00F5FF" }};
            --purple-core: {{ global_config.accent_color|default:"#7B61FF" }};
            
            /* Text Color Adaptation */
            --text-main: {% if global_config.background_style == 'minimal' %}#1A202C{% else %}#E6F1FF{% endif %};
            
            --text-dim: #8892B0;
            --glass-border: rgba(255, 255, 255, 0.08);
        }"""

# Regex to find the corrupted :root block up to the start of body match
# Matches :root { ... } (non-greedy) until body {
pattern = r':root\s*\{[\s\S]*?\}\s*body\s*\{'

# Check if we find the pattern
match = re.search(pattern, content)
if match:
    print("Found corrupted CSS block. Replacing...")
    # Replace with clean root block followed by body start
    replacement = clean_root + "\n\n        body {"
    content = re.sub(pattern, replacement, content, count=1)
else:
    print("Warning: CSS :root block pattern not found (might already be fixed or structure differs).")

# Extra check for the specific JS strings if regex missed
if "default: 1.0" in content:
    content = content.replace("default: 1.0", "default:1.0")
    print("Fixed default: 1.0 explicitly.")

if 'yesno: "true,false"' in content:
    content = content.replace('yesno: "true,false"', 'yesno:"true,false"')
    print("Fixed yesno explicitly.")

# Write back
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done.")
