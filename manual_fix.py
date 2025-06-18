#!/usr/bin/env python3
"""
Manual fix for pricing_agent.py - focusing on dataclass and specific methods.
"""

import sys

def manual_fix(file_path):
    """Apply manual fixes to the pricing agent file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Fix dataclass decorators
    fixed_lines = []
    for i, line in enumerate(lines):
        if line.strip() == '@dataclass':
            # Make sure next line starts with 'class'
            next_line = lines[i+1] if i+1 < len(lines) else ''
            if not next_line.lstrip().startswith('class'):
                fixed_lines.append('@dataclass\n')
                continue
        fixed_lines.append(line)
    
    # Write the fixed content
    with open(file_path, 'w') as f:
        f.writelines(fixed_lines)
    
    # Now do a second pass to fix specific methods
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix the calculate_loyalty_discount method
    content = content.replace(
        'async def _calculate_loyalty_discount(',
        '    async def _calculate_loyalty_discount('
    )
    content = content.replace(
        '            """Calculate loyalty-based discount."""',
        '        """Calculate loyalty-based discount."""'
    )
    
    # Fix the calculate_regulatory_surcharge method
    content = content.replace(
        '            async def _calculate_regulatory_surcharge(',
        '    async def _calculate_regulatory_surcharge('
    )
    content = content.replace(
        '            """Calculate regulatory surcharge."""',
        '        """Calculate regulatory surcharge."""'
    )
    
    # Fix the calculate_age_factor method
    content = content.replace(
        'def _calculate_age_factor(',
        '    def _calculate_age_factor('
    )
    
    # Write the fixed content
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Applied manual fixes to {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python manual_fix.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    manual_fix(file_path)
