import re

class TsxValidator:
    @staticmethod
    def validate(code: str, filename: str = "<unknown>"):
        # 1. Structural check for export default function
        if not re.search(r"export\s+default\s+function\s+[A-Za-z0-9_]+\s*\(", code) and \
           not re.search(r"export\s+default\s+[A-Za-z0-9_]+", code):
            return False, f"Structural Error in {filename}: Missing 'export default function' or default export."
            
        # 2. Simple brace balancing (ignores strings/comments for this basic compiler pass)
        stack = []
        pairs = {
            '{': '}',
            '[': ']',
            '(': ')'
        }
        closing = set(pairs.values())
        
        # Strip simple string literals to avoid false positives (very naive implementation)
        clean_code = re.sub(r'\'[^\']*\'', "''", code)
        clean_code = re.sub(r'\"[^\"]*\"', '""', clean_code)
        
        for i, char in enumerate(clean_code):
            if char in pairs:
                stack.append(char)
            elif char in closing:
                if not stack:
                    return False, f"Syntax Error in {filename}: Unmatched closing brace '{char}' at index {i}"
                last = stack.pop()
                if pairs[last] != char:
                    return False, f"Syntax Error in {filename}: Mismatched brace '{char}', expected '{pairs[last]}'"
                    
        if stack:
            return False, f"Syntax Error in {filename}: Unclosed brace '{stack[-1]}'"
            
        return True, None
