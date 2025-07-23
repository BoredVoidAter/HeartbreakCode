
class GreatestHits:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def change_the_key(self, text, case_type):
        if not isinstance(text, str):
            raise Exception("Type error: 'Change The Key' expects a string for 'text'.")
        if not isinstance(case_type, str):
            raise Exception("Type error: 'Change The Key' expects a string for 'case_type'.")

        if case_type == "upper":
            return text.upper()
        elif case_type == "lower":
            return text.lower()
        elif case_type == "title":
            return text.title()
        else:
            raise Exception(f"Invalid case type: {case_type}. Expected 'upper', 'lower', or 'title'.")

    def calculate_the_score(self, num1, num2, operation):
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            raise Exception("Type error: 'Calculate The Score' expects numbers for 'num1' and 'num2'.")
        if not isinstance(operation, str):
            raise Exception("Type error: 'Calculate The Score' expects a string for 'operation'.")

        if operation == "add":
            return num1 + num2
        elif operation == "subtract":
            return num1 - num2
        elif operation == "multiply":
            return num1 * num2
        elif operation == "divide":
            if num2 == 0:
                raise Exception("Division by zero error in 'Calculate The Score'.")
            return num1 / num2
        else:
            raise Exception(f"Invalid operation: {operation}. Expected 'add', 'subtract', 'multiply', or 'divide'.")

    def rewrite_history(self, value, target_type):
        if not isinstance(target_type, str):
            raise Exception("Type error: 'Rewrite History' expects a string for 'target_type'.")

        if target_type == "string":
            return str(value)
        elif target_type == "number":
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    raise Exception(f"Cannot convert '{value}' to a number.")
        elif target_type == "boolean":
            if isinstance(value, str):
                if value.lower() in ("true", "yes", "1"):
                    return True
                elif value.lower() in ("false", "no", "0"):
                    return False
                else:
                    raise Exception(f"Cannot convert string '{value}' to boolean.")
            return bool(value)
        else:
            raise Exception(f"Invalid target type: {target_type}. Expected 'string', 'number', or 'boolean'.")
