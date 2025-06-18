#!/usr/bin/env python3
"""
Fix docstring quote issues in Python files.
"""

import os
import re

def fix_docstring_quotes(filepath):
    """Fix docstring quote issues in a Python file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 4 quotes at start of file (should be 3)
    content = re.sub(r'^""""', '"""', content, flags=re.MULTILINE)
    
    # Fix 4 quotes at end of docstring (should be 3)
    content = re.sub(r'""""', '"""', content)
    
    # Fix cases where quotes are broken across lines
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Look for lines that start with just quotes
        if re.match(r'^\s*["\']', line.strip()):
            # If previous line ends with content but no quotes, this might be a broken docstring
            if i > 0 and fixed_lines and not re.search(r'["\']$', fixed_lines[-1].strip()):
                # Check if this line is just quotes
                if line.strip() in ['"""', "'''", '"', "'"]:
                    # Append to previous line
                    fixed_lines[-1] = fixed_lines[-1].rstrip() + line.strip()
                    continue
        
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Additional fixes for common patterns
    # Fix broken triple quotes
    content = re.sub(r'"""\s*$\n\s*"""', '"""', content, flags=re.MULTILINE)
    content = re.sub(r"'''\s*$\n\s*'''", "'''", content, flags=re.MULTILINE)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def fix_all_files():
    """Fix all Python files in the src directory."""
    fixed_count = 0
    
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                print(f"Checking {filepath}...")
                if fix_docstring_quotes(filepath):
                    fixed_count += 1
                    print(f"  Fixed {filepath}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    fix_all_files()
