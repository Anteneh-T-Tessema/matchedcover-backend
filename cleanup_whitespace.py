#!/usr/bin/env python3
"""
Script to automatically fix whitespace-related linting issues:
- W293: blank line contains whitespace
- W291: trailing whitespace
"""

import os
import re
from pathlib import Path

def clean_whitespace_in_file(file_path):
    """Clean whitespace issues in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into lines
        lines = content.splitlines()
        
        # Fix each line
        cleaned_lines = []
        for line in lines:
            # Remove trailing whitespace (W291)
            # Remove whitespace from blank lines (W293)
            cleaned_line = line.rstrip()
            cleaned_lines.append(cleaned_line)
        
        # Join lines back
        cleaned_content = '\n'.join(cleaned_lines)
        
        # Add final newline if the original had one
        if content.endswith('\n'):
            cleaned_content += '\n'
        
        # Write back only if content changed
        if content != cleaned_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Clean whitespace in all Python files in src/"""
    src_dir = Path('src')
    if not src_dir.exists():
        print("src/ directory not found")
        return
    
    files_processed = 0
    files_changed = 0
    
    # Find all Python files
    for py_file in src_dir.rglob('*.py'):
        files_processed += 1
        if clean_whitespace_in_file(py_file):
            files_changed += 1
            print(f"Cleaned: {py_file}")
    
    print(f"\nProcessed {files_processed} files")
    print(f"Changed {files_changed} files")

if __name__ == '__main__':
    main()
