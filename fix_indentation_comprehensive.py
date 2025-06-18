#!/usr/bin/env python3
"""
Comprehensive indentation fixer for pricing_agent.py.
This script fixes indentation issues in the PricingAgent class implementation.
"""

import re
import sys

def fix_indentation(file_path):
    """Fix indentation issues in the given Python file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split the file into lines
    lines = content.split('\n')
    fixed_lines = []
    
    # Track indentation state
    in_class = False
    in_method = False
    in_try_block = False
    in_if_block = False
    current_indent = 0
    next_indent = 0
    method_indent = 0
    
    # Process each line
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        
        # Skip empty lines
        if not stripped_line:
            fixed_lines.append(line)
            continue
        
        # Track class definition
        if re.match(r'class\s+\w+.*:', stripped_line):
            in_class = True
            current_indent = 0
            next_indent = 4
            fixed_lines.append(line)
            continue
            
        # Track method definition
        if in_class and re.match(r'(async\s+)?def\s+\w+\s*\(', stripped_line):
            in_method = True
            method_indent = 4
            current_indent = 4
            next_indent = 8
            # Ensure method has proper indentation
            fixed_line = ' ' * method_indent + stripped_line
            fixed_lines.append(fixed_line)
            continue
            
        # Handle method body
        if in_method:
            # End of method - blank line after method body
            if not stripped_line and i < len(lines) - 1 and lines[i+1].strip() and not lines[i+1].strip().startswith(' '):
                in_method = False
                in_try_block = False
                in_if_block = False
                fixed_lines.append(line)
                continue
                
            # Track try blocks
            if stripped_line == 'try:':
                in_try_block = True
                current_indent = next_indent
                next_indent = current_indent + 4
                fixed_line = ' ' * current_indent + stripped_line
                fixed_lines.append(fixed_line)
                continue
                
            # Track except blocks
            if stripped_line.startswith('except ') or stripped_line == 'except:':
                if in_try_block:
                    fixed_line = ' ' * (next_indent - 4) + stripped_line
                    fixed_lines.append(fixed_line)
                    continue
                    
            # Track else blocks after except
            if stripped_line == 'else:' and in_try_block:
                fixed_line = ' ' * (next_indent - 4) + stripped_line
                fixed_lines.append(fixed_line)
                continue
                
            # Track if/elif/else blocks
            if stripped_line.startswith('if ') and stripped_line.endswith(':'):
                in_if_block = True
                current_indent = next_indent
                next_indent = current_indent + 4
                fixed_line = ' ' * current_indent + stripped_line
                fixed_lines.append(fixed_line)
                continue
                
            if stripped_line.startswith('elif ') and in_if_block:
                fixed_line = ' ' * (next_indent - 4) + stripped_line
                fixed_lines.append(fixed_line)
                continue
                
            if stripped_line == 'else:' and in_if_block:
                fixed_line = ' ' * (next_indent - 4) + stripped_line
                fixed_lines.append(fixed_line)
                continue
                
            # Regular line inside method body
            if in_try_block or in_if_block:
                fixed_line = ' ' * next_indent + stripped_line
            else:
                fixed_line = ' ' * 8 + stripped_line
                
            fixed_lines.append(fixed_line)
            continue
            
        # Outside method but inside class
        if in_class and not in_method:
            # Track class-level indentation
            fixed_line = ' ' * 4 + stripped_line
            fixed_lines.append(fixed_line)
            continue
            
        # Outside class
        fixed_lines.append(line)
    
    # Write the fixed content back to the file
    with open(file_path, 'w') as f:
        f.write('\n'.join(fixed_lines))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_indentation_comprehensive.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    fix_indentation(file_path)
    print(f"Fixed indentation in {file_path}")
