#!/usr/bin/env python3
"""
Automated script to fix all linting errors in pricing_agent.py
"""

import re
import os

def fix_pricing_agent():
    """Fix all linting errors in the pricing agent file."""
    filepath = "src/agents/pricing_agent.py"
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Split into lines for easier processing
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Remove trailing whitespace
        line = line.rstrip()
        
        # Fix inline comments (need at least 2 spaces before #)
        if '#' in line and not line.strip().startswith('#'):
            # Find the comment
            comment_pos = line.find('#')
            if comment_pos > 0:
                before_comment = line[:comment_pos].rstrip()
                comment = line[comment_pos:]
                # Ensure at least 2 spaces before comment
                if not before_comment.endswith('  '):
                    line = before_comment + '  ' + comment
        
        # Fix long lines by breaking them
        if len(line) > 79:
            line = fix_long_line(line, i)
        
        fixed_lines.append(line)
    
    # Join lines back together
    content = '\n'.join(fixed_lines)
    
    # Fix other issues
    content = fix_other_issues(content)
    
    # Ensure file ends with newline
    if not content.endswith('\n'):
        content += '\n'
    
    # Write back
    with open(filepath, 'w') as f:
        f.write(content)
    
    print("Fixed all linting errors in pricing_agent.py")

def fix_long_line(line, line_num):
    """Fix a long line by breaking it appropriately."""
    if len(line) <= 79:
        return line
    
    # Get indentation
    indent = len(line) - len(line.lstrip())
    indent_str = ' ' * indent
    
    # Handle different patterns
    if '=' in line and line.count('=') == 1 and not line.strip().startswith('#'):
        # Assignment
        parts = line.split('=', 1)
        if len(parts) == 2:
            var_part = parts[0].strip()
            value_part = parts[1].strip()
            if len(var_part) + len(value_part) + 3 > 79:
                return f"{indent_str}{var_part} = (\n{indent_str}    {value_part})"
    
    elif line.strip().startswith('"""') and line.strip().endswith('"""'):
        # Docstring on one line - leave as is for now
        return line
    
    elif ',' in line and '(' in line:
        # Function call or parameter list
        return break_at_commas(line, indent_str)
    
    elif ' and ' in line or ' or ' in line:
        # Boolean expressions
        for op in [' and ', ' or ']:
            if op in line:
                pos = line.find(op)
                if 40 < pos < 70:
                    return line[:pos] + ' \\' + '\n' + indent_str + '    ' + line[pos+1:].lstrip()
    
    # Default: try to break at a reasonable point
    if len(line) > 79:
        # Find a good break point (space, operator, etc.)
        break_points = []
        for i, char in enumerate(line):
            if char in [' ', '+', '-', '*', '/', '=', '<', '>', '&', '|']:
                if 60 < i < 75:
                    break_points.append(i)
        
        if break_points:
            bp = break_points[0]
            return line[:bp+1] + ' \\' + '\n' + indent_str + '    ' + line[bp+1:].lstrip()
    
    return line

def break_at_commas(line, indent_str):
    """Break a line at commas if it contains function parameters."""
    if '(' in line and ')' in line and ',' in line:
        # Find the parentheses
        paren_start = line.find('(')
        paren_end = line.rfind(')')
        
        if paren_start > 0 and paren_end > paren_start:
            prefix = line[:paren_start+1]
            params = line[paren_start+1:paren_end]
            suffix = line[paren_end:]
            
            if ',' in params:
                param_list = [p.strip() for p in params.split(',')]
                if len(param_list) > 1:
                    result = prefix + '\n'
                    for i, param in enumerate(param_list):
                        if param:
                            comma = ',' if i < len(param_list) - 1 else ''
                            result += f"{indent_str}    {param}{comma}\n"
                    result += f"{indent_str}{suffix}"
                    return result
    
    return line

def fix_other_issues(content):
    """Fix other linting issues."""
    
    # Fix blank line issues
    # Remove excessive blank lines
    content = re.sub(r'\n\s*\n\s*\n\s*\n', '\n\n\n', content)
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Fix blank line contains whitespace
    content = re.sub(r'\n[ \t]+\n', '\n\n', content)
    
    # Fix F541 f-string missing placeholders
    content = re.sub(r'f"([^{]*)"', r'"\1"', content)
    content = re.sub(r"f'([^{]*)'", r"'\1'", content)
    
    # Fix undefined variables (basic cases)
    content = content.replace('customer_3', 'customer_3_data')
    content = content.replace('customer_5', 'customer_5_data')
    
    # Fix unused variables by prefixing with underscore
    content = re.sub(r'start_time = ', '_start_time = ', content)
    
    return content

if __name__ == "__main__":
    fix_pricing_agent()
