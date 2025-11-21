import os
import re

# --- CONFIGURATION ---
MAIN_FILE = 'paper.tex'
OUTPUT_FILE = 'paper_flattened.tex'
# ---------------------

def clean_path(path):
    """
    Fixes paths that include the full project structure 
    when we are already inside the folder.
    """
    # Convert backslashes to forward slashes for consistency
    path = path.replace('\\', '/')
    
    # If the path tries to reference the root folders, strip them out
    # This fixes the "Latex/Current Version/Sections" issue
    redundant_prefix = "Latex/Current Version/"
    if redundant_prefix in path: # Case sensitive check
        path = path.replace(redundant_prefix, "")
    
    # Also try case-insensitive check just in case
    elif "latex/current version/" in path.lower():
        # Split by slash and take the last parts (e.g. Sections/1-Intro...)
        parts = path.split('/')
        if 'Sections' in parts:
            index = parts.index('Sections')
            path = "/".join(parts[index:])
            
    return path

def flatten_latex(filename, current_dir):
    content = ""
    
    # Ensure extension
    if not filename.lower().endswith('.tex'):
        filename += '.tex'
    
    # CLEAN THE PATH before looking for it
    clean_filename = clean_path(filename)
    
    # Construct full path
    full_path = os.path.join(current_dir, clean_filename)
    
    # Check if file exists
    if not os.path.exists(full_path):
        print(f"  -> FAIL: Could not find '{clean_filename}'")
        return f"% MISSING FILE: {filename}\n"

    print(f"Processing: {clean_filename}")

    with open(full_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Regex to find \input{...} or \include{...} (ignoring comments)
            match = re.search(r'^\s*(?!%)\\(:?input|include)\{([^}]+)\}', line)
            
            if match:
                included_file = match.group(2)
                content += f"\n% --- START {included_file} ---\n"
                # Recursively process
                content += flatten_latex(included_file, current_dir)
                content += f"\n% --- END {included_file} ---\n"
            else:
                content += line
    return content

# Execution
try:
    cwd = os.getcwd()
    print(f"Working in: {cwd}")
    full_content = flatten_latex(MAIN_FILE, cwd)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_content)
    print(f"\nSUCCESS! Flattened file saved to: {OUTPUT_FILE}")
    
except Exception as e:
    print(f"\nERROR: {e}")