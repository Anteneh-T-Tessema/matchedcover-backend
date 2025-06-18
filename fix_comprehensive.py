"""
Comprehensive indentation fixer for pricing_agent.py
"""

import re


def fix_file_indentation(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix enum class definitions
    content = re.sub(
        r'class PricingStrategy\(Enum\):\n\s+"""Pricing strategy options."""\n\n\s+COMPETITIVE = "competitive"\n(?!\s+)PENETRATION',
        r'class PricingStrategy(Enum):\n    """Pricing strategy options."""\n\n    COMPETITIVE = "competitive"\n    PENETRATION',
        content
    )
    
    content = re.sub(
        r'class PricingFactorType\(Enum\):\n\s+"""Types of pricing factors."""\n\n\s+BASE_RATE = "base_rate"\n(?!\s+)RISK_ADJUSTMENT',
        r'class PricingFactorType(Enum):\n    """Types of pricing factors."""\n\n    BASE_RATE = "base_rate"\n    RISK_ADJUSTMENT',
        content
    )
    
    # Fix dataclass fields indentation
    for dataclass in ["PricingFactor", "PricingQuote", "MarketData"]:
        pattern = fr'@dataclass\nclass {dataclass}.*?:\n\s+""".*?"""\n\n(.*?)(?=\n\n)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            fields_block = match.group(1)
            fixed_fields = []
            for line in fields_block.split('\n'):
                if line.strip() and not line.startswith('    '):
                    fixed_fields.append('    ' + line)
                else:
                    fixed_fields.append(line)
            
            fixed_block = '\n'.join(fixed_fields)
            content = content.replace(fields_block, fixed_block)
    
    # Fix method indentation in PricingAgent class
    pattern = r'class PricingAgent\(BaseAgent\):.*?(?=\n\n\n|$)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        class_block = match.group(0)
        
        # Fix __init__ method indentation
        init_pattern = r'def __init__\(self\):.*?(?=\n\s+def|\n\s+async def|\n\n\n|$)'
        init_match = re.search(init_pattern, class_block, re.DOTALL)
        if init_match:
            init_block = init_match.group(0)
            fixed_init = []
            for line in init_block.split('\n'):
                if line.strip().startswith('def '):
                    fixed_init.append(line)
                elif line.strip() and not line.startswith('    '):
                    fixed_init.append('        ' + line)
                else:
                    fixed_init.append(line)
            
            fixed_init_block = '\n'.join(fixed_init)
            class_block = class_block.replace(init_block, fixed_init_block)
        
        # Fix async methods indentation (for each method)
        method_pattern = r'(async )?def (_[a-z_]+).*?(?=\n\s+(?:async )?def|\n\n\n|$)'
        for method_match in re.finditer(method_pattern, class_block, re.DOTALL):
            method_block = method_match.group(0)
            
            # Fix method body indentation
            fixed_method = []
            in_docstring = False
            for line in method_block.split('\n'):
                if line.strip().startswith(('def ', 'async def ')):
                    fixed_method.append(line)
                    continue
                
                if '"""' in line:
                    in_docstring = not in_docstring
                
                if line.strip() and not line.startswith('    '):
                    fixed_method.append('        ' + line)
                else:
                    fixed_method.append(line)
            
            fixed_method_block = '\n'.join(fixed_method)
            class_block = class_block.replace(method_block, fixed_method_block)
        
        content = content.replace(match.group(0), class_block)
    
    # Fix broken f-strings
    # Example: f"Risk level: {risk_assessment" .overall_risk_level.value}",
    content = re.sub(
        r'f"([^"]*?){([^{}]+)"(\s*\.\s*[^{}]+)}',
        r'f"\1{\2\3}',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Fixed indentation issues in {file_path}")


if __name__ == "__main__":
    file_path = "/Users/antenehtessema/Desktop/MatchInsurane/src/agents/pricing_agent.py"
    fix_file_indentation(file_path)
