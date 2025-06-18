"""
Final fix script for pricing_agent.py
"""

import re


def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Fix PricingStrategy indentation
    start_idx = -1
    for i, line in enumerate(lines):
        if "class PricingStrategy(Enum):" in line:
            start_idx = i
            break
    
    if start_idx != -1:
        for i in range(start_idx + 3, start_idx + 8):
            if i < len(lines) and not lines[i].startswith(' '):
                lines[i] = '    ' + lines[i]
    
    # Fix PricingFactorType indentation
    start_idx = -1
    for i, line in enumerate(lines):
        if "class PricingFactorType(Enum):" in line:
            start_idx = i
            break
    
    if start_idx != -1:
        for i in range(start_idx + 3, start_idx + 9):
            if i < len(lines) and not lines[i].startswith(' '):
                lines[i] = '    ' + lines[i]
    
    # Fix dataclass field indentation
    for i, line in enumerate(lines):
        if '@dataclass' in line and i+2 < len(lines):
            class_name = lines[i+1].strip()
            j = i + 2
            while j < len(lines) and not (lines[j].strip() == '' or lines[j].strip().startswith('@') or lines[j].strip().startswith('class ')):
                if not lines[j].startswith(' ') and lines[j].strip():
                    lines[j] = '    ' + lines[j]
                j += 1
    
    # Fix __init__ method indentation
    start_idx = -1
    for i, line in enumerate(lines):
        if "def __init__(self):" in line:
            start_idx = i
            break
    
    if start_idx != -1:
        for i in range(start_idx + 1, len(lines)):
            if lines[i].strip() == '':
                break
            if not lines[i].startswith(' '):
                lines[i] = '        ' + lines[i]
    
    # Fix calculate_quote method indentation and docstring
    start_idx = -1
    for i, line in enumerate(lines):
        if "async def calculate_quote" in line:
            start_idx = i
            break
    
    if start_idx != -1:
        # Fix parameters indentation
        j = start_idx
        while j < len(lines) and ')' not in lines[j]:
            if j > start_idx and not lines[j].startswith(' '):
                lines[j] = '        ' + lines[j]
            j += 1
        
        # Fix docstring
        if j < len(lines) and '""""' in lines[j+1]:
            lines[j+1] = lines[j+1].replace('""""', '"""')
            
            # Find end of docstring
            k = j + 2
            while k < len(lines) and '""""' not in lines[k]:
                if not lines[k].startswith(' '):
                    lines[k] = '        ' + lines[k]
                k += 1
            
            if k < len(lines) and '""""' in lines[k]:
                lines[k] = lines[k].replace('""""', '"""')
    
    # Write fixed content back
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


if __name__ == "__main__":
    file_path = "/Users/antenehtessema/Desktop/MatchInsurane/src/agents/pricing_agent.py"
    fix_file(file_path)
