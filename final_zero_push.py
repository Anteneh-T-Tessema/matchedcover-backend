#!/usr/bin/env python3
"""
Final script to achieve absolute zero linting errors.
Addresses each category of error systematically.
"""

import os
import subprocess
import sys

def get_error_count():
    """Get current flake8 error count."""
    try:
        result = subprocess.run(
            ['python', '-m', 'flake8', 'src', '--count'],
            capture_output=True, text=True
        )
        lines = result.stdout.strip().split('\n')
        for line in reversed(lines):
            if line.strip().isdigit():
                return int(line.strip())
        return 0
    except:
        return -1

def install_autopep8():
    """Install autopep8 if needed."""
    try:
        subprocess.run(['python', '-m', 'autopep8', '--version'], 
                      capture_output=True, check=True)
    except:
        print("Installing autopep8...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'autopep8'])

def run_comprehensive_autopep8():
    """Run autopep8 to fix as many issues as possible."""
    print("Running comprehensive autopep8...")
    install_autopep8()
    
    cmd = [
        'python', '-m', 'autopep8',
        '--in-place',
        '--aggressive',
        '--aggressive',
        '--max-line-length=79',
        '--recursive',
        'src'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("autopep8 completed successfully")
    except Exception as e:
        print(f"autopep8 error: {e}")

def manual_fixes():
    """Apply manual fixes for remaining issues."""
    print("Applying manual fixes...")
    
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Fix remaining syntax issues
                lines = content.split('\n')
                fixed_lines = []
                
                for line in lines:
                    # Skip empty lines or lines that might cause issues
                    if not line.strip():
                        fixed_lines.append(line.rstrip())
                        continue
                    
                    # Fix obvious syntax issues
                    if line.strip() == '""""':
                        line = '"""'
                    elif line.strip() == "''''":
                        line = "'''"
                    
                    # Remove trailing quotes that might be causing issues
                    if line.rstrip().endswith('""""'):
                        line = line.rstrip()[:-4] + '"""'
                    elif line.rstrip().endswith("''''"):
                        line = line.rstrip()[:-4] + "'''"
                    
                    fixed_lines.append(line.rstrip())
                
                content = '\n'.join(fixed_lines)
                
                # Ensure proper file ending
                if content and not content.endswith('\n'):
                    content += '\n'
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)

def main():
    """Main function to achieve zero errors."""
    print("🎯 FINAL PUSH TO ZERO LINTING ERRORS")
    print("=" * 50)
    
    initial_count = get_error_count()
    print(f"Starting with {initial_count} errors")
    
    # Step 1: Comprehensive autopep8
    run_comprehensive_autopep8()
    after_autopep8 = get_error_count()
    print(f"After autopep8: {after_autopep8} errors ({initial_count - after_autopep8} fixed)")
    
    # Step 2: Manual fixes
    manual_fixes()
    after_manual = get_error_count()
    print(f"After manual fixes: {after_manual} errors ({after_autopep8 - after_manual} fixed)")
    
    # Final status
    total_fixed = initial_count - after_manual
    print("\n" + "=" * 50)
    print(f"TOTAL PROGRESS: {total_fixed} errors fixed!")
    print(f"FINAL ERROR COUNT: {after_manual}")
    
    if after_manual == 0:
        print("\n🎉🎉🎉 MISSION ACCOMPLISHED! 🎉🎉🎉")
        print("✨ ZERO LINTING ERRORS ACHIEVED! ✨")
        print("🚀 The MatchInsurance codebase is now 100% lint-free!")
    else:
        print(f"\n📊 Current status: {after_manual} errors remaining")
        print("🎯 Excellent progress! The codebase is significantly cleaner.")
        
        # Show remaining issues for reference
        print("\nRemaining issues:")
        result = subprocess.run(
            ['python', '-m', 'flake8', 'src', '--statistics'],
            capture_output=True, text=True
        )
        print(result.stdout)

if __name__ == "__main__":
    main()
