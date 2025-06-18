"""
Script to fix indentation and other formatting issues in pricing_agent.py
"""

import re
import sys

def fix_indentation(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # First, let's fix the class definitions for PricingStrategy and PricingFactorType
    # that have incorrect indentation
    fixed_content = re.sub(
        r'class PricingStrategy\(Enum\):\n    """Pricing strategy options."""\n\n    COMPETITIVE = "competitive"\nPENETRATION',
        'class PricingStrategy(Enum):\n    """Pricing strategy options."""\n\n    COMPETITIVE = "competitive"\n    PENETRATION',
        content
    )
    
    fixed_content = re.sub(
        r'class PricingFactorType\(Enum\):\n    """Types of pricing factors."""\n\n    BASE_RATE = "base_rate"\nRISK_ADJUSTMENT',
        'class PricingFactorType(Enum):\n    """Types of pricing factors."""\n\n    BASE_RATE = "base_rate"\n    RISK_ADJUSTMENT',
        fixed_content
    )
    
    # Fix dataclass definitions
    dataclasses = ['PricingFactor', 'PricingQuote', 'MarketData']
    for cls in dataclasses:
        pattern = fr'@dataclass\nclass {cls}.*?:\n    .*?\n(.*?)(?=\n\n)'
        match = re.search(pattern, fixed_content, re.DOTALL)
        if match:
            indented_fields = '\n'.join(['    ' + line.strip() for line in match.group(1).strip().split('\n')])
            fixed_content = re.sub(pattern, f'@dataclass\nclass {cls}.*?:\n    .*?\n{indented_fields}', fixed_content, flags=re.DOTALL)
    
    # Fix method parameters and docstrings
    methods = [
        ('def __init__', 'def _initialize_pricing_models'),
        ('def _initialize_pricing_models', 'async def calculate_quote'),
        ('async def calculate_quote', 'async def _calculate_base_premium'),
        ('async def _calculate_base_premium', 'async def _calculate_pricing_factors'),
        ('async def _calculate_pricing_factors', 'async def _get_market_data'),
        ('async def _get_market_data', 'async def _calculate_market_factor'),
        ('async def _calculate_market_factor', 'async def _calculate_volume_discount'),
        ('async def _calculate_volume_discount', 'async def _calculate_loyalty_discount'),
        ('async def _calculate_loyalty_discount', 'async def _calculate_regulatory_surcharge'),
        ('async def _calculate_regulatory_surcharge', 'async def _calculate_profit_margin'),
        ('async def _calculate_profit_margin', 'async def _apply_pricing_strategy'),
        ('async def _apply_pricing_strategy', 'async def _calculate_market_competitiveness'),
        ('async def _calculate_market_competitiveness', 'async def _calculate_pricing_confidence'),
        ('async def _calculate_pricing_confidence', 'def _calculate_age_factor'),
        ('def _calculate_age_factor', 'def _get_seasonal_factors'),
        ('def _get_seasonal_factors', 'def _generate_quote_id'),
        ('def _generate_quote_id', 'async def compare_with_competitors'),
        ('async def compare_with_competitors', 'def _get_competitiveness_rating')
    ]
    
    for i, (method_start, method_end) in enumerate(methods):
        pattern = fr'({method_start}.*?)(?={method_end}|$)'
        match = re.search(pattern, fixed_content, re.DOTALL)
        if match:
            method_content = match.group(1)
            
            # Fix parameter indentation (move them to be properly indented)
            param_pattern = r'(\s+)(self,\n)(\s*)([^)]+)'
            param_match = re.search(param_pattern, method_content, re.DOTALL)
            if param_match:
                base_indent = param_match.group(1)
                param_indent = base_indent + ' ' * 4
                params = param_match.group(4).strip().split(',\n')
                indented_params = [p.strip() for p in params]
                indented_params_str = f",\n{param_indent}".join(indented_params)
                method_content = re.sub(param_pattern, f"{base_indent}self,\n{param_indent}{indented_params_str}", method_content, flags=re.DOTALL)
            
            # Fix method body indentation
            lines = method_content.split('\n')
            indented_lines = []
            in_docstring = False
            docstring_indent = None
            
            for line in lines:
                if '"""' in line or "'''" in line:
                    if not in_docstring:  # Start of docstring
                        in_docstring = True
                        docstring_indent = line.index('"""') if '"""' in line else line.index("'''")
                    elif docstring_indent is not None and (line.strip().endswith('"""') or line.strip().endswith("'''")):  # End of docstring
                        in_docstring = False
                        docstring_indent = None
                
                if in_docstring and docstring_indent is not None and line.strip() and not (line.strip().startswith('"""') or line.strip().startswith("'''")):
                    # Indent docstring content correctly
                    indented_lines.append(' ' * docstring_indent + line.strip())
                else:
                    indented_lines.append(line)
            
            fixed_method = '\n'.join(indented_lines)
            fixed_content = fixed_content.replace(match.group(1), fixed_method)
    
    # Fix broken string concatenations
    broken_strings = [
        (r'logger.info\(\n            f"Calculating quote for {policy_type} policy,"\n                coverage: {coverage_amount}""',
         'logger.info(\n            f"Calculating quote for {policy_type} policy, coverage: {coverage_amount}"'),
        (r'description=f"Risk level: {risk_assessment"\n                .overall_risk_level.value}",',
         'description=f"Risk level: {risk_assessment.overall_risk_level.value}",'),
        (r'description=f"Market competitive adjustment: {adjustment_pct:"\n            .1f}%",',
         'description=f"Market competitive adjustment: {adjustment_pct:.1f}%",')
    ]
    
    for old, new in broken_strings:
        fixed_content = fixed_content.replace(old, new)
    
    # Fix various indentation issues by using autopep8
    # Note: We're doing a simple fix by correcting consistent indentation patterns
    # In a real scenario, you'd use autopep8 or black here
    
    # Write back to file
    with open(file_path, 'w') as file:
        file.write(fixed_content)
    
    print(f"Fixed indentation issues in {file_path}")

if __name__ == "__main__":
    file_path = "/Users/antenehtessema/Desktop/MatchInsurane/src/agents/pricing_agent.py"
    fix_indentation(file_path)
