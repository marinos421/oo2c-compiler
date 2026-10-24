grammar oos;

startRule
    : 'class' 'Main' ':'
      'def' 'main' '(' 'self' ')' ':' '-'
      printStatement ';' ';'
      EOF
    ;

printStatement
    : 'print' expression
    ;

expression
    : ('+' | '-')? term (('+' | '-') term)*
    ;

term
    : factor (('*' | '/') factor)*
    ;

factor
    : INTEGER
    | '(' expression ')'
    ;

INTEGER
    : [0-9]+
    ;

WS
    : [ \t\r\n]+ -> skip
    ;