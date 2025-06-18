#!/usr/bin/env python3
"""
Final fix script for pricing_agent.py.
This script addresses indentation issues in the PricingAgent class with special focus on
if/elif/else blocks, try/except blocks, and method bodies.
"""

import re
import sys

def fix_pricing_agent(file_path):
    """Fix indentation and syntax issues in pricing_agent.py."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # First, fix dataclass indentation
    content = fix_dataclass_indentation(content)
    
    # Fix method indentation
    content = fix_method_indentation(content)
    
    # Fix try/except blocks
    content = fix_try_except_blocks(content)
    
    # Fix if/elif/else blocks
    content = fix_if_blocks(content)
    
    # Write the fixed content back to the file
    with open(file_path, 'w') as f:
        f.write(content)

def fix_dataclass_indentation(content):
    """Fix indentation for dataclass definitions."""
    # Pattern to match @dataclass followed by class definition
    pattern = r'(@dataclass)\s*\n(\s*)class\s+(\w+):'
    
    # Replace with properly indented version
    content = re.sub(pattern, r'\1\nclass \3:', content)
    
    return content

def fix_method_indentation(content):
    """Fix indentation in class methods."""
    lines = content.split('\n')
    fixed_lines = []
    
    in_class = False
    in_method = False
    method_indent = 4
    class_name = None
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Check for class definition
        class_match = re.match(r'class\s+(\w+).*:', stripped)
        if class_match:
            in_class = True
            class_name = class_match.group(1)
            fixed_lines.append(line)
            continue
        
        # Check for method definition
        method_match = re.match(r'(async\s+)?def\s+(\w+)\s*\(', stripped)
        if in_class and method_match:
            in_method = True
            method_name = method_match.group(2)
            fixed_lines.append(' ' * method_indent + stripped)
            continue
        
        # Inside method
        if in_method:
            # Check if we're out of method - empty line followed by non-indented line or another method
            if not stripped:
                fixed_lines.append('')
                # Check if next line indicates end of method
                if i+1 < len(lines):
                    next_line = lines[i+1].strip()
                    next_method = re.match(r'(async\s+)?def\s+(\w+)\s*\(', next_line)
                    if next_method or not lines[i+1].startswith(' '):
                        in_method = False
                continue
            
            # Inside method body, indent by 8 if not already indented
            if not line.startswith(' ' * 8):
                fixed_lines.append(' ' * 8 + stripped)
            else:
                fixed_lines.append(line)
            continue
        
        # Class level but not in method
        if in_class and not in_method:
            if stripped and not line.startswith(' ' * 4):
                fixed_lines.append(' ' * 4 + stripped)
            else:
                fixed_lines.append(line)
            continue
        
        # Outside class
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_try_except_blocks(content):
    """Fix indentation in try/except blocks."""
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Check for try block
        if stripped == 'try:':
            # Get current indentation
            indent_match = re.match(r'^(\s*)', line)
            current_indent = len(indent_match.group(1)) if indent_match else 0
            next_indent = current_indent + 4
            
            # Add the try line
            fixed_lines.append(line)
            i += 1
            
            # Process lines inside try block until we hit except or end of file
            while i < len(lines) and not lines[i].strip().startswith('except '):
                if lines[i].strip():
                    # Ensure proper indentation for try block content
                    fixed_lines.append(' ' * next_indent + lines[i].strip())
                else:
                    fixed_lines.append('')
                i += 1
            
            # Process except blocks
            while i < len(lines) and (lines[i].strip().startswith('except ') or lines[i].strip() == 'except:'):
                except_line = ' ' * current_indent + lines[i].strip()
                fixed_lines.append(except_line)
                i += 1
                
                # Process lines inside except block until we hit another except or else or end of block
                while i < len(lines) and not (lines[i].strip().startswith('except ') or lines[i].strip() == 'else:'):
                    if lines[i].strip():
                        # Ensure proper indentation for except block content
                        fixed_lines.append(' ' * next_indent + lines[i].strip())
                    else:
                        fixed_lines.append('')
                        # Check if next line might be end of block
                        if i+1 < len(lines) and not lines[i+1].strip().startswith(' '):
                            break
                    i += 1
            
            # Check for else block after except
            if i < len(lines) and lines[i].strip() == 'else:':
                else_line = ' ' * current_indent + 'else:'
                fixed_lines.append(else_line)
                i += 1
                
                # Process lines inside else block
                while i < len(lines) and lines[i].strip():
                    fixed_lines.append(' ' * next_indent + lines[i].strip())
                    i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    return '\n'.join(fixed_lines)

def fix_if_blocks(content):
    """Fix indentation in if/elif/else blocks."""
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Check for if statement
        if_match = re.match(r'^(\s*)if\s+.+:', stripped)
        if if_match:
            # Get current indentation
            indent_match = re.match(r'^(\s*)', line)
            current_indent = len(indent_match.group(1)) if indent_match else 0
            next_indent = current_indent + 4
            
            # Add the if line
            fixed_lines.append(line)
            i += 1
            
            # Process lines inside if block until we hit elif, else or end of block
            while (i < len(lines) and 
                   not (lines[i].strip().startswith('elif ') or 
                        lines[i].strip() == 'else:')):
                if lines[i].strip():
                    # Ensure proper indentation for if block content
                    fixed_lines.append(' ' * next_indent + lines[i].strip())
                else:
                    fixed_lines.append('')
                    # Check if next line might be end of block
                    if i+1 < len(lines) and not (lines[i+1].strip().startswith(' ') or 
                                               lines[i+1].strip().startswith('elif ') or 
                                               lines[i+1].strip() == 'else:'):
                        break
                i += 1
            
            # Process elif blocks
            while i < len(lines) and lines[i].strip().startswith('elif '):
                elif_line = ' ' * current_indent + lines[i].strip()
                fixed_lines.append(elif_line)
                i += 1
                
                # Process lines inside elif block
                while (i < len(lines) and 
                       not (lines[i].strip().startswith('elif ') or 
                            lines[i].strip() == 'else:')):
                    if lines[i].strip():
                        # Ensure proper indentation for elif block content
                        fixed_lines.append(' ' * next_indent + lines[i].strip())
                    else:
                        fixed_lines.append('')
                        # Check if next line might be end of block
                        if i+1 < len(lines) and not (lines[i+1].strip().startswith(' ') or 
                                                   lines[i+1].strip().startswith('elif ') or 
                                                   lines[i+1].strip() == 'else:'):
                            break
                    i += 1
            
            # Check for else block
            if i < len(lines) and lines[i].strip() == 'else:':
                else_line = ' ' * current_indent + 'else:'
                fixed_lines.append(else_line)
                i += 1
                
                # Process lines inside else block
                while i < len(lines):
                    if lines[i].strip():
                        next_indent_check = False
                        # Check if we've exited the block
                        if i+1 < len(lines):
                            next_line = lines[i+1].strip()
                            if (next_line.startswith('def ') or 
                                next_line.startswith('class ') or 
                                next_line.startswith('async def ')):
                                next_indent_check = True
                        
                        if next_indent_check:
                            fixed_lines.append(lines[i])
                            break
                        
                        # Ensure proper indentation for else block content
                        fixed_lines.append(' ' * next_indent + lines[i].strip())
                    else:
                        fixed_lines.append('')
                        # Check if next line might be end of block
                        if i+1 < len(lines) and not lines[i+1].strip().startswith(' '):
                            break
                    i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    return '\n'.join(fixed_lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python final_fix.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    fix_pricing_agent(file_path)
    print(f"Fixed pricing agent indentation and syntax in {file_path}")
