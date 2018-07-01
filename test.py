#! -*- coding:utf-8 -*-
#!/usr/bin/env python3


from compyl.lexer import Lexer
import re

lrules = [
    (r"([A-Z][a-z]?)(\d+)?", "ATOM"),
    (r"\(", "L_DEL"),
    (r"(\))(\d+)?", "R_DEL"),

]

lexer = Lexer(rules=lrules)
lexer.set_line_rule("\n")
lexer.build()


def use_only_known_dels(molecula):
    replacements = [
        ('\]', ')'),
        ('\}', ')'),
        ('\[', '('),
        ('\{', '('),
    ]
    for old, new in replacements:
        molecula = re.sub(old, new, molecula)

    return molecula


def find_matching_del(s):
    pairs = []
    stack = []

    for i, token in enumerate(s):
        if token == '(':
            stack.append(i)
        elif token == ')':
            if len(stack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            pairs.append((stack.pop(), i))

    if len(stack) > 0:
        raise IndexError("No matching opening parens at: " + str(stack.pop()))

    return pairs


def reduce_string(tokens):
    reduced_string = ""
    coef = re.search("\)(?P<num>\d+)?", tokens[-1].value).group("num")
    while tokens:
        token = tokens.pop(0)
        if token.type == "ATOM":
            atom = re.search("(?P<name>[A-Z][a-z]?)(?P<num>\d+)?", token.value).group("name")
            coef1 = re.search("(?P<name>[A-Z][a-z]?)(?P<num>\d+)?", token.value).group("num")
            if coef1 is None: coef1 = 1
            reduced_string += str(atom) + str(int(coef1) * int(coef))

    return reduced_string


def create_tokens(chain):
    tokens = []
    lexer.read(chain)
    tk = lexer.lex()

    while tk:
        tokens.append(tk)
        tk = lexer.lex()
    return tokens


def transform(molecula):
    pairs = find_matching_del(molecula)

    if pairs:
        pair = pairs.pop(0)

        sub = molecula[pair[0]:pair[1]+2]
        red = reduce_string(create_tokens(sub))
        new_molecula = molecula.replace(sub, red)

        if '(' in new_molecula:
            return transform(new_molecula)
        else:
            return new_molecula
    else:
        return molecula


def create_dict(tokens):
    adict = {}
    for token in tokens:
        if token.type == "ATOM":
            atom = re.search("(?P<name>[A-Z][a-z]?)(?P<num>\d+)?", token.value).group("name")
            coef = re.search("(?P<name>[A-Z][a-z]?)(?P<num>\d+)?", token.value).group("num")
            if coef is None: coef = 1
            adict[atom] = adict.get(atom, 0) + int(coef)
    return adict


if __name__ == "__main__":
    # molecula = "Mg(OH)2"
    # molecula = "K4[ON(SO3)2]2"
    molecula = "COOH{C(CH3)2}3CH3"
    # molecula = "H20"

    print(molecula)
    molecula = use_only_known_dels(molecula)

    my_molecula = transform(molecula)
    print(my_molecula)

    my_tokens = create_tokens(my_molecula)
    my_dict = create_dict(my_tokens)

    print(my_dict)
