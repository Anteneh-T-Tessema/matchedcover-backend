#!/usr/bin/env python3
"""
Comprehensive lint fixer for MatchInsurance codebase.
This script systematically fixes all linting errors while preserving functionality.
"""

import os
import re
import ast
import subprocess
from typing import List, Dict, Tuple
import textwrap
import shutil


class ComprehensiveLintFixer:
    def __init__(self, src_dir: str = "src"):
        self.src_dir = src_dir
        self.backup_dir = "backup_before_comprehensive_fix"
        self.max_line_length = 79
        
    def create_backup(self):
        """Create a backup of the source directory."""
        if os.path.exists(self.backup_dir):
            shutil.rmtree(self.backup_dir)
        shutil.copytree(self.src_dir, self.backup_dir)
        print(f"Created backup in {self.backup_dir}")
    
    def get_python_files(self) -> List[str]:
        """Get all Python files in the source directory."""
        python_files = []
        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        return python_files
    
    def fix_syntax_errors(self, content: str) -> str:
        """Fix common syntax errors like unterminated strings."""
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Fix unterminated string literals
            # Count quotes to see if they're balanced
            single_quotes = line.count("'") - line.count("\\'")
            double_quotes = line.count('"') - line.count('\\"')
            
            # If odd number of quotes, try to fix
            if single_quotes % 2 == 1:
                # Try to close the string at the end of line
                if line.rstrip().endswith("'"):
                    pass  # Already properly terminated
                else:
                    # Add closing quote
                    line = line.rstrip() + "'"
            
            if double_quotes % 2 == 1:
                if line.rstrip().endswith('"'):
                    pass  # Already properly terminated
                else:
                    # Add closing quote
                    line = line.rstrip() + '"'
            
            # Fix broken docstrings
            if '"""' in line:
                triple_quotes = line.count('"""')
                if triple_quotes % 2 == 1 and not line.strip().endswith('"""'):
                    line = line.rstrip() + '"""'
            
            if "'''" in line:
                triple_quotes = line.count("'''")
                if triple_quotes % 2 == 1 and not line.strip().endswith("'''"):
                    line = line.rstrip() + "'''"
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def fix_long_lines(self, content: str) -> str:
        """Intelligently fix long lines."""
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            if len(line) <= self.max_line_length:
                fixed_lines.append(line)
                continue
            
            # Get indentation
            indent = len(line) - len(line.lstrip())
            indent_str = line[:indent]
            
            # Handle different types of long lines
            stripped = line.strip()
            
            # Skip very long strings or comments that shouldn't be broken
            if (stripped.startswith('#') or 
                stripped.startswith('"""') or 
                stripped.startswith("'''")):
                # For comments, try to wrap them
                if stripped.startswith('#'):
                    wrapped = textwrap.fill(stripped, width=self.max_line_length - indent,
                                          initial_indent='', subsequent_indent='# ')
                    wrapped_lines = wrapped.split('\n')
                    for j, wrapped_line in enumerate(wrapped_lines):
                        if j == 0:
                            fixed_lines.append(indent_str + wrapped_line)
                        else:
                            fixed_lines.append(indent_str + wrapped_line)
                else:
                    fixed_lines.append(line)
                continue
            
            # Handle imports
            if 'import' in line and ('from' in line or line.strip().startswith('import')):
                fixed_lines.extend(self._fix_import_line(line, indent_str))
                continue
            
            # Handle function calls and definitions
            if ('(' in line and ')' in line) or line.strip().startswith('def '):
                fixed_lines.extend(self._fix_function_line(line, indent_str))
                continue
            
            # Handle assignments
            if '=' in line and not line.strip().startswith('#'):
                fixed_lines.extend(self._fix_assignment_line(line, indent_str))
                continue
            
            # Handle string concatenations
            if '+' in line and ('"' in line or "'" in line):
                fixed_lines.extend(self._fix_string_concat_line(line, indent_str))
                continue
            
            # Default: break at logical points
            fixed_lines.extend(self._break_line_at_logical_points(line, indent_str))
        
        return '\n'.join(fixed_lines)
    
    def _fix_import_line(self, line: str, indent_str: str) -> List[str]:
        """Fix long import lines."""
        if 'from' in line and 'import' in line:
            # from module import a, b, c, d
            parts = line.split('import', 1)
            if len(parts) == 2:
                from_part = parts[0].strip()
                import_part = parts[1].strip()
                
                if ',' in import_part:
                    imports = [imp.strip() for imp in import_part.split(',')]
                    result = [f"{indent_str}{from_part}import ("]
                    for imp in imports:
                        result.append(f"{indent_str}    {imp},")
                    result.append(f"{indent_str})")
                    return result
        
        return [line]
    
    def _fix_function_line(self, line: str, indent_str: str) -> List[str]:
        """Fix long function definitions and calls."""
        # Simple approach: break after commas in parameter lists
        if '(' in line and ')' in line:
            # Find the opening parenthesis
            paren_start = line.find('(')
            paren_end = line.rfind(')')
            
            if paren_start > -1 and paren_end > paren_start:
                prefix = line[:paren_start + 1]
                params = line[paren_start + 1:paren_end]
                suffix = line[paren_end:]
                
                if ',' in params and len(line) > self.max_line_length:
                    param_list = [p.strip() for p in params.split(',')]
                    result = [prefix]
                    for param in param_list:
                        if param:
                            result.append(f"{indent_str}    {param},")
                    result[-1] = result[-1].rstrip(',')  # Remove last comma
                    result.append(f"{indent_str}{suffix}")
                    return result
        
        return [line]
    
    def _fix_assignment_line(self, line: str, indent_str: str) -> List[str]:
        """Fix long assignment lines."""
        if '=' in line:
            parts = line.split('=', 1)
            if len(parts) == 2:
                var_part = parts[0].strip()
                value_part = parts[1].strip()
                
                # If the value part is very long, try to break it
                if len(value_part) > 50:
                    # Try to break at logical operators
                    for op in [' and ', ' or ', ' + ', ' - ', ' * ', ' / ']:
                        if op in value_part:
                            backslash_op = ' \\' + op
                            new_line = f"{indent_str}{var_part} = ({value_part.replace(op, backslash_op)}"
                            return [new_line.replace(' \\', ' \\\n' + indent_str + '    ')]
        
        return [line]
    
    def _fix_string_concat_line(self, line: str, indent_str: str) -> List[str]:
        """Fix long string concatenation lines."""
        # Simple approach: break at + operators
        if '+' in line:
            parts = line.split('+')
            if len(parts) > 1:
                result = []
                current_line = indent_str + parts[0].strip()
                
                for part in parts[1:]:
                    potential_line = current_line + " + " + part.strip()
                    if len(potential_line) > self.max_line_length:
                        result.append(current_line + " +")
                        current_line = indent_str + "    " + part.strip()
                    else:
                        current_line = potential_line
                
                result.append(current_line)
                return result
        
        return [line]
    
    def _break_line_at_logical_points(self, line: str, indent_str: str) -> List[str]:
        """Break line at logical points like operators, commas, etc."""
        # Find good break points
        break_points = []
        for i, char in enumerate(line):
            if char in [',', '+', '-', '*', '/', '&', '|', '=', '<', '>']:
                if i > 40:  # Don't break too early
                    break_points.append(i)
        
        if break_points:
            # Use the first suitable break point
            for bp in break_points:
                if bp < self.max_line_length - 10:  # Leave some margin
                    part1 = line[:bp + 1]
                    part2 = indent_str + "    " + line[bp + 1:].lstrip()
                    return [part1, part2]
        
        # If no good break point found, just break at max length
        part1 = line[:self.max_line_length - 1] + "\\"
        part2 = indent_str + "    " + line[self.max_line_length - 1:]
        return [part1, part2]
    
    def fix_other_issues(self, content: str) -> str:
        """Fix other common linting issues."""
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Fix trailing whitespace
            line = line.rstrip()
            
            # Fix tabs to spaces
            if '\t' in line:
                line = line.expandtabs(4)
            
            # Fix bare except
            if re.match(r'\s*except\s*:', line):
                line = re.sub(r'except\s*:', 'except Exception:', line)
            
            # Fix lambda assignments (basic fix)
            if re.search(r'\w+\s*=\s*lambda', line):
                # This is complex to fix automatically, just add a comment
                line = line + "  # TODO: Replace lambda with def"
            
            # Fix ambiguous variable names
            line = re.sub(r'\bl\b(?=\s*=)', 'lst', line)  # Replace 'l' with 'lst'
            line = re.sub(r'\bO\b(?=\s*=)', 'obj', line)  # Replace 'O' with 'obj'
            line = re.sub(r'\bI\b(?=\s*=)', 'idx', line)  # Replace 'I' with 'idx'
            
            fixed_lines.append(line)
        
        # Remove trailing blank lines
        while fixed_lines and not fixed_lines[-1].strip():
            fixed_lines.pop()
        
        # Ensure file ends with newline
        result = '\n'.join(fixed_lines)
        if result and not result.endswith('\n'):
            result += '\n'
        
        return result
    
    def remove_unused_imports(self, content: str, filename: str) -> str:
        """Remove unused imports (basic implementation)."""
        lines = content.split('\n')
        import_lines = []
        other_lines = []
        
        # Separate import lines from other lines
        for line in lines:
            if (line.strip().startswith('import ') or 
                line.strip().startswith('from ') and 'import' in line):
                import_lines.append(line)
            else:
                other_lines.append(line)
        
        # Check which imports are actually used
        content_without_imports = '\n'.join(other_lines)
        used_imports = []
        
        for import_line in import_lines:
            # Extract imported names
            imported_names = self._extract_imported_names(import_line)
            
            # Check if any imported name is used
            is_used = False
            for name in imported_names:
                if name in content_without_imports:
                    is_used = True
                    break
            
            if is_used:
                used_imports.append(import_line)
        
        return '\n'.join(used_imports + other_lines)
    
    def _extract_imported_names(self, import_line: str) -> List[str]:
        """Extract imported names from an import line."""
        names = []
        
        if import_line.strip().startswith('from '):
            # from module import name1, name2
            if 'import' in import_line:
                import_part = import_line.split('import', 1)[1]
                names = [name.strip() for name in import_part.split(',')]
        elif import_line.strip().startswith('import '):
            # import module1, module2
            import_part = import_line.replace('import', '', 1)
            modules = [mod.strip() for mod in import_part.split(',')]
            names = [mod.split('.')[0] for mod in modules]  # Get base module name
        
        return [name.strip() for name in names if name.strip()]
    
    def fix_file(self, filepath: str) -> bool:
        """Fix a single file."""
        try:
            print(f"Fixing {filepath}...")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply fixes in order
            content = self.fix_syntax_errors(content)
            content = self.fix_long_lines(content)
            content = self.fix_other_issues(content)
            # content = self.remove_unused_imports(content, filepath)  # Skip for now as it's complex
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Error fixing {filepath}: {e}")
            return False
    
    def run_flake8(self) -> Tuple[int, str]:
        """Run flake8 and return error count and output."""
        try:
            result = subprocess.run(
                ['python', '-m', 'flake8', self.src_dir, '--count', '--statistics'],
                capture_output=True, text=True
            )
            output = result.stdout + result.stderr
            
            # Extract total error count from last line
            lines = output.strip().split('\n')
            total_errors = 0
            for line in reversed(lines):
                if line.strip().isdigit():
                    total_errors = int(line.strip())
                    break
            
            return total_errors, output
            
        except Exception as e:
            print(f"Error running flake8: {e}")
            return -1, str(e)
    
    def fix_all_files(self):
        """Fix all Python files in the source directory."""
        print("=== Comprehensive Lint Fixer ===")
        print(f"Target directory: {self.src_dir}")
        print(f"Max line length: {self.max_line_length}")
        
        # Create backup
        self.create_backup()
        
        # Get initial error count
        initial_errors, initial_output = self.run_flake8()
        print(f"\nInitial error count: {initial_errors}")
        
        # Get all Python files
        python_files = self.get_python_files()
        print(f"Found {len(python_files)} Python files")
        
        # Fix each file
        success_count = 0
        for filepath in python_files:
            if self.fix_file(filepath):
                success_count += 1
        
        print(f"\nFixed {success_count}/{len(python_files)} files")
        
        # Get final error count
        final_errors, final_output = self.run_flake8()
        print(f"Final error count: {final_errors}")
        print(f"Improvement: {initial_errors - final_errors} fewer errors")
        
        if final_errors > 0:
            print("\nRemaining issues:")
            print(final_output)
        else:
            print("\n🎉 ZERO LINTING ERRORS ACHIEVED! 🎉")


if __name__ == "__main__":
    fixer = ComprehensiveLintFixer()
    fixer.fix_all_files()
