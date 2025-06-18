#!/usr/bin/env python3
"""
Targeted indentation fix for specific methods in pricing_agent.py.
"""

import re
import sys

def fix_specific_methods(file_path):
    """Fix indentation in specific problematic methods."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix volume discount method
    content = fix_calculate_volume_discount(content)
    
    # Fix loyalty discount method
    content = fix_calculate_loyalty_discount(content)
    
    # Fix profit margin method
    content = fix_calculate_profit_margin(content)
    
    # Fix age factor method
    content = fix_calculate_age_factor(content)
    
    # Fix pricing strategy application
    content = fix_apply_pricing_strategy(content)
    
    # Fix competitiveness rating
    content = fix_competitiveness_rating(content)
    
    # Write the fixed content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed specific method indentation in {file_path}")

def fix_calculate_volume_discount(content):
    """Fix the _calculate_volume_discount method."""
    pattern = r'(async def _calculate_volume_discount.*?\):.*?\n)(.*?)(return PricingFactor)'
    
    def replacement(match):
        method_def = match.group(1)
        method_body = match.group(2)
        return_stmt = match.group(3)
        
        # Fix indentation in the method body
        lines = method_body.split('\n')
        fixed_lines = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                fixed_lines.append('')
                continue
                
            if stripped.startswith('if '):
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('elif '):
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('else:'):
                fixed_lines.append('        ' + stripped)
            else:
                fixed_lines.append('            ' + stripped)
                
        return method_def + '\n'.join(fixed_lines) + '\n        ' + return_stmt
    
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

def fix_calculate_loyalty_discount(content):
    """Fix the _calculate_loyalty_discount method."""
    pattern = r'(async def _calculate_loyalty_discount.*?\):.*?\n)(.*?)(return PricingFactor)'
    
    def replacement(match):
        method_def = match.group(1)
        method_body = match.group(2)
        return_stmt = match.group(3)
        
        # Fix indentation in the method body
        lines = method_body.split('\n')
        fixed_lines = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                fixed_lines.append('')
                continue
                
            if stripped.startswith('if '):
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('elif '):
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('else:'):
                fixed_lines.append('        ' + stripped)
            else:
                fixed_lines.append('            ' + stripped)
                
        return method_def + '\n'.join(fixed_lines) + '\n        ' + return_stmt
    
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

def fix_calculate_profit_margin(content):
    """Fix the _calculate_profit_margin method."""
    pattern = r'(async def _calculate_profit_margin.*?\):.*?\n)(.*?)(return PricingFactor)'
    
    def replacement(match):
        method_def = match.group(1)
        method_body = match.group(2)
        return_stmt = match.group(3)
        
        # Fix indentation in the method body
        lines = method_body.split('\n')
        fixed_lines = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                fixed_lines.append('')
                continue
                
            if stripped.startswith('if '):
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('elif '):
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('else:'):
                fixed_lines.append('        ' + stripped)
            else:
                fixed_lines.append('            ' + stripped)
                
        return method_def + '\n'.join(fixed_lines) + '\n        ' + return_stmt
    
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

def fix_calculate_age_factor(content):
    """Fix the _calculate_age_factor method."""
    pattern = r'(def _calculate_age_factor.*?\):.*?\n)(.*?)(\n    \S)'
    
    def replacement(match):
        method_def = match.group(1)
        method_body = match.group(2)
        next_line = match.group(3)
        
        # Fix indentation in the method body
        lines = method_body.split('\n')
        fixed_lines = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                fixed_lines.append('')
                continue
                
            if stripped.startswith('if '):
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('elif '):
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('else:'):
                fixed_lines.append('        ' + stripped)
            else:
                fixed_lines.append('            ' + stripped)
                
        return method_def + '\n'.join(fixed_lines) + next_line
    
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

def fix_apply_pricing_strategy(content):
    """Fix the _apply_pricing_strategy method."""
    pattern = r'(async def _apply_pricing_strategy.*?\):.*?\n)(.*?)(return final_premium)'
    
    def replacement(match):
        method_def = match.group(1)
        method_body = match.group(2)
        return_stmt = match.group(3)
        
        # Fix indentation in the method body
        lines = method_body.split('\n')
        fixed_lines = []
        in_try = False
        in_except = False
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                fixed_lines.append('')
                continue
                
            if stripped == 'try:':
                in_try = True
                in_except = False
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('except '):
                in_try = False
                in_except = True
                fixed_lines.append('        ' + stripped)
            elif in_try or in_except:
                if stripped.startswith('if '):
                    fixed_lines.append('            ' + stripped)
                elif stripped.startswith('elif '):
                    fixed_lines.append('            ' + stripped)
                elif stripped.startswith('else:'):
                    fixed_lines.append('            ' + stripped)
                else:
                    fixed_lines.append('                ' + stripped)
            else:
                fixed_lines.append('        ' + stripped)
                
        return method_def + '\n'.join(fixed_lines) + '\n        ' + return_stmt
    
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

def fix_competitiveness_rating(content):
    """Fix the _get_competitiveness_rating method."""
    pattern = r'(def _get_competitiveness_rating.*?\):.*?\n)(.*?)(\n(\s*def|\Z))'
    
    def replacement(match):
        method_def = match.group(1)
        method_body = match.group(2)
        next_section = match.group(3)
        
        # Fix indentation in the method body
        lines = method_body.split('\n')
        fixed_lines = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                fixed_lines.append('')
                continue
                
            if stripped.startswith('if '):
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('elif '):
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('else:'):
                fixed_lines.append('        ' + stripped)
            else:
                fixed_lines.append('            ' + stripped)
                
        return method_def + '\n'.join(fixed_lines) + next_section
    
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_specific_methods.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    fix_specific_methods(file_path)
