#!/usr/bin/env python3
"""
Ultra-aggressive line breaker for the final E501 issues.
This script uses more forceful techniques to break remaining long lines.
"""

import re
from pathlib import Path

def force_break_lines(content: str, max_length: int = 79) -> str:
    """Aggressively break lines that are too long"""
    lines = content.splitlines()
    result_lines = []
    
    for line in lines:
        if len(line) <= max_length:
            result_lines.append(line)
            continue
            
        # Get indentation
        indent = line[:len(line) - len(line.lstrip())]
        stripped = line.strip()
        
        # Strategy 1: Break at any comma after position 40
        if ',' in line:
            for i in range(40, len(line)):
                if line[i] == ',' and i < len(line) - 1:
                    part1 = line[:i+1]
                    part2 = line[i+1:].lstrip()
                    if part2:
                        result_lines.append(part1)
                        result_lines.append(f'{indent}    {part2}')
                        break
            else:
                # No suitable comma found, try other strategies
                result_lines.extend(force_break_other_strategies(line, indent, max_length))
        else:
            result_lines.extend(force_break_other_strategies(line, indent, max_length))
    
    return '\n'.join(result_lines) + ('\n' if content.endswith('\n') else '')

def force_break_other_strategies(line: str, indent: str, max_length: int):
    """Use other aggressive strategies to break lines"""
    
    # Strategy 2: Break at operators
    operators = [' = ', ' == ', ' != ', ' and ', ' or ', ' + ', ' - ', ' * ', ' / ']
    for op in operators:
        if op in line:
            for i in range(30, len(line) - len(op)):
                if line[i:i+len(op)] == op:
                    part1 = line[:i+len(op)]
                    part2 = line[i+len(op):].lstrip()
                    if len(part1) <= max_length and part2:
                        return [part1, f'{indent}    {part2}']
    
    # Strategy 3: Break at parentheses
    if '(' in line:
        paren_pos = line.find('(', 30)
        if paren_pos > 0:
            part1 = line[:paren_pos+1]
            part2 = line[paren_pos+1:]
            if len(part1) <= max_length:
                return [part1, f'{indent}    {part2}']
    
    # Strategy 4: Break at dots (method chaining)
    if '.' in line:
        for i in range(40, len(line)):
            if line[i] == '.' and i > 0 and line[i-1] != '.':
                part1 = line[:i]
                part2 = line[i:]
                if len(part1) <= max_length:
                    return [part1, f'{indent}    {part2}']
    
    # Strategy 5: Break at spaces after position 60
    words = line.split()
    if len(words) > 1:
        current_line = indent
        current_length = len(indent)
        broken_lines = []
        
        for word in words:
            if current_length + len(word) + 1 > max_length and current_line.strip():
                broken_lines.append(current_line)
                current_line = f'{indent}    {word}'
                current_length = len(current_line)
            else:
                if current_line.strip():
                    current_line += f' {word}'
                    current_length += len(word) + 1
                else:
                    current_line = f'{indent}{word}'
                    current_length = len(current_line)
        
        if current_line.strip():
            broken_lines.append(current_line)
        
        if len(broken_lines) > 1:
            return broken_lines
    
    # Strategy 6: Force break at character 75 if nothing else works
    if len(line) > max_length:
        part1 = line[:75].rstrip()
        part2 = line[75:].lstrip()
        if part2:
            return [part1 + ' \\', f'{indent}    {part2}']
    
    # Last resort: return original line
    return [line]

def fix_docstrings_and_comments(content: str) -> str:
    """Fix long docstrings and comments"""
    lines = content.splitlines()
    result_lines = []
    
    for line in lines:
        if len(line) <= 79:
            result_lines.append(line)
            continue
            
        stripped = line.strip()
        indent = line[:len(line) - len(line.lstrip())]
        
        # Handle docstrings
        if stripped.startswith('"""') or stripped.startswith("'''"):
            quote_type = '"""' if '"""' in stripped else "'''"
            if stripped.endswith(quote_type) and len(stripped) > 6:
                # Single line docstring
                content_part = stripped[3:-3].strip()
                if len(content_part) > 65:
                    words = content_part.split()
                    current_line = []
                    current_length = 0
                    
                    result_lines.append(f'{indent}{quote_type}')
                    
                    for word in words:
                        if current_length + len(word) + 1 > 70:
                            if current_line:
                                result_lines.append(f'{indent}{" ".join(current_line)}')
                                current_line = [word]
                                current_length = len(word)
                            else:
                                result_lines.append(f'{indent}{word}')
                        else:
                            current_line.append(word)
                            current_length += len(word) + 1
                    
                    if current_line:
                        result_lines.append(f'{indent}{" ".join(current_line)}')
                    
                    result_lines.append(f'{indent}{quote_type}')
                    continue
        
        # Handle comments
        if stripped.startswith('#'):
            comment_text = stripped[1:].strip()
            if len(comment_text) > 70:
                words = comment_text.split()
                current_line = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 > 70:
                        if current_line:
                            result_lines.append(f'{indent}# {" ".join(current_line)}')
                            current_line = [word]
                            current_length = len(word)
                        else:
                            result_lines.append(f'{indent}# {word}')
                    else:
                        current_line.append(word)
                        current_length += len(word) + 1
                
                if current_line:
                    result_lines.append(f'{indent}# {" ".join(current_line)}')
                continue
        
        result_lines.append(line)
    
    return '\n'.join(result_lines) + ('\n' if content.endswith('\n') else '')

def fix_file_aggressive(file_path: Path) -> bool:
    """Aggressively fix E501 issues in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # First pass: aggressive line breaking
        content_after_breaking = force_break_lines(original_content)
        
        # Second pass: fix docstrings and comments
        final_content = fix_docstrings_and_comments(content_after_breaking)
        
        if final_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Aggressively fix remaining E501 issues"""
    src_dir = Path('src')
    if not src_dir.exists():
        print("src/ directory not found")
        return
    
    files_processed = 0
    files_changed = 0
    
    print("💥 Starting ultra-aggressive line breaking...")
    
    for py_file in src_dir.rglob('*.py'):
        files_processed += 1
        if fix_file_aggressive(py_file):
            files_changed += 1
            print(f"🔥 Aggressively fixed: {py_file}")
    
    print(f"\n📊 Summary:")
    print(f"   Files processed: {files_processed}")
    print(f"   Files changed: {files_changed}")
    print(f"💥 Ultra-aggressive line breaking complete!")

if __name__ == '__main__':
    main()
