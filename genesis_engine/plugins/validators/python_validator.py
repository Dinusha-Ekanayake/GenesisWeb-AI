import ast

class PythonValidator:
    @staticmethod
    def validate(code: str, filename: str = "<unknown>"):
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            error_msg = f"Syntax error in {filename} at line {e.lineno}: {e.msg}\n{e.text}"
            return False, error_msg
        except Exception as e:
            return False, f"Unexpected error parsing {filename}: {str(e)}"
