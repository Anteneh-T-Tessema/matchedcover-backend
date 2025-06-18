#!/usr/bin/env python3
"""Fix E251 spacing issues around parameter equals"""

import re
from pathlib import Path

def fix_spacing_in_file(file_path):
    """Fix spacing around equals in function parameters"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix pattern: parameter = Depends -> parameter=Depends
        # But only in function parameter context
        lines = content.splitlines()
        fixed_lines = []
        
        for line in lines:
            # Look for pattern like "parameter = Depends(" or "parameter = default"
            # in function parameter lines (usually indented)
            if re.search(r'^\s+\w+\s+=\s+', line):
                # Replace spaces around = in parameter assignments
                line = re.sub(r'(\w+)\s+=\s+', r'\1=', line)
            fixed_lines.append(line)
        
        new_content = '\n'.join(fixed_lines)
        if content.endswith('\n'):
            new_content += '\n'
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    src_dir = Path('src')
    files_changed = 0
    
    for py_file in src_dir.rglob('*.py'):
        if fix_spacing_in_file(py_file):
            files_changed += 1
            print(f"Fixed spacing in: {py_file}")
    
    print(f"Fixed spacing in {files_changed} files")

if __name__ == '__main__':
    main()
