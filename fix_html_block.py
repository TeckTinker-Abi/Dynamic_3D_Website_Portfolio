
import os

file_path = r"e:\08- ExplorerX Protfolio Projects\django antigrativy\templates\core\dashboard.html"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the block we want to fix
start_index = -1
for i, line in enumerate(lines):
    if '<!-- Role & Philosophy -->' in line:
        start_index = i
        break

if start_index != -1:
    # We want to replace the next few lines.
    # The current state (based on view_file output):
    # 312: <!-- Role & Philosophy -->
    # 313: <div class="space-y-4 opacity-0 translate-y-10" id="role-line">
    # 314:     <h2 ...>{{
    # 315:         identity_core.profile_title }}</h2>
    # 316:     <p ...>
    
    # Let's just locate the <h2> tag and fix it regardless of newlines
    
    # Find the H2 line.
    h2_index = -1
    for j in range(start_index, start_index + 10):
        if '<h2' in lines[j] and 'font-scifi' in lines[j]:
            h2_index = j
            break
            
    if h2_index != -1:
        # Check if it spans multiple lines
        content = "".join(lines)
        
        # We'll valid replacement string
        new_block = """                <div class="space-y-4 opacity-0 translate-y-10" id="role-line">
                    <h2 class="font-scifi text-xl md:text-2xl text-cyan-400 tracking-widest uppercase">{{ identity_core.profile_title }}</h2>
                    <p class="font-inter text-gray-400 text-lg leading-relaxed max-w-xl mx-auto lg:mx-0 border-l-2 border-purple-500 pl-4">
                        "{{ identity_core.slogan }}"
                    </p>
                </div>"""

        # We need to find the old block to replace.
        # It's tricky with fuzzy matching.
        # Let's rewrite the lines directly if we can identify the range.
        
        # Simpler approach: Read content, use regex to find the H2 block.
        import re
        
        # Pattern to match the H2 tag and its content, potentially across lines.
        # <h2 class="...">{{ \n content \n }}</h2>
        # or similar variants.
        
        # Logic: Find the div#role-line start, find the closing div. Replace everything inside.
        
        div_start_pattern = r'<div class="space-y-4 opacity-0 translate-y-10" id="role-line">'
        div_end_pattern = r'</div>' # Need to be careful not to match wrong div
        
        # Finding the div start
        idx = content.find('<div class="space-y-4 opacity-0 translate-y-10" id="role-line">')
        if idx != -1:
            # Find the closing div. The structure is div > h2, p > div.
            # So looking for the next </div> might be tricky if nested, but here it is flat.
            # However, `p` tag is closed.
            
            # Let's search for the creation of the H2 and repair it.
            # We know the H2 starts after the div.
            
            # Reconstruct the file content by lines is safer here.
            
            new_lines = []
            skip = False
            for i, line in enumerate(lines):
                if '<!-- Role & Philosophy -->' in line:
                    new_lines.append(line)
                    # Add our new block
                    new_lines.append('                <div class="space-y-4 opacity-0 translate-y-10" id="role-line">\n')
                    new_lines.append('                    <h2 class="font-scifi text-xl md:text-2xl text-cyan-400 tracking-widest uppercase">{{ identity_core.profile_title }}</h2>\n')
                    new_lines.append('                    <p class="font-inter text-gray-400 text-lg leading-relaxed max-w-xl mx-auto lg:mx-0 border-l-2 border-purple-500 pl-4">\n')
                    new_lines.append('                        "{{ identity_core.slogan }}"\n')
                    new_lines.append('                    </p>\n')
                    new_lines.append('                </div>\n')
                    
                    # Now skip lines until we pass the old block
                    skip = True
                    continue
                
                if skip:
                    # Heuristic to stop skipping:
                    # The old block ends with </div>.
                    # Or the next section starts: <!-- Explore Cue -->
                    if '<!-- Explore Cue -->' in line:
                        skip = False
                        new_lines.append(line)
                    continue
                
                new_lines.append(line)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print("Successfully rewrote the Role & Philosophy block.")
        else:
            print("Could not find the role-line div to replace.")

else:
    print("Could not find '<!-- Role & Philosophy -->' marker.")
