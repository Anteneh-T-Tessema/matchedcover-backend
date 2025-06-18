#!/usr/bin/env python3
"""
Fix the specific 4-quote docstring issue.
"""

import os
import re

def fix_docstring_issue():
    """Fix the specific docstring 4-quote issue."""
    fixed_count = 0
    
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Fix the specific issue: """" -> """
                content = content.replace('""""', '"""')
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed_count += 1
                    print(f"Fixed {filepath}")
    
    print(f"Fixed {fixed_count} files")

if __name__ == "__main__":
    fix_docstring_issue()
