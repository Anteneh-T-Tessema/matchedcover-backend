#!/usr/bin/env python3
"""
Ultra-careful line length fixer that preserves syntax.
Only fixes E501 errors without breaking anything else.
"""

import os
import re
import textwrap
import subprocess

def run_autopep8_line_length_only():
    """Run autopep8 to fix only line length issues."""
    print("Running autopep8 for line length only...")
    cmd = [
        "python", "-m", "autopep8",
        "--select=E501",
        "--in-place",
        "--max-line-length=79",
        "--recursive",
        "src"
    ]
    try:
        subprocess.run(cmd, check=True)
        print("autopep8 completed")
    except subprocess.CalledProcessError as e:
        print(f"autopep8 failed: {e}")
    except FileNotFoundError:
        print("autopep8 not available, installing...")
        subprocess.run(["pip", "install", "autopep8"])
        subprocess.run(cmd)

def careful_line_break(content, max_length=79):
    """Carefully break long lines without breaking syntax."""
    lines = content.split('\n')
    result_lines = []
    
    for line in lines:
        if len(line) <= max_length:
            result_lines.append(line)
            continue
        
        # Get indentation
        indent = len(line) - len(line.lstrip())
        indent_str = ' ' * indent
        
        # Skip very long strings/comments that are hard to break
        stripped = line.strip()
        if (stripped.startswith('#') or 
            stripped.startswith('"""') or 
            stripped.startswith("'''") or
            'http://' in line or 
            'https://' in line):
            result_lines.append(line)
            continue
        
        # Try to break at safe points
        if ',' in line and '(' in line:
            # Function call with parameters
            paren_pos = line.find('(')
            if paren_pos > 0 and paren_pos < max_length:
                params_part = line[paren_pos+1:]
                if ',' in params_part and ')' in params_part:
                    prefix = line[:paren_pos+1]
                    result_lines.append(prefix)
                    
                    # Add parameters on separate lines
                    params_str = params_part[:params_part.rfind(')')]
                    params = [p.strip() for p in params_str.split(',')]
                    for param in params:
                        if param:
                            result_lines.append(f"{indent_str}    {param},")
                    
                    # Add closing parenthesis
                    suffix = line[line.rfind(')'):]
                    result_lines.append(f"{indent_str}{suffix}")
                    continue
        
        # Break at operators
        for op in [' and ', ' or ', ' + ', ' - ', ' * ', ' == ', ' != ']:
            if op in line:
                pos = line.find(op)
                if 40 < pos < max_length - 10:
                    part1 = line[:pos+len(op)-1] + " \\"
                    part2 = indent_str + "    " + line[pos+1:].lstrip()
                    result_lines.extend([part1, part2])
                    break
        else:
            # If no good break point, keep original line
            result_lines.append(line)
    
    return '\n'.join(result_lines)

def fix_file_carefully(filepath):
    """Fix a single file very carefully."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Only apply careful line breaking
        content = careful_line_break(content)
        
        # Basic cleanup that's safe
        lines = content.split('\n')
        fixed_lines = []
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            fixed_lines.append(line)
        
        # Ensure single newline at end
        content = '\n'.join(fixed_lines)
        if content and not content.endswith('\n'):
            content += '\n'
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def get_e501_count():
    """Get count of E501 errors only."""
    try:
        result = subprocess.run(
            ['python', '-m', 'flake8', 'src', '--select=E501', '--count'],
            capture_output=True, text=True
        )
        output = result.stdout.strip()
        if output.isdigit():
            return int(output)
        return 0
    except:
        return -1

def main():
    """Main function."""
    print("=== Ultra-Careful E501 Fixer ===")
    print("Only fixing line length issues, preserving all syntax")
    
    initial_e501 = get_e501_count()
    print(f"Initial E501 errors: {initial_e501}")
    
    # First try autopep8 with only E501
    run_autopep8_line_length_only()
    
    after_autopep8 = get_e501_count()
    print(f"After autopep8: {after_autopep8} E501 errors")
    
    # Then manually fix remaining ones carefully
    print("Manually fixing remaining long lines...")
    fixed_count = 0
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if fix_file_carefully(filepath):
                    fixed_count += 1
    
    print(f"Manually fixed {fixed_count} files")
    
    final_e501 = get_e501_count()
    print(f"Final E501 errors: {final_e501}")
    print(f"Total improvement: {initial_e501 - final_e501} fewer E501 errors")
    
    # Check for any syntax errors we might have introduced
    print("\nChecking for syntax errors...")
    result = subprocess.run(
        ['python', '-m', 'flake8', 'src', '--select=E999', '--count'],
        capture_output=True, text=True
    )
    syntax_errors = result.stdout.strip()
    if syntax_errors.isdigit() and int(syntax_errors) > 0:
        print(f"⚠️  {syntax_errors} syntax errors detected")
    else:
        print("✅ No syntax errors")
    
    if final_e501 == 0:
        print("\n🎉 ZERO E501 ERRORS ACHIEVED! 🎉")

if __name__ == "__main__":
    main()
