grammar oos;

startRule
    : class_main_def EOF
    ;

class_main_def
    : 'class' ('main' | 'Main') ':'
      main_body
    ;

main_body
    : 'def' 'main' '(' 'self' ')' ':' '-'
      declarations
      statements?
      ';' ';'
    ;

declarations
    : (decl_line (';' decl_line)* ';' ';')?
    ;

decl_line
    : 'int' ID (',' ID)*
    ;

statements
    : statement (';' statement)*
    ;

statement
    : assignment_stat
    | print_stat
    ;

assignment_stat
    : ID '=' expression
    ;

print_stat
    : 'print' expression (',' expression)*
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
    | ID
    ;

INTEGER
    : [1-9] [0-9]*
    | '0'+
    ;

ID
    : [A-Za-z] [A-Za-z0-9_]*
    ;

WS
    : [ \t\r\n]+ -> skip
    ;