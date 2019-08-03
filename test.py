#! -*- coding:utf-8 -*-
#!/usr/bin/env python3

from collections import defaultdict

import compyl


def arggetter(n):
    return lambda *args: args[n]


def merge_dicts(d1, d2=None):
    if d2 is None:
        return d1

    for atom in d2:
        d1[atom] += d2[atom]

    return d1


def mul_dict(d, n):
    for atom in d:
        d[atom] *= int(n.value)

    return d


def atomic_dict(atom):
    return defaultdict(int, {atom.value: 1})


class Lexer(compyl.Lexer):
    ATOM = r'[A-Z][a-z]?'
    NUM = r'\d+'
    L_PA = r'\('
    R_PA = r'\)'
    L_SQ = r'\['
    R_SQ = r'\]'
    L_BR = r'\{'
    R_BR = r'\}'


class Parser(compyl.Parser, terminal='res'):
    res = 'molecule', dict

    molecule = ('component molecule?', merge_dicts)

    component =\
        ('L_PA molecule R_PA', arggetter(1)),\
        ('L_SQ molecule R_SQ', arggetter(1)),\
        ('L_BR molecule R_BR', arggetter(1)),\
        ('component NUM', mul_dict),\
        ('ATOM', atomic_dict)


_lexer = Lexer()
_parser = Parser()


def parse_molecule(formula):
    _lexer.read(formula)
    for tk in _lexer:
        _parser.parse(tk)
    return _parser.end()



if __name__ == "__main__":
    # molecula = "Mg(OH)2"
    # molecula = "K4[ON(SO3)2]2"
    molecula = "COOH{C(CH3)2}3CH3"
    # molecula = "H2O"

    my_dict = parse_molecule(molecula)

    print(my_dict)
