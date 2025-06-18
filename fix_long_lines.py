#!/usr/bin/env python3
"""
Script to automatically fix some long line issues (E501)
by breaking common patterns like long string literals and function calls.
"""

import re
from pathlib import Path

def fix_long_lines_in_file(file_path):
    """Fix some common long line patterns in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.splitlines()
        fixed_lines = []
        changed = False
        
        for line in lines:
            original_line = line
            
            # Skip if line is not too long
            if len(line) <= 79:
                fixed_lines.append(line)
                continue
            
            # Pattern 1: Long string assignments
            # Example: some_var = "very long string here"
            string_pattern = r'^(\s*)(\w+\s*=\s*)"([^"]{60,})"(.*)$'
            match = re.match(string_pattern, line)
            if match:
                indent, assignment, string_content, rest = match.groups()
                if len(string_content) > 60 and '"' not in string_content:
                    # Split the string
                    mid_point = len(string_content) // 2
                    # Find a good break point (space)
                    break_point = mid_point
                    for i in range(mid_point - 10, mid_point + 10):
                        if i < len(string_content) and string_content[i] == ' ':
                            break_point = i
                            break
                    
                    part1 = string_content[:break_point].rstrip()
                    part2 = string_content[break_point:].lstrip()
                    
                    if part1 and part2:
                        fixed_lines.append(f'{indent}{assignment}(')
                        fixed_lines.append(f'{indent}    "{part1} "')
                        fixed_lines.append(f'{indent}    "{part2}"{rest}')
                        fixed_lines.append(f'{indent})')
                        changed = True
                        continue
            
            # Pattern 2: Long function calls with multiple arguments
            # Example: function_call(arg1, arg2, arg3, very_long_arg4)
            func_pattern = r'^(\s*)(\w+\([^)]+),\s*([^)]+\))(.*)$'
            match = re.match(func_pattern, line)
            if match and len(line) > 90:
                indent, func_start, last_args, rest = match.groups()
                # Split into multiple lines
                fixed_lines.append(f'{indent}{func_start},')
                fixed_lines.append(f'{indent}    {last_args}{rest}')
                changed = True
                continue
            
            # Pattern 3: Long if conditions
            # Example: if very_long_condition and another_long_condition:
            if_pattern = r'^(\s*)(if\s+.+\s+and\s+.+):(.*)$'
            match = re.match(if_pattern, line)
            if match and len(line) > 90:
                indent, condition, rest = match.groups()
                # Try to split on 'and'
                parts = condition.split(' and ')
                if len(parts) == 2:
                    fixed_lines.append(f'{indent}({parts[0]} and')
                    fixed_lines.append(f'{indent} {parts[1]}){rest}')
                    changed = True
                    continue
            
            # If no pattern matched, keep the original line
            fixed_lines.append(line)
        
        if changed:
            # Join lines back
            new_content = '\n'.join(fixed_lines)
            if content.endswith('\n'):
                new_content += '\n'
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix long lines in all Python files in src/"""
    src_dir = Path('src')
    if not src_dir.exists():
        print("src/ directory not found")
        return
    
    files_processed = 0
    files_changed = 0
    
    # Find all Python files
    for py_file in src_dir.rglob('*.py'):
        files_processed += 1
        if fix_long_lines_in_file(py_file):
            files_changed += 1
            print(f"Fixed long lines in: {py_file}")
    
    print(f"\nProcessed {files_processed} files")
    print(f"Changed {files_changed} files")

if __name__ == '__main__':
    main()
