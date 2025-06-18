#!/usr/bin/env python3
"""
Fix unterminated string literals in Python files.
"""

import os
import re

def fix_unterminated_strings(filepath):
    """Fix unterminated string literals in a Python file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    fixed_lines = []
    in_triple_quote = False
    triple_quote_type = None
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Handle triple quotes
        if '"""' in line:
            count = line.count('"""')
            if count % 2 == 1:  # Odd number means we're opening or closing
                if not in_triple_quote:
                    in_triple_quote = True
                    triple_quote_type = '"""'
                else:
                    in_triple_quote = False
                    triple_quote_type = None
        elif "'''" in line:
            count = line.count("'''")
            if count % 2 == 1:  # Odd number means we're opening or closing
                if not in_triple_quote:
                    in_triple_quote = True
                    triple_quote_type = "'''"
                else:
                    in_triple_quote = False
                    triple_quote_type = None
        
        # If we're in a triple quote block and this line doesn't close it,
        # and it's the last line of the file or next line doesn't continue the docstring
        if in_triple_quote and i == len(lines) - 1:
            # This is the last line and we're still in a triple quote
            line = line.rstrip() + triple_quote_type
            in_triple_quote = False
        
        # Handle single and double quotes
        if not in_triple_quote:
            # Count unescaped quotes
            single_quotes = 0
            double_quotes = 0
            i_pos = 0
            while i_pos < len(line):
                if line[i_pos] == "'" and (i_pos == 0 or line[i_pos-1] != '\\'):
                    single_quotes += 1
                elif line[i_pos] == '"' and (i_pos == 0 or line[i_pos-1] != '\\'):
                    double_quotes += 1
                i_pos += 1
            
            # If odd number of quotes, try to fix
            if single_quotes % 2 == 1 and not line.rstrip().endswith("'"):
                line = line.rstrip() + "'"
            elif double_quotes % 2 == 1 and not line.rstrip().endswith('"'):
                line = line.rstrip() + '"'
        
        fixed_lines.append(line)
    
    # Write back the fixed content
    fixed_content = '\n'.join(fixed_lines)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    return original_line != line

def fix_all_files():
    """Fix all Python files in the src directory."""
    fixed_count = 0
    
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                print(f"Checking {filepath}...")
                if fix_unterminated_strings(filepath):
                    fixed_count += 1
                    print(f"  Fixed {filepath}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    fix_all_files()
