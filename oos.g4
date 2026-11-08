grammar oos;

startRule
    : classes
    ;

classes
    : class_def*
      class_main_def
      EOF
    ;

class_def
    : 'class' class_name
      ('(' class_name (',' class_name)* ')')?
      ':'
      declarations
      class_body
    ;

class_main_def
    : 'class' ('main' | 'Main') ':'
      declarations
      main_body
    ;

class_name
    : ID
    ;

class_body
    : (constructor_def ';' ';')+
      (method_def ';' ';')*
    ;

main_body
    : method_main_def ';' ';'
    ;

constructor_def
    : 'def' '__init__' parameters ':' class_name
      method_body
    ;

method_def
    : 'def' ID parameters ':' return_type
      method_body
    ;

method_main_def
    : 'def' 'main' '(' 'self' ')' ':' '-'
      method_body
    ;

method_body
    : declarations
      statements?
    ;

return_type
    : types
    | '-'
    ;

types
    : class_name
    | 'int'
    ;

parameters
    : '(' parlist ')'
    ;

parlist
    : 'self' (',' types ID)*
    ;

declarations
    : (decl_line (';' decl_line)* ';' ';')?
    ;

decl_line
    : types ID (',' ID)*
    ;

statements
    : statement (';' statement)*
    ;

statement
    : assignment_stat
    | direct_call_stat
    | if_stat
    | while_stat
    | return_stat
    | input_stat
    | print_stat
    ;

assignment_stat
    : assign_target '=' expression
    ;

assign_target
    : ('self' '.')? ID
    | ID '.' ID
    ;

direct_call_stat
    : object_method_call
    | ('self' '.')? func_call
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

return_stat
    : 'return' expression
    ;

input_stat
    : 'input' assign_target
    ;

print_stat
    : 'print' expression (',' expression)*
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

factor
    : INTEGER
    | '(' expression ')'
    | object_method_call
    | ('self' '.')? func_call
    | reference
    ;

reference
    : 'self'
    | 'self' '.' ID
    | ID '.' ID
    | ID
    ;

object_method_call
    : ('self' '.')? ID '.' func_call
    ;

func_call
    : ID arguments
    ;

arguments
    : '(' arglist ')'
    ;

arglist
    : expression (',' expression)*
    |
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

add_oper
    : '+'
    | '-'
    ;

mul_oper
    : '*'
    | '/'
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