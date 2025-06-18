"""
Script to fix all linting issues in pricing_agent.py
"""

import subprocess
import sys
import re


def fix_all_linting_issues(file_path):
    # First, let's fix the docstrings and f-strings
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix docstrings
    content = content.replace('""""', '"""')
    
    # Fix f-strings with broken expressions
    content = re.sub(
        r'f"(.*?){([^}]*?)"([^"]*?)"}(.*?)"',
        r'f"\1{\2\3}\4"', 
        content
    )
    
    # Fix indentation in class definitions
    content = re.sub(
        r'class PricingStrategy\(Enum\):\n    """Pricing strategy options."""\n\n    COMPETITIVE = "competitive"\nPENETRATION',
        r'class PricingStrategy(Enum):\n    """Pricing strategy options."""\n\n    COMPETITIVE = "competitive"\n    PENETRATION',
        content
    )
    
    content = re.sub(
        r'class PricingFactorType\(Enum\):\n    """Types of pricing factors."""\n\n    BASE_RATE = "base_rate"\nRISK_ADJUSTMENT',
        r'class PricingFactorType(Enum):\n    """Types of pricing factors."""\n\n    BASE_RATE = "base_rate"\n    RISK_ADJUSTMENT',
        content
    )
    
    # Write fixed content back to file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    # Now run black to fix all formatting
    try:
        subprocess.run(
            ["black", "--line-length", "79", file_path],
            check=True
        )
        print(f"Successfully formatted {file_path} with black")
        
        # Run autopep8 as well for additional fixes
        subprocess.run(
            [
                "autopep8",
                "--in-place",
                "--aggressive", 
                "--max-line-length", "79",
                file_path
            ],
            check=True
        )
        print(f"Successfully applied autopep8 to {file_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running formatting tools: {e}")
        sys.exit(1)


if __name__ == "__main__":
    file_path = "/Users/antenehtessema/Desktop/MatchInsurane/src/agents/pricing_agent.py"
    fix_all_linting_issues(file_path)
