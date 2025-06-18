#!/usr/bin/env python3
"""Fix F841 unused variable issues by commenting them out"""

import re
from pathlib import Path

# Map of files and line numbers with unused variables to fix
UNUSED_VARS = {
    "src/agents/compliance_agent.py": [305],
    "src/agents/guardrail_ai_agent.py": [217, 280],
    "src/agents/risk_assessor.py": [217, 220],
    "src/api/blockchain_fraud_detection.py": [494],
    "src/api/compliance_api.py": [419, 678],
    "src/blockchain/chaincode/fraud_audit_chaincode.py": [134],
    "src/compliance/aml_bsa_compliance.py": [261],
}

def fix_unused_vars_in_file(file_path, line_numbers):
    """Comment out unused variables on specific lines"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        changed = False
        for line_num in line_numbers:
            if line_num <= len(lines):
                line = lines[line_num - 1]  # Convert to 0-based index
                # Check if it's an assignment line and not already commented
                if '=' in line and not line.strip().startswith('#'):
                    # Find the variable name
                    match = re.search(r'(\s*)(\w+)\s*=', line)
                    if match:
                        indent, var_name = match.groups()
                        # Comment out the line
                        lines[line_num - 1] = f"{indent}# {var_name} = ...  # Unused variable\n"
                        changed = True
        
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    files_changed = 0
    
    for file_path, line_numbers in UNUSED_VARS.items():
        if fix_unused_vars_in_file(file_path, line_numbers):
            files_changed += 1
            print(f"Fixed unused variables in: {file_path}")
    
    print(f"Fixed unused variables in {files_changed} files")

if __name__ == '__main__':
    main()
