"""
Minimal linting fixes for pricing_agent.py
"""
import os

def fix_file():
    # First, fix the docstring quotes
    os.system("cd /Users/antenehtessema/Desktop/MatchInsurane && "
              "python fix_docstring_quotes.py")
    
    # Then use autopep8 to fix line length issues
    os.system("cd /Users/antenehtessema/Desktop/MatchInsurane && "
              "autopep8 --in-place --max-line-length=79 --select=E501 "
              "src/agents/pricing_agent.py")
    
    # Manually fix the remaining E999 errors to eliminate critical syntax issues
    # This creates a valid Python file without syntax errors
    with open("/Users/antenehtessema/Desktop/MatchInsurane/src/agents/pricing_agent.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix broken f-strings
    content = content.replace(
        'description=f"Risk level: {risk_assessment"\n            .overall_risk_level.value}","',
        'description=f"Risk level: {risk_assessment.overall_risk_level.value}",')
    
    content = content.replace(
        'description = f"Market competitive adjustment: {adjustment_pct:"\n            .1f}%","',
        'description=f"Market competitive adjustment: {adjustment_pct:.1f}%",')
    
    # Fix enum class indentation
    content = content.replace(
        'class PricingStrategy(Enum):\n    """Pricing strategy options."""\n\n    COMPETITIVE = "competitive"\nPENETRATION',
        'class PricingStrategy(Enum):\n    """Pricing strategy options."""\n\n    COMPETITIVE = "competitive"\n    PENETRATION')
    
    content = content.replace(
        'class PricingFactorType(Enum):\n    """Types of pricing factors."""\n\n    BASE_RATE = "base_rate"\nRISK_ADJUSTMENT',
        'class PricingFactorType(Enum):\n    """Types of pricing factors."""\n\n    BASE_RATE = "base_rate"\n    RISK_ADJUSTMENT')
    
    # Fix specific spacing issues
    content = content.replace('source = "risk_assessment",', 'source="risk_assessment",')
    content = content.replace('source = "market_data",', 'source="market_data",')
    
    # Write back the fixed file
    with open("/Users/antenehtessema/Desktop/MatchInsurane/src/agents/pricing_agent.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    # Now run autopep8 with aggressive settings for spacing
    os.system("cd /Users/antenehtessema/Desktop/MatchInsurane && "
              "autopep8 --in-place --aggressive --select=E2,E3,W2,W3 "
              "src/agents/pricing_agent.py")
    
    print("Fixed critical syntax errors in pricing_agent.py")

if __name__ == "__main__":
    fix_file()
