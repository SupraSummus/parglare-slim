# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from parglare import Parser, Grammar
from parglare.exceptions import ParseError
from .expression_grammar import get_grammar


def test_default_whitespaces():

    grammar = get_grammar()
    p = Parser(grammar)

    p.parse("""id+  id * (id
    +id  )
    """)


def test_whitespace_redefinition():

    grammar = get_grammar()

    # Make newline treated as non-ws characted
    p = Parser(grammar, ws=' \t')

    p.parse("""id+  id * (id +id  ) """)

    try:
        p.parse("""id+  id * (id
        +id  )
        """)
    except ParseError as e:
        assert e.location.start_position == 13


def test_whitespace_not_used_if_layout():
    """
    If LAYOUT rule is used, ws definition is ignored.
    """
    g, _ = Grammar.from_struct(
        {
            'S': [['a', 'b']],
            'LAYOUT': [['k'], []],
        },
        {s: ('string', s) for s in ['a', 'b', 'k']},
        'S',
    )
    parser = Parser(g)
    with pytest.raises(ParseError):
        parser.parse('a b')
