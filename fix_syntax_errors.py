#!/usr/bin/env python3
"""
Fix syntax errors caused by aggressive line breaking.
This script repairs unterminated string literals and other syntax issues.
"""

import re
from pathlib import Path

def fix_syntax_errors(content: str) -> str:
    """Fix common syntax errors from aggressive line breaking"""
    lines = content.splitlines()
    result_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Fix unterminated string literals
        if (line.count('"') % 2 == 1 and not line.strip().endswith('\\')) or \
           (line.count("'") % 2 == 1 and not line.strip().endswith('\\')):
            
            # Find the unterminated quote
            if '"' in line:
                # Find the last quote and add closing quote
                last_quote = line.rfind('"')
                if last_quote != -1:
                    # Check if this quote starts a string
                    before_quote = line[:last_quote]
                    if before_quote.count('"') % 2 == 0:
                        # This is an opening quote, add closing quote at end of line
                        line = line + '"'
            elif "'" in line:
                last_quote = line.rfind("'")
                if last_quote != -1:
                    before_quote = line[:last_quote]
                    if before_quote.count("'") % 2 == 0:
                        line = line + "'"
        
        # Fix lines that end with backslash but shouldn't
        if line.rstrip().endswith('\\') and not _should_have_backslash(line):
            line = line.rstrip()[:-1].rstrip()
        
        result_lines.append(line)
        i += 1
    
    return '\n'.join(result_lines) + ('\n' if content.endswith('\n') else '')

def _should_have_backslash(line: str) -> bool:
    """Check if a line should legitimately end with backslash"""
    stripped = line.strip()
    # Allow backslash for string continuation, imports, etc.
    return (stripped.startswith('from ') or 
            stripped.startswith('import ') or
            '"' in stripped or
            "'" in stripped)

def fix_indentation_errors(content: str) -> str:
    """Fix basic indentation errors"""
    lines = content.splitlines()
    result_lines = []
    
    for i, line in enumerate(lines):
        # Fix unexpected indents - look for lines that start with extra spaces
        if line.startswith('    ') and i > 0:
            prev_line = lines[i-1].strip()
            if prev_line and not prev_line.endswith(':') and not prev_line.endswith('\\'):
                # This might be an unexpected indent, check if it should be dedented
                if not _needs_indent(prev_line):
                    # Remove extra indentation
                    line = line[4:]
        
        result_lines.append(line)
    
    return '\n'.join(result_lines) + ('\n' if content.endswith('\n') else '')

def _needs_indent(prev_line: str) -> bool:
    """Check if the next line should be indented"""
    keywords_needing_indent = [
        'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except', 'finally:',
        'def ', 'class ', 'with ', 'async def'
    ]
    return any(prev_line.strip().startswith(kw) for kw in keywords_needing_indent)

def fix_trailing_whitespace(content: str) -> str:
    """Remove trailing whitespace"""
    lines = content.splitlines()
    result_lines = [line.rstrip() for line in lines]
    return '\n'.join(result_lines) + ('\n' if content.endswith('\n') else '')

def fix_file_syntax(file_path: Path) -> bool:
    """Fix syntax errors in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Apply fixes in sequence
        content = original_content
        content = fix_syntax_errors(content)
        content = fix_indentation_errors(content)
        content = fix_trailing_whitespace(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix syntax errors in all Python files"""
    src_dir = Path('src')
    if not src_dir.exists():
        print("src/ directory not found")
        return
    
    files_processed = 0
    files_changed = 0
    
    print("🔧 Fixing syntax errors...")
    
    for py_file in src_dir.rglob('*.py'):
        files_processed += 1
        if fix_file_syntax(py_file):
            files_changed += 1
            print(f"🔧 Fixed syntax in: {py_file}")
    
    print(f"\n📊 Summary:")
    print(f"   Files processed: {files_processed}")
    print(f"   Files changed: {files_changed}")
    print(f"🔧 Syntax repair complete!")

if __name__ == '__main__':
    main()
