
from typing import Union, Dict, Callable, Optional

from pe.actions import Action
from pe._constants import Flag
from pe._errors import Error
from pe._parser import Parser
from pe._grammar import Grammar
from pe._parse import loads

_FuncMap = Dict[str, Union[Action, Callable]]


def compile(source: Union[str, Grammar],
            actions: Optional[_FuncMap] = None,
            parser: str = 'packrat',
            flags: Flag = Flag.OPTIMIZE) -> Parser:
    """Compile the parsing expression or grammar in *source*."""
    parsername = parser.lower()
    if parsername == 'packrat':
        from pe.packrat import PackratParser as parser_class
    elif parsername == 'machine':
        from pe.machine import MachineParser as parser_class  # type: ignore
    elif parsername == 'machine-python':
        from pe._py_machine import MachineParser as parser_class  # type: ignore
    else:
        raise Error(f'unsupported parser: {parser}')

    if isinstance(source, Grammar):
        g = source
        if actions:
            raise Error('cannot assign actions to prepared grammar')
    else:
        assert isinstance(source, str)
        start, defmap = loads(source)
        g = Grammar(defmap, actions=actions, start=start)

    if flags & Flag.DEBUG:
        print('## Grammar ##')
        print(g)

    p = parser_class(g, flags=flags)

    if (flags & Flag.DEBUG) and (flags & Flag.OPTIMIZE):
        print('## Modified Grammar ##')
        print(p.modified_grammar)

    return p


def match(pattern: str,
          string: str,
          actions: Optional[_FuncMap] = None,
          parser: str = 'packrat',
          flags: Flag = Flag.MEMOIZE):
    """Compile *pattern* and match *string* against it.

    Example:
        >>> import pe
        >>> pe.match(r'"-"? [1-9] [0-9]*', '-12345').group()
        '-12345'
    """
    expr = compile(pattern,
                   actions=actions,
                   parser=parser,
                   flags=Flag.OPTIMIZE)
    return expr.match(string, flags=flags)
