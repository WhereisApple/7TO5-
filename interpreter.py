from parser import (
    Program, VariableDeclaration, VariableAssignment, PrintStatement,
    IfStatement, WhileLoop, FunctionDeclaration, ReturnStatement,
    CallExpression, BinaryExpression, UnaryExpression, Literal
)


class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise RuntimeError(f"Variable '{name}' does not exist")

    def set(self, name, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent is not None:
            self.parent.set(name, value)
            return
        self.values[name] = value

    def define(self, name, value):
        self.values[name] = value


class FunctionValue:
    def __init__(self, name, params, body, env):
        self.name = name
        self.params = params
        self.body = body
        self.env = env


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.env = self.global_env

    def run(self, program):
        if not isinstance(program, Program):
            raise RuntimeError("Expected a Program node")
        for statement in program.statements:
            self.execute(statement)

    def execute(self, statement):
        if isinstance(statement, VariableDeclaration):
            self.env.define(statement.name, self.evaluate(statement.value))
            return None

        if isinstance(statement, VariableAssignment):
            self.env.set(statement.name, self.evaluate(statement.value))
            return None

        if isinstance(statement, PrintStatement):
            value = self.evaluate(statement.value)
            print(value)
            return None

        if isinstance(statement, IfStatement):
            if self.is_truthy(self.evaluate(statement.condition)):
                return self.execute_block(statement.then_body)
            if statement.else_body is not None:
                return self.execute_block(statement.else_body)
            return None

        if isinstance(statement, WhileLoop):
            while self.is_truthy(self.evaluate(statement.condition)):
                self.execute_block(statement.body)
            return None

        if isinstance(statement, FunctionDeclaration):
            self.env.define(statement.name, FunctionValue(statement.name, statement.params, statement.body, self.env))
            return None

        if isinstance(statement, ReturnStatement):
            raise ReturnSignal(self.evaluate(statement.value))

        raise RuntimeError(f"Unknown statement: {statement}")

    def execute_block(self, statements):
        previous_env = self.env
        self.env = Environment(previous_env)
        try:
            for statement in statements:
                if isinstance(statement, ReturnStatement):
                    self.execute(statement)
                    break
                self.execute(statement)
            return None
        finally:
            self.env = previous_env

    def evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, str):
            return self.env.get(expression)

        if isinstance(expression, bool):
            return expression

        if isinstance(expression, (int, float)):
            return expression

        if isinstance(expression, CallExpression):
            func = self.evaluate(expression.name) if isinstance(expression.name, str) else self.evaluate(expression.name)
            if not isinstance(func, FunctionValue):
                raise RuntimeError(f"'{expression.name}' is not callable")

            args = [self.evaluate(arg) for arg in expression.arguments]
            previous_env = self.env
            self.env = Environment(func.env)
            try:
                for param_info, arg in zip(func.params, args):
                    param_name = param_info[0] if isinstance(param_info, tuple) else param_info
                    self.env.define(param_name, arg)
                for statement in func.body:
                    try:
                        self.execute(statement)
                    except ReturnSignal as signal:
                        self.env = previous_env
                        return signal.value
                self.env = previous_env
                return None
            finally:
                self.env = previous_env

        if isinstance(expression, BinaryExpression):
            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)
            op = expression.operator

            if op == "ADD":
                return left + right
            if op == "SUB":
                return left - right
            if op == "MUL":
                return left * right
            if op == "DIV":
                if right == 0:
                    raise RuntimeError("Cannot divide by zero")
                return left / right
            if op == "EQ":
                return left == right
            if op == "NEQ":
                return left != right
            if op == "GT":
                return left > right
            if op == "LT":
                return left < right
            if op == "GTE":
                return left >= right
            if op == "LTE":
                return left <= right
            if op == "AND":
                return self.is_truthy(left) and self.is_truthy(right)
            if op == "OR":
                return self.is_truthy(left) or self.is_truthy(right)
            raise RuntimeError(f"Unknown operator: {op}")

        if isinstance(expression, UnaryExpression):
            value = self.evaluate(expression.operand)
            if expression.operator == "NOT":
                return not self.is_truthy(value)
            if expression.operator == "NEGATE":
                return -value
            raise RuntimeError(f"Unknown unary operator: {expression.operator}")

        raise RuntimeError(f"Cannot evaluate: {expression}")

    def is_truthy(self, value):
        return bool(value)


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value