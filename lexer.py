LET = "LET"
NUM = "NUM"
STR = "STR"
DECI = "DECI"
BE = "BE"
SET = "SET"
PRINT = "PRINT"
IF = "IF"
THEN = "THEN"
ELSE = "ELSE"
END = "END"
WHILE = "WHILE"
DO = "DO"
FUNC = "FUNC"
RETURN = "RETURN"
CALL = "CALL"
TRUE = "TRUE"
FALSE = "FALSE"
AND = "AND"
OR = "OR"
NOT = "NOT"
EQ = "EQ"
NEQ = "NEQ"
GT = "GT"
LT = "LT"
GTE = "GTE"
LTE = "LTE"
ADD = "ADD"
SUB = "SUB"
MUL = "MUL"
DIV = "DIV"
ASSIGN = "ASSIGN"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
LBRACE = "LBRACE"
RBRACE = "RBRACE"
COMMA = "COMMA"
IDENTIFIER = "IDENTIFIER"
INTEGER = "INTEGER"
DECIMAL = "DECIMAL"
STRING = "STRING"
EOF = "EOF"


class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


KEYWORDS = {
    "let": LET,
    "num": NUM,
    "str": STR,
    "deci": DECI,
    "be": BE,
    "set": SET,
    "print": PRINT,
    "if": IF,
    "then": THEN,
    "else": ELSE,
    "end": END,
    "while": WHILE,
    "do": DO,
    "func": FUNC,
    "return": RETURN,
    "call": CALL,
    "true": TRUE,
    "false": FALSE,
    "and": AND,
    "or": OR,
    "not": NOT,
    "eq": EQ,
    "neq": NEQ,
    "gt": GT,
    "lt": LT,
    "gte": GTE,
    "lte": LTE,
    "add": ADD,
    "sub": SUB,
    "mul": MUL,
    "div": DIV,
}


def tokenize(source):
    tokens = []
    i = 0

    while i < len(source):
        char = source[i]

        if char.isspace():
            i += 1
            continue

        if char == '"':
            i += 1
            start = i
            while i < len(source) and source[i] != '"':
                i += 1

            if i >= len(source):
                raise SyntaxError("Unterminated string literal")

            value = source[start:i]
            i += 1
            tokens.append(Token(STRING, value))
            continue

        if char.isdigit():
            start = i
            decimal_found = False
            while i < len(source):
                if source[i].isdigit():
                    i += 1
                elif source[i] == "." and not decimal_found:
                    decimal_found = True
                    i += 1
                else:
                    break

            number = source[start:i]
            if decimal_found:
                tokens.append(Token(DECIMAL, float(number)))
            else:
                tokens.append(Token(INTEGER, int(number)))
            continue

        if char.isalpha() or char == "_":
            start = i
            while i < len(source) and (source[i].isalnum() or source[i] == "_"):
                i += 1

            word = source[start:i]
            tokens.append(
                Token(KEYWORDS.get(word, IDENTIFIER), word if word not in KEYWORDS else None)
            )
            continue

        if source.startswith("==", i):
            tokens.append(Token(EQ))
            i += 2
            continue

        if source.startswith("!=", i):
            tokens.append(Token(NEQ))
            i += 2
            continue

        if source.startswith("<=", i):
            tokens.append(Token(LTE))
            i += 2
            continue

        if source.startswith(">=", i):
            tokens.append(Token(GTE))
            i += 2
            continue

        if char == "=":
            tokens.append(Token(ASSIGN))
            i += 1
            continue

        if char == "<":
            tokens.append(Token(LT))
            i += 1
            continue

        if char == ">":
            tokens.append(Token(GT))
            i += 1
            continue

        if char == "+":
            tokens.append(Token(ADD))
            i += 1
            continue

        if char == "-":
            tokens.append(Token(SUB))
            i += 1
            continue

        if char == "*":
            tokens.append(Token(MUL))
            i += 1
            continue

        if char == "/":
            tokens.append(Token(DIV))
            i += 1
            continue

        if char == "(":
            tokens.append(Token(LPAREN))
            i += 1
            continue

        if char == ")":
            tokens.append(Token(RPAREN))
            i += 1
            continue

        if char == "{":
            tokens.append(Token(LBRACE))
            i += 1
            continue

        if char == "}":
            tokens.append(Token(RBRACE))
            i += 1
            continue

        if char == ",":
            tokens.append(Token(COMMA))
            i += 1
            continue

        raise SyntaxError(f"Unknown character: {char}")

    tokens.append(Token(EOF))
    return tokens