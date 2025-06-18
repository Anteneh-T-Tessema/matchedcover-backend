"""
Script to fix string literal issues in pricing_agent.py
"""

import re


def fix_string_literals(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find and fix the calculate_quote method docstring
    pattern = r'async def calculate_quote\([^)]*\):\n        """"([^"]*?)""""'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        docstring_content = match.group(1)
        fixed_docstring = f'async def calculate_quote(self,\n        customer_data: Dict[str, Any],\n        policy_type: str,\n        coverage_amount: Decimal,\n        risk_assessment: RiskAssessment,\n        pricing_strategy: PricingStrategy = PricingStrategy.COMPETITIVE,\n    ) -> PricingQuote:\n        """{docstring_content}"""'
        content = re.sub(pattern, fixed_docstring, content, flags=re.DOTALL)
    
    # Fix broken string literals and concatenations
    fixes = [
        # Add other specific string fixes here
        (r'f"Calculating quote for \{policy_type\} policy, coverage: \{coverage_amount\}""', 
         r'f"Calculating quote for {policy_type} policy, coverage: {coverage_amount}"'),
        
        (r'f"Risk level: \{risk_assessment.overall_risk_level.value\}",',
         r'f"Risk level: {risk_assessment.overall_risk_level.value}",'),
        
        (r'f"Market competitive adjustment: \{adjustment_pct:.1f\}%",',
         r'f"Market competitive adjustment: {adjustment_pct:.1f}%",'),
        
        # Look for any other broken string patterns
        (r'"""\n    Calculate insurance quote with dynamic pricing\.',
         r'"""\n        Calculate insurance quote with dynamic pricing.'),
    ]
    
    for old, new in fixes:
        content = content.replace(old, new)
    
    # Write back to file
    with open(file_path, 'w') as file:
        file.write(content)
    
    print(f"Fixed string literal issues in {file_path}")


if __name__ == "__main__":
    file_path = "/Users/antenehtessema/Desktop/MatchInsurane/src/agents/pricing_agent.py"
    fix_string_literals(file_path)
