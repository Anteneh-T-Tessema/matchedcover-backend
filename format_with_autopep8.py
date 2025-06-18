"""
Script to clean and format pricing_agent.py using autopep8
"""

import subprocess
import sys

def run_autopep8(file_path):
    try:
        # Run autopep8 with aggressive level 2 and line length 79
        subprocess.run(
            [
                "autopep8", 
                "--in-place", 
                "--aggressive", 
                "--aggressive", 
                "--max-line-length", "79", 
                file_path
            ],
            check=True
        )
        print(f"Successfully formatted {file_path} with autopep8")
    except subprocess.CalledProcessError as e:
        print(f"Error running autopep8: {e}")
        sys.exit(1)

if __name__ == "__main__":
    file_path = "/Users/antenehtessema/Desktop/MatchInsurane/src/agents/pricing_agent.py"
    run_autopep8(file_path)
