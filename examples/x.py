

import pe
from pe.constants import Flag
from pe.actions import join, pack

X = pe.compile(
    r'''
    Start   <- Expr EOL? EOF
    Expr    <- Term PLUS Expr
             / (Sign Sign)+ Term MINUS Expr
             / Term
    Sign    <- [-+] :Spacing
    Term    <- Factor TIMES Term
             / Factor DIVIDE Term
             / Factor
    Factor  <- LPAREN Expr RPAREN
             / Atom
    Atom    <- NAME / NUMBER
    NAME    <- [a-bA-B_] [a-bA-B0-9_]* :Spacing
    NUMBER  <- '0' / [1-9] [0-9]* :Spacing
    PLUS    <- '+' :Spacing
    MINUS   <- '-' :Spacing
    TIMES   <- '*' :Spacing
    DIVIDE  <- '/' :Spacing
    LPAREN  <- '(' :Spacing
    RPAREN  <- ')' :Spacing
    EOL     <- '\r\n' / [\n\r]
    EOF     <- !.
    Spacing <- ' '*
    ''',
    flags=Flag.OPTIMIZE)

if __name__ == '__main__':
    import sys
    print(0, end='')
    for i, line in enumerate(open(sys.argv[1]), 1):
        print(f'\r{i}', end='')
        X.match(line, flags=Flag.STRICT|Flag.MEMOIZE)
    print('done')
