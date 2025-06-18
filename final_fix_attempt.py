"""
Final attempt to fix pricing_agent.py
"""

import os
import tempfile
import re

def fix_pricing_agent():
    # Make a backup copy of the file
    os.system("cd /Users/antenehtessema/Desktop/MatchInsurane && "
              "cp src/agents/pricing_agent.py src/agents/pricing_agent.py.bak")
    
    # Step 1: Create a simplified version of the file that black can format
    file_path = "/Users/antenehtessema/Desktop/MatchInsurane/src/agents/pricing_agent.py"
    simplified_file = create_simplified_file(file_path)
    
    # Step 2: Format the simplified file with black
    os.system(f"black --line-length 79 {simplified_file}")
    
    # Step 3: Copy the simplified file back to the original
    os.system(f"cp {simplified_file} {file_path}")
    
    # Step 4: Apply autopep8 for additional fixes
    os.system("cd /Users/antenehtessema/Desktop/MatchInsurane && "
              "autopep8 --in-place --aggressive "
              "--select=E1,E2,E3,E5,W1,W2,W3 src/agents/pricing_agent.py")
    
    print("Fixed pricing_agent.py - check results with flake8")

def create_simplified_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix docstrings - replace quadruple quotes with triple quotes
    content = content.replace('""""', '"""')
    
    # Fix PricingAgent class docstring
    content = re.sub(
        r'class PricingAgent\(BaseAgent\):\s+"""(.*?)"""',
        r'class PricingAgent(BaseAgent):\n    """\n    \1\n    """',
        content,
        flags=re.DOTALL
    )
    
    # Fix class definitions for Enums
    content = content.replace(
        'class PricingStrategy(Enum):\n    """Pricing strategy options."""\n\n    COMPETITIVE = "competitive"\nPENETRATION',
        'class PricingStrategy(Enum):\n    """Pricing strategy options."""\n\n    COMPETITIVE = "competitive"\n    PENETRATION'
    )
    
    content = content.replace(
        'class PricingFactorType(Enum):\n    """Types of pricing factors."""\n\n    BASE_RATE = "base_rate"\nRISK_ADJUSTMENT',
        'class PricingFactorType(Enum):\n    """Types of pricing factors."""\n\n    BASE_RATE = "base_rate"\n    RISK_ADJUSTMENT'
    )
    
    # Fix __init__ method indentation
    content = re.sub(
        r'def __init__\(self\):\n\s+super\(\).__init__\(name="PricingAgent", agent_type="pricing"\)\n(\s+)self',
        r'def __init__(self):\n        super().__init__(name="PricingAgent", agent_type="pricing")\n        self',
        content
    )
    
    # Fix the _initialize_pricing_models method indentation
    content = re.sub(
        r'def _initialize_pricing_models\(self\):\n\s+"""Initialize machine learning models for pricing."""\n(\s+)try:',
        r'def _initialize_pricing_models(self):\n        """Initialize machine learning models for pricing."""\n        try:',
        content
    )
    
    # Fix broken f-strings
    content = content.replace(
        'description=f"Risk level: {risk_assessment"\n            .overall_risk_level.value}","',
        'description=f"Risk level: {risk_assessment.overall_risk_level.value}",')
    
    content = content.replace(
        'description = f"Market competitive adjustment: {adjustment_pct:"\n            .1f}%","',
        'description=f"Market competitive adjustment: {adjustment_pct:.1f}%",')
    
    # Write the simplified content to a temporary file
    fd, temp_file = tempfile.mkstemp(suffix='.py')
    os.close(fd)
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return temp_file

if __name__ == "__main__":
    fix_pricing_agent()
