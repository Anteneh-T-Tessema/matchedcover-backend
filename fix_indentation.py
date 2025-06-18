"""
Script to fix remaining indentation issues in pricing_agent.py
"""
import re

def fix_indentation(content):
    """Fix indentation issues in the file."""
    lines = content.split('\n')
    fixed_lines = []
    
    in_method = False
    current_method = None
    expected_indent = 0
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            fixed_lines.append(line)
            continue
            
        # Check if we're starting a new method
        method_start = re.match(r'^(\s*)(?:async )?def\s+(\w+)', line)
        if method_start:
            in_method = True
            current_method = method_start.group(2)
            expected_indent = len(method_start.group(1)) + 4
            fixed_lines.append(line)
            continue
            
        # If we're in a method and the line is not properly indented
        if in_method and line.strip() and not line.startswith(' ' * expected_indent):
            # But it's not the end of the method (another method or class)
            if not (line.startswith('    def') or line.startswith('    async def') or line.startswith('class')):
                # Fix the indentation
                fixed_lines.append(' ' * expected_indent + line.lstrip())
                continue
                
        # Normal line, add as is
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

# Read the file
with open('/Users/antenehtessema/Desktop/MatchInsurane/src/agents/pricing_agent.py', 'r') as file:
    content = file.read()

# Fix indentation
fixed_content = fix_indentation(content)

# Write back to file
with open('/Users/antenehtessema/Desktop/MatchInsurane/src/agents/pricing_agent.py', 'w') as file:
    file.write(fixed_content)

print("Indentation fixes applied to pricing_agent.py")
