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
    | if_stat
    | while_stat
    | input_stat
    | print_stat
    ;

assignment_stat
    : ID '=' expression
    ;

if_stat
    : 'if' '(' condition ')' ':'
      (statements ';')?
      else_part
      'endif'
    ;

else_part
    : 'else' ':'
      (statements ';')?
    |
    ;

while_stat
    : 'while' '(' condition ')' ':'
      statements?
      'endwhile'
    ;

input_stat
    : 'input' ID
    ;

print_stat
    : 'print' expression (',' expression)*
    ;

condition
    : boolterm ('or' boolterm)*
    ;

boolterm
    : boolfactor ('and' boolfactor)*
    ;

boolfactor
    : 'not' '[' condition ']'
    | '[' condition ']'
    | expression rel_oper expression
    ;

rel_oper
    : '=='
    | '<='
    | '>='
    | '>'
    | '<'
    | '!='
    ;

expression
    : optional_sign term (add_oper term)*
    ;

optional_sign
    : add_oper
    |
    ;

term
    : factor (mul_oper factor)*
    ;

add_oper
    : '+'
    | '-'
    ;

mul_oper
    : '*'
    | '/'
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

COMMENTS
    : '#' ~[#]* '#' -> skip
    ;

WS
    : [ \t\r\n]+ -> skip
    ;