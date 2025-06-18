#!/usr/bin/env python3
"""
Advanced automatic line breaking script to fix ALL E501 issues.
This script intelligently breaks long lines while preserving code functionality.
"""

import re
import ast
import textwrap
from pathlib import Path
from typing import List, Tuple, Optional


class IntelligentLineBreaker:
    """Advanced line breaker that understands Python syntax"""
    
    def __init__(self, max_line_length: int = 79):
        self.max_line_length = max_line_length
        
    def break_long_lines(self, content: str) -> str:
        """Break long lines intelligently"""
        lines = content.splitlines()
        result_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            if len(line) <= self.max_line_length:
                result_lines.append(line)
                i += 1
                continue
                
            # Try different strategies to break the line
            broken_lines = self._break_line_smart(line)
            
            if broken_lines:
                result_lines.extend(broken_lines)
            else:
                # Fallback: keep original line if we can't break it safely
                result_lines.append(line)
            
            i += 1
        
        return '\n'.join(result_lines) + ('\n' if content.endswith('\n') else '')
    
    def _break_line_smart(self, line: str) -> Optional[List[str]]:
        """Intelligently break a line using multiple strategies"""
        
        # Strategy 1: Function definitions
        if self._is_function_definition(line):
            return self._break_function_definition(line)
        
        # Strategy 2: Function calls
        if self._is_function_call(line):
            return self._break_function_call(line)
        
        # Strategy 3: String literals
        if self._has_long_string(line):
            return self._break_string_literal(line)
        
        # Strategy 4: Import statements
        if line.strip().startswith(('from ', 'import ')):
            return self._break_import_statement(line)
        
        # Strategy 5: Dictionary/list literals
        if self._has_dict_or_list(line):
            return self._break_dict_or_list(line)
        
        # Strategy 6: Conditional expressions
        if self._is_conditional(line):
            return self._break_conditional(line)
        
        # Strategy 7: Mathematical expressions
        if self._has_math_operators(line):
            return self._break_math_expression(line)
        
        # Strategy 8: Comments
        if '#' in line:
            return self._break_with_comment(line)
        
        # Strategy 9: Generic line breaking at operators
        return self._break_at_operators(line)
    
    def _is_function_definition(self, line: str) -> bool:
        """Check if line is a function definition"""
        stripped = line.strip()
        return (stripped.startswith('def ') or stripped.startswith('async def ')) and ':' in line
    
    def _break_function_definition(self, line: str) -> List[str]:
        """Break function definition across multiple lines"""
        indent = self._get_indent(line)
        
        # Find the function signature
        if '(' in line and ')' in line:
            func_start = line[:line.find('(') + 1]
            params_and_end = line[line.find('(') + 1:]
            
            closing_paren = params_and_end.rfind(')')
            params = params_and_end[:closing_paren]
            func_end = params_and_end[closing_paren:]
            
            if ',' in params:
                # Break parameters across lines
                param_list = [p.strip() for p in params.split(',') if p.strip()]
                
                result = [func_start]
                for i, param in enumerate(param_list):
                    if i == len(param_list) - 1:
                        result.append(f'{indent}    {param}')
                    else:
                        result.append(f'{indent}    {param},')
                result.append(f'{indent}{func_end}')
                return result
        
        return None
    
    def _is_function_call(self, line: str) -> bool:
        """Check if line contains a function call"""
        return '(' in line and ')' in line and not self._is_function_definition(line)
    
    def _break_function_call(self, line: str) -> List[str]:
        """Break function call across multiple lines"""
        indent = self._get_indent(line)
        
        # Find the function call pattern
        match = re.search(r'(.+?)(\([^)]+\))(.*)', line)
        if match:
            before_call, call_part, after_call = match.groups()
            
            # Extract parameters
            params = call_part[1:-1]  # Remove parentheses
            if ',' in params and len(call_part) > 40:
                param_list = [p.strip() for p in params.split(',') if p.strip()]
                
                if len(param_list) > 1:
                    result = [f'{before_call}(']
                    for i, param in enumerate(param_list):
                        if i == len(param_list) - 1:
                            result.append(f'{indent}    {param}')
                        else:
                            result.append(f'{indent}    {param},')
                    result.append(f'{indent}){after_call}')
                    return result
        
        return None
    
    def _has_long_string(self, line: str) -> bool:
        """Check if line has a long string literal"""
        return ('"' in line or "'" in line) and len(line) > self.max_line_length
    
    def _break_string_literal(self, line: str) -> List[str]:
        """Break long string literals"""
        indent = self._get_indent(line)
        
        # Find string assignments
        match = re.match(r'^(\s*)(\w+\s*=\s*)["\']([^"\']+)["\'](.*)$', line)
        if match:
            leading, assignment, string_content, trailing = match.groups()
            
            if len(string_content) > 50:
                # Break string into parts
                words = string_content.split()
                chunks = []
                current_chunk = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 > 45:  # Leave room for quotes
                        if current_chunk:
                            chunks.append(' '.join(current_chunk))
                            current_chunk = [word]
                            current_length = len(word)
                        else:
                            chunks.append(word)
                    else:
                        current_chunk.append(word)
                        current_length += len(word) + 1
                
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                
                if len(chunks) > 1:
                    result = [f'{leading}{assignment}(']
                    for i, chunk in enumerate(chunks):
                        if i == len(chunks) - 1:
                            result.append(f'{indent}    "{chunk}"{trailing}')
                        else:
                            result.append(f'{indent}    "{chunk} "')
                    result.append(f'{indent})')
                    return result
        
        return None
    
    def _break_import_statement(self, line: str) -> List[str]:
        """Break long import statements"""
        indent = self._get_indent(line)
        
        if line.strip().startswith('from ') and ' import ' in line:
            parts = line.split(' import ', 1)
            if len(parts) == 2:
                from_part, import_part = parts
                
                if ',' in import_part:
                    imports = [imp.strip() for imp in import_part.split(',')]
                    if len(imports) > 2:
                        result = [f'{from_part} import (']
                        for i, imp in enumerate(imports):
                            if i == len(imports) - 1:
                                result.append(f'{indent}    {imp}')
                            else:
                                result.append(f'{indent}    {imp},')
                        result.append(f'{indent})')
                        return result
        
        return None
    
    def _has_dict_or_list(self, line: str) -> bool:
        """Check if line has dictionary or list literals"""
        return ('{' in line and '}' in line) or ('[' in line and ']' in line)
    
    def _break_dict_or_list(self, line: str) -> List[str]:
        """Break dictionary or list literals"""
        indent = self._get_indent(line)
        
        # Simple dictionary breaking
        if '{' in line and '}' in line and ',' in line:
            # Find the dictionary content
            start_brace = line.find('{')
            end_brace = line.rfind('}')
            
            if start_brace != -1 and end_brace != -1:
                before = line[:start_brace + 1]
                content = line[start_brace + 1:end_brace]
                after = line[end_brace:]
                
                if ',' in content and len(content) > 40:
                    items = [item.strip() for item in content.split(',') if item.strip()]
                    if len(items) > 1:
                        result = [before]
                        for i, item in enumerate(items):
                            if i == len(items) - 1:
                                result.append(f'{indent}    {item}')
                            else:
                                result.append(f'{indent}    {item},')
                        result.append(f'{indent}{after}')
                        return result
        
        return None
    
    def _is_conditional(self, line: str) -> bool:
        """Check if line is a conditional statement"""
        stripped = line.strip()
        return (stripped.startswith('if ') or ' if ' in stripped or 
                stripped.startswith('elif ') or stripped.startswith('while '))
    
    def _break_conditional(self, line: str) -> List[str]:
        """Break conditional statements"""
        indent = self._get_indent(line)
        
        # Break on logical operators
        for op in [' and ', ' or ']:
            if op in line:
                parts = line.split(op, 1)
                if len(parts) == 2 and len(parts[0]) > 30:
                    return [
                        f'{parts[0]} {op.strip()}',
                        f'{indent}    {parts[1]}'
                    ]
        
        return None
    
    def _has_math_operators(self, line: str) -> bool:
        """Check if line has mathematical operators"""
        return any(op in line for op in [' + ', ' - ', ' * ', ' / ', ' ** ', ' // ', ' % '])
    
    def _break_math_expression(self, line: str) -> List[str]:
        """Break mathematical expressions"""
        indent = self._get_indent(line)
        
        # Break at mathematical operators
        for op in [' + ', ' - ', ' * ', ' / ']:
            if op in line:
                parts = line.split(op, 1)
                if len(parts) == 2 and len(parts[0]) > 40:
                    return [
                        f'{parts[0]} {op.strip()}',
                        f'{indent}    {parts[1]}'
                    ]
        
        return None
    
    def _break_with_comment(self, line: str) -> List[str]:
        """Break line with comments"""
        if '#' in line:
            code_part, comment_part = line.split('#', 1)
            code_part = code_part.rstrip()
            comment_part = comment_part.strip()
            
            if len(code_part) > self.max_line_length - 10:
                # Try to break the code part
                broken_code = self._break_line_smart(code_part)
                if broken_code:
                    # Add comment to last line
                    broken_code[-1] += f'  # {comment_part}'
                    return broken_code
        
        return None
    
    def _break_at_operators(self, line: str) -> List[str]:
        """Generic line breaking at various operators"""
        indent = self._get_indent(line)
        
        # Try breaking at various operators
        operators = [' = ', ' == ', ' != ', ' <= ', ' >= ', ' < ', ' > ', 
                    ' in ', ' not in ', ' is ', ' is not ']
        
        for op in operators:
            if op in line:
                parts = line.split(op, 1)
                if len(parts) == 2 and len(parts[0]) > 30:
                    return [
                        f'{parts[0]} {op.strip()}',
                        f'{indent}    {parts[1]}'
                    ]
        
        # Try breaking at commas in function calls or lists
        if ',' in line and ('(' in line or '[' in line):
            # Find a good comma to break at
            for i, char in enumerate(line):
                if char == ',' and i > 40:
                    return [
                        line[:i + 1],
                        f'{indent}    {line[i + 1:].lstrip()}'
                    ]
        
        return None
    
    def _get_indent(self, line: str) -> str:
        """Get the indentation of a line"""
        return line[:len(line) - len(line.lstrip())]


def fix_file(file_path: Path) -> bool:
    """Fix E501 issues in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        breaker = IntelligentLineBreaker()
        fixed_content = breaker.break_long_lines(original_content)
        
        if fixed_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Fix all E501 issues in the codebase"""
    src_dir = Path('src')
    if not src_dir.exists():
        print("src/ directory not found")
        return
    
    files_processed = 0
    files_changed = 0
    
    print("🚀 Starting intelligent line breaking...")
    
    for py_file in src_dir.rglob('*.py'):
        files_processed += 1
        if fix_file(py_file):
            files_changed += 1
            print(f"✅ Fixed long lines in: {py_file}")
    
    print(f"\n📊 Summary:")
    print(f"   Files processed: {files_processed}")
    print(f"   Files changed: {files_changed}")
    print(f"🎯 Intelligent line breaking complete!")


if __name__ == '__main__':
    main()
