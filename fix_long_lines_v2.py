#!/usr/bin/env python3
"""Fix E501 line too long issues by intelligently breaking lines"""

import re
from pathlib import Path

def break_long_lines_in_file(file_path):
    """Break long lines intelligently"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.splitlines()
        fixed_lines = []
        changed = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Skip if line is acceptable length
            if len(line) <= 79:
                fixed_lines.append(line)
                i += 1
                continue
            
            original_line = line
            
            # Pattern 1: Function definitions with long parameter lists
            if re.match(r'^(\s*)(async\s+)?def\s+\w+\(.*\):', line):
                indent = re.match(r'^(\s*)', line).group(1)
                if '(' in line and ')' in line:
                    # Extract function signature parts
                    parts = line.split('(', 1)
                    if len(parts) == 2:
                        func_part = parts[0] + '('
                        params_and_closing = parts[1]
                        
                        # Find the closing parenthesis
                        paren_count = 1
                        closing_pos = 0
                        for j, char in enumerate(params_and_closing):
                            if char == '(':
                                paren_count += 1
                            elif char == ')':
                                paren_count -= 1
                                if paren_count == 0:
                                    closing_pos = j
                                    break
                        
                        params = params_and_closing[:closing_pos]
                        closing = params_and_closing[closing_pos:]
                        
                        # Split parameters
                        if ',' in params:
                            param_list = [p.strip() for p in params.split(',')]
                            if len(param_list) > 1:
                                fixed_lines.append(func_part)
                                for param in param_list[:-1]:
                                    fixed_lines.append(f'{indent}    {param},')
                                fixed_lines.append(f'{indent}    {param_list[-1]}')
                                fixed_lines.append(f'{indent}{closing}')
                                changed = True
                                i += 1
                                continue
            
            # Pattern 2: Long import lines
            if line.strip().startswith('from') and 'import' in line:
                match = re.match(r'^(\s*from\s+\S+\s+import\s+)(.+)$', line)
                if match:
                    indent_part, imports_part = match.groups()
                    if ',' in imports_part:
                        imports = [imp.strip() for imp in imports_part.split(',')]
                        if len(imports) > 2:
                            fixed_lines.append(f'{indent_part}(')
                            for imp in imports[:-1]:
                                fixed_lines.append(f'    {imp},')
                            fixed_lines.append(f'    {imports[-1]}')
                            fixed_lines.append(')')
                            changed = True
                            i += 1
                            continue
            
            # Pattern 3: Long string assignments
            if '=' in line and '"' in line:
                match = re.match(r'^(\s*)(\w+\s*=\s*)"([^"]+)"(.*)$', line)
                if match:
                    indent, assignment, string_content, rest = match.groups()
                    if len(string_content) > 50:
                        # Split long strings
                        mid_point = len(string_content) // 2
                        # Find a good break point
                        break_point = mid_point
                        for j in range(max(0, mid_point - 15), min(len(string_content), mid_point + 15)):
                            if j < len(string_content) and string_content[j] == ' ':
                                break_point = j
                                break
                        
                        if break_point != mid_point:
                            part1 = string_content[:break_point].rstrip()
                            part2 = string_content[break_point:].lstrip()
                            
                            fixed_lines.append(f'{indent}{assignment}(')
                            fixed_lines.append(f'{indent}    "{part1} "')
                            fixed_lines.append(f'{indent}    "{part2}"{rest}')
                            fixed_lines.append(f'{indent})')
                            changed = True
                            i += 1
                            continue
            
            # Pattern 4: Long method calls
            if '(' in line and ')' in line and '.' in line:
                # Try to break after commas in method calls
                if ',' in line:
                    match = re.match(r'^(\s*)(.+?)(\([^)]+\))(.*)$', line)
                    if match:
                        indent, prefix, args_part, suffix = match.groups()
                        args_content = args_part[1:-1]  # Remove parentheses
                        if ',' in args_content:
                            args = [arg.strip() for arg in args_content.split(',')]
                            if len(args) > 1:
                                fixed_lines.append(f'{indent}{prefix}(')
                                for arg in args[:-1]:
                                    fixed_lines.append(f'{indent}    {arg},')
                                fixed_lines.append(f'{indent}    {args[-1]}')
                                fixed_lines.append(f'{indent}){suffix}')
                                changed = True
                                i += 1
                                continue
            
            # If no pattern matched, keep original line
            fixed_lines.append(line)
            i += 1
        
        if changed:
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
    src_dir = Path('src')
    files_changed = 0
    
    for py_file in src_dir.rglob('*.py'):
        if break_long_lines_in_file(py_file):
            files_changed += 1
            print(f"Fixed long lines in: {py_file}")
    
    print(f"Fixed long lines in {files_changed} files")

if __name__ == '__main__':
    main()
