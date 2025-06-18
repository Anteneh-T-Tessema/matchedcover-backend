#!/usr/bin/env python3
"""
Fix for dataclass decorator issues in pricing_agent.py.
"""

import re
import sys

def fix_dataclass_decorator(file_path):
    """Fix dataclass decorator syntax."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all @dataclass decorators and ensure they're properly formatted
    # We're looking for @dataclass with the class definition on the next line
    fixed_content = re.sub(
        r'(@dataclass)\s*\n\s*class',
        r'@dataclass\nclass',
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(fixed_content)
    
    print(f"Fixed dataclass decorators in {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_dataclass.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    fix_dataclass_decorator(file_path)
