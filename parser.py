from lexer import (
    LET, NUM, STR, DECI, BE, SET, PRINT, IF, THEN, ELSE, END,
    WHILE, DO, FUNC, RETURN, CALL, TRUE, FALSE, AND, OR, NOT,
    EQ, NEQ, GT, LT, GTE, LTE, ADD, SUB, MUL, DIV, ASSIGN,
    LPAREN, RPAREN, LBRACE, RBRACE, COMMA, IDENTIFIER, INTEGER,
    DECIMAL, STRING, EOF
)


class Program:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"


class VariableDeclaration:
    def __init__(self, name, var_type, value):
        self.name = name
        self.var_type = var_type
        self.value = value

    def __repr__(self):
        return f"VariableDeclaration(name={self.name}, type={self.var_type}, value={self.value})"


class VariableAssignment:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"VariableAssignment(name={self.name}, value={self.value})"


class PrintStatement:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Print({self.value})"


class IfStatement:
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

    def __repr__(self):
        return f"If({self.condition}, {self.then_body}, {self.else_body})"


class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"While({self.condition}, {self.body})"


class FunctionDeclaration:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDeclaration({self.name}, {self.params}, {self.body})"


class ReturnStatement:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"


class CallExpression:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"Call({self.name}, {self.arguments})"


class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.right = right
        self.operator = operator

    def __repr__(self):
        return f"BinaryExpression({self.left}, {self.operator}, {self.right})"


class UnaryExpression:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryExpression({self.operator}, {self.operand})"


class Literal:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Literal({self.value})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def peek(self, offset=1):
        index = self.position + offset
        if index < len(self.tokens):
            return self.tokens[index]
        return self.tokens[-1]

    def eat(self, expected_type=None):
        token = self.current()
        if expected_type is not None and token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, but got {token.type}")
        self.position += 1
        return token

    def parse(self):
        statements = []
        while self.current().type != EOF:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        if self.current().type == LET:
            return self.parse_declaration()
        if self.current().type == SET:
            return self.parse_assignment()
        if self.current().type == PRINT:
            return self.parse_print()
        if self.current().type == IF:
            return self.parse_if()
        if self.current().type == WHILE:
            return self.parse_while()
        if self.current().type == FUNC:
            return self.parse_function()
        if self.current().type == RETURN:
            return self.parse_return()
        raise SyntaxError(f"Unexpected token: {self.current()}")

    def parse_declaration(self):
        self.eat(LET)
        var_type = None

        if self.current().type == NUM:
            var_type = "num"
            self.eat(NUM)
        elif self.current().type == STR:
            var_type = "str"
            self.eat(STR)
        elif self.current().type == DECI:
            var_type = "deci"
            self.eat(DECI)
        else:
            raise SyntaxError(f"Expected type, got {self.current()}")

        name = self.eat(IDENTIFIER).value
        self.eat(BE)
        value = self.parse_expression()
        return VariableDeclaration(name, var_type, value)

    def parse_assignment(self):
        self.eat(SET)
        name = self.eat(IDENTIFIER).value
        self.eat(ASSIGN)
        value = self.parse_expression()
        return VariableAssignment(name, value)

    def parse_print(self):
        self.eat(PRINT)
        value = self.parse_expression()
        return PrintStatement(value)

    def parse_if(self):
        self.eat(IF)
        condition = self.parse_expression()
        self.eat(THEN)
        then_body = self.parse_block()
        else_body = None
        if self.current().type == ELSE:
            self.eat(ELSE)
            else_body = self.parse_block()
        self.eat(END)
        return IfStatement(condition, then_body, else_body)

    def parse_while(self):
        self.eat(WHILE)
        condition = self.parse_expression()
        self.eat(DO)
        body = self.parse_block()
        self.eat(END)
        return WhileLoop(condition, body)

    def parse_function(self):
        self.eat(FUNC)
        name = self.eat(IDENTIFIER).value
        self.eat(LPAREN)
        params = []
        if self.current().type != RPAREN:
            param_type = self.current().type
            if param_type in (NUM, STR, DECI):
                self.eat(param_type)
                params.append((self.eat(IDENTIFIER).value, param_type))
            else:
                params.append((self.eat(IDENTIFIER).value, None))
            while self.current().type == COMMA:
                self.eat(COMMA)
                next_type = self.current().type
                if next_type in (NUM, STR, DECI):
                    self.eat(next_type)
                    params.append((self.eat(IDENTIFIER).value, next_type))
                else:
                    params.append((self.eat(IDENTIFIER).value, None))
        self.eat(RPAREN)
        body = self.parse_block()
        self.eat(END)
        return FunctionDeclaration(name, params, body)

    def parse_return(self):
        self.eat(RETURN)
        value = self.parse_expression()
        return ReturnStatement(value)

    def parse_block(self):
        statements = []
        self.eat(LBRACE)
        while self.current().type != RBRACE:
            if self.current().type == EOF:
                raise SyntaxError("Missing closing brace")
            statements.append(self.parse_statement())
        self.eat(RBRACE)
        return statements

    def parse_expression(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.current().type == OR:
            self.eat(OR)
            right = self.parse_and()
            left = BinaryExpression(left, "OR", right)
        return left

    def parse_and(self):
        left = self.parse_equality()
        while self.current().type == AND:
            self.eat(AND)
            right = self.parse_equality()
            left = BinaryExpression(left, "AND", right)
        return left

    def parse_equality(self):
        left = self.parse_relational()
        while self.current().type in (EQ, NEQ):
            op = self.current().type
            self.eat(op)
            right = self.parse_relational()
            left = BinaryExpression(left, op, right)
        return left

    def parse_relational(self):
        left = self.parse_additive()
        while self.current().type in (LT, GT, LTE, GTE):
            op = self.current().type
            self.eat(op)
            right = self.parse_additive()
            left = BinaryExpression(left, op, right)
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.current().type in (ADD, SUB):
            op = self.current().type
            self.eat(op)
            right = self.parse_multiplicative()
            left = BinaryExpression(left, op, right)
        return left

    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.current().type in (MUL, DIV):
            op = self.current().type
            self.eat(op)
            right = self.parse_unary()
            left = BinaryExpression(left, op, right)
        return left

    def parse_unary(self):
        if self.current().type == NOT:
            self.eat(NOT)
            return UnaryExpression("NOT", self.parse_unary())
        if self.current().type == SUB:
            self.eat(SUB)
            return UnaryExpression("NEGATE", self.parse_unary())
        return self.parse_primary()

    def parse_primary(self):
        token = self.current()

        if token.type in (ADD, SUB, MUL, DIV):
            operator = self.eat(token.type).type
            left = self.parse_primary()
            self.eat(AND)
            right = self.parse_primary()
            return BinaryExpression(left, operator, right)

        if token.type == CALL:
            self.eat(CALL)
            name = self.eat(IDENTIFIER).value
            self.eat(LPAREN)
            args = []
            if self.current().type != RPAREN:
                args.append(self.parse_expression())
                while self.current().type == COMMA:
                    self.eat(COMMA)
                    args.append(self.parse_expression())
            self.eat(RPAREN)
            return CallExpression(name, args)

        if token.type == INTEGER:
            self.eat(INTEGER)
            return Literal(token.value)
        if token.type == DECIMAL:
            self.eat(DECIMAL)
            return Literal(token.value)
        if token.type == STRING:
            self.eat(STRING)
            return Literal(token.value)
        if token.type == TRUE:
            self.eat(TRUE)
            return Literal(True)
        if token.type == FALSE:
            self.eat(FALSE)
            return Literal(False)
        if token.type == IDENTIFIER:
            name = self.eat(IDENTIFIER).value
            if self.current().type == LPAREN:
                self.eat(LPAREN)
                args = []
                if self.current().type != RPAREN:
                    args.append(self.parse_expression())
                    while self.current().type == COMMA:
                        self.eat(COMMA)
                        args.append(self.parse_expression())
                self.eat(RPAREN)
                return CallExpression(name, args)
            return name
        if token.type == LPAREN:
            self.eat(LPAREN)
            value = self.parse_expression()
            self.eat(RPAREN)
            return value

        raise SyntaxError(f"Unexpected token in expression: {token}")