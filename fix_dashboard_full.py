
import re
import os

file_path = r"e:\08- ExplorerX Protfolio Projects\django antigrativy\templates\core\dashboard.html"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Fix the JS TemplateSyntaxError (spaces in filters)
    # Remove space after default: and yesno:
    content = re.sub(r'\|\s*default:\s+', '|default:', content)
    content = re.sub(r'\|\s*yesno:\s+', '|yesno:', content)
    
    # 2. Fix the CSS/Style Block corruption
    # We will look for the corrupted patterns and replace them with single-line versions
    
    # Fix --bg-deep
    bg_deep_pattern = r'--bg-deep:\s*{\s*%\s*if\s+global_config\.background_style==\'minimal\'\s*%\s*}\s*#F0F2F5\s*{\s*%\s*elif\s+global_config\.background_style==\'gradient\'\s*%\s*}\s*#0F172A\s*{\s*%\s*else\s*%\s*}\s*#05070A\s*{\s*%\s*endif\s*%\s*}\s*;'
    # The pattern is complex due to newlines/spaces. Let's try a simpler approach if the specific structure is consistent.
    # Actually, replacing the whole style block might be safer if we can identify start/end reliably.
    
    # Let's rebuild the :root block entirely.
    # Identifying the bounds of :root { ... }
    root_start = content.find(':root {')
    root_end = content.find('}', root_start)
    
    if root_start != -1 and root_end != -1:
        new_root = """:root {
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
        
        # Replace the messy root block with the clean one
        # Note: We need to be careful not to replace too much if the find is loose.
        # But looking at previous view_file, the block is quite distinct.
        
        # Taking a chunk approach to avoid regex complexity on large multiline text
        # We rely on the fact that :root is at the start of style.
        
        # Let's assume the previous content lines 27 to 83 (approx) are the target.
        # We can detect the range by looking for specific markers.
        
        pre_root = content[:root_start]
        post_root = content[root_end+1:]
        content = pre_root + new_root + post_root
        print("Fixed CSS root block.")
    else:
        print("Warning: Could not locate :root block.")


    # Write back
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Successfully corrected templates/core/dashboard.html")

except Exception as e:
    print(f"Error: {e}")
