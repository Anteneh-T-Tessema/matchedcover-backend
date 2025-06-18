#!/usr/bin/env python3
"""
Final manual fixes for specific blocks in pricing_agent.py.
"""

import sys
import re

def apply_final_fixes(file_path):
    """Apply final manual fixes to specific blocks with indentation issues."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Define fixes for specific method blocks
    fixes = [
        # Fix for _calculate_base_premium
        (
            r'async def _calculate_base_premium\([^)]*\):[^}]*?try:',
            lambda m: m.group(0).replace('try:', '        try:')
        ),
        # Fix for if/elif/else in _calculate_age_factor
        (
            r'def _calculate_age_factor\([^)]*\):[^}]*?if policy_type == "auto":[^}]*?if age < 25:',
            lambda m: m.group(0).replace('if age < 25:', '            if age < 25:')
        ),
        (
            r'if age < 25:[^}]*?return Decimal\("1.3"\)',
            lambda m: m.group(0).replace('return Decimal("1.3")', '                return Decimal("1.3")')
        ),
        (
            r'return Decimal\("1.3"\)[^}]*?elif age > 65:',
            lambda m: m.group(0).replace('elif age > 65:', '            elif age > 65:')
        ),
        (
            r'elif age > 65:[^}]*?return Decimal\("1.1"\)',
            lambda m: m.group(0).replace('return Decimal("1.1")', '                return Decimal("1.1")')
        ),
        (
            r'return Decimal\("1.1"\)[^}]*?else:',
            lambda m: m.group(0).replace('else:', '            else:')
        ),
        (
            r'else:[^}]*?return Decimal\("1.0"\)',
            lambda m: m.group(0).replace('return Decimal("1.0")', '                return Decimal("1.0")')
        ),
        (
            r'return Decimal\("1.0"\)[^}]*?elif policy_type == "life":',
            lambda m: m.group(0).replace('elif policy_type == "life":', '        elif policy_type == "life":')
        ),
        (
            r'elif policy_type == "life":[^}]*?return Decimal\(str\(1.0 \+ \(age - 30\) \* 0.01\)\)',
            lambda m: m.group(0).replace('return Decimal(str(1.0 + (age - 30) * 0.01))', '            return Decimal(str(1.0 + (age - 30) * 0.01))')
        ),
        (
            r'return Decimal\(str\(1.0 \+ \(age - 30\) \* 0.01\)\)[^}]*?elif policy_type == "health":',
            lambda m: m.group(0).replace('elif policy_type == "health":', '        elif policy_type == "health":')
        ),
        (
            r'elif policy_type == "health":[^}]*?return Decimal\(str\(1.0 \+ max\(0, age - 25\) \* 0.015\)\)',
            lambda m: m.group(0).replace('return Decimal(str(1.0 + max(0, age - 25) * 0.015))', '            return Decimal(str(1.0 + max(0, age - 25) * 0.015))')
        ),
        (
            r'return Decimal\(str\(1.0 \+ max\(0, age - 25\) \* 0.015\)\)[^}]*?else:',
            lambda m: m.group(0).replace('else:', '        else:')
        ),
        (
            r'else:[^}]*?return Decimal\("1.0"\)',
            lambda m: m.group(0).replace('return Decimal("1.0")', '            return Decimal("1.0")')
        ),
        # Fix for _apply_pricing_strategy method
        (
            r'async def _apply_pricing_strategy\([^)]*\):[^}]*?try:',
            lambda m: m.group(0).replace('try:', '        try:')
        ),
        (
            r'try:[^}]*?adjusted_factors = factors.copy\(\)',
            lambda m: m.group(0).replace('adjusted_factors = factors.copy()', '            adjusted_factors = factors.copy()')
        ),
        # Fix for weighted_adjustment calculation
        (
            r'for factor in adjusted_factors:[^}]*?weighted_adjustment = factor.value \* Decimal\(',
            lambda m: m.group(0).replace('weighted_adjustment = factor.value * Decimal(', '                weighted_adjustment = factor.value * Decimal(')
        ),
        # Fix for except clause
        (
            r'adjustment_multiplier[^}]*?except Exception as e:',
            lambda m: m.group(0).replace('except Exception as e:', '        except Exception as e:')
        ),
        # Fix for _calculate_market_competitiveness method
        (
            r'async def _calculate_market_competitiveness\([^)]*\):[^}]*?try:',
            lambda m: m.group(0).replace('try:', '        try:')
        ),
        (
            r'try:[^}]*?if market_data.market_average > 0:',
            lambda m: m.group(0).replace('if market_data.market_average > 0:', '            if market_data.market_average > 0:')
        ),
        (
            r'if market_data.market_average > 0:[^}]*?competitiveness = float\(',
            lambda m: m.group(0).replace('competitiveness = float(', '                competitiveness = float(')
        ),
        (
            r'\) \/ float\(market_data.market_average\)[^}]*?except Exception:',
            lambda m: m.group(0).replace('except Exception:', '        except Exception:')
        ),
        # Fix for _get_competitiveness_rating method
        (
            r'def _get_competitiveness_rating\([^)]*\):[^}]*?if percentile >= 0.8:',
            lambda m: m.group(0).replace('if percentile >= 0.8:', '        if percentile >= 0.8:')
        ),
        (
            r'if percentile >= 0.8:[^}]*?return "highly_competitive"',
            lambda m: m.group(0).replace('return "highly_competitive"', '            return "highly_competitive"')
        ),
        (
            r'return "highly_competitive"[^}]*?elif percentile >= 0.6:',
            lambda m: m.group(0).replace('elif percentile >= 0.6:', '        elif percentile >= 0.6:')
        ),
        (
            r'elif percentile >= 0.6:[^}]*?return "competitive"',
            lambda m: m.group(0).replace('return "competitive"', '            return "competitive"')
        ),
        (
            r'return "competitive"[^}]*?elif percentile >= 0.4:',
            lambda m: m.group(0).replace('elif percentile >= 0.4:', '        elif percentile >= 0.4:')
        ),
        (
            r'elif percentile >= 0.4:[^}]*?return "average"',
            lambda m: m.group(0).replace('return "average"', '            return "average"')
        ),
        (
            r'return "average"[^}]*?elif percentile >= 0.2:',
            lambda m: m.group(0).replace('elif percentile >= 0.2:', '        elif percentile >= 0.2:')
        ),
        (
            r'elif percentile >= 0.2:[^}]*?return "above_average"',
            lambda m: m.group(0).replace('return "above_average"', '            return "above_average"')
        ),
        (
            r'return "above_average"[^}]*?else:',
            lambda m: m.group(0).replace('else:', '        else:')
        ),
        (
            r'else:[^}]*?return "premium_pricing"',
            lambda m: m.group(0).replace('return "premium_pricing"', '            return "premium_pricing"')
        ),
    ]
    
    # Apply all fixes
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write the fixed content
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Applied final manual fixes to {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python final_manual_fix.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    apply_final_fixes(file_path)
