grammar pandaQ;
root : statement             
     ;
statement : stat ';'                                              # PreSelect
     | Id ':=' stat ';'                                           # Assig
     | 'plot' Id ';'                                              # Plot
     ;

stat : 'select' identificadors 'from' taula extras                # Select
     ;

taula : Id                                                        # IdTaula
     | Id ('inner join' Id 'on' Id '=' Id)+                       # InnerJoin
     ;

identificadors: (identificador ',')* identificador                # Ident
     | '*'                                                        # All
     ;   

identificador: Id                                                 # CampNoCalculat 
     | operacio 'as' Id                                           # CampCalculat
     ;

extras : where order                                              # Extra
     ;

where : ('where' compar)?                                         # ExtraWhere
     | 'where' Id 'in' '(' stat ')'                               # Subquery
     ;

order : ('order by' orderby)?                                     # ExtraOrder
     ;

orderby : (Id tipusord ',')* Id tipusord                          # Order_by
     ;

tipusord : ('ASC' | 'DESC' | 'asc' | 'desc')?                     # TipusOrd
     ;


compar : (Num | Id) simbol (Num | Id)                             # Comparacio
     | '(' compar ')'                                             # ComparacioParentesis
     | compar ('and'|'or') compar                                 # ComparacioAndOr
     | 'not' compar                                               # ComparacioNot
     ;

simbol : ('=' | '<>' | '<' | '>' | '<=' | '>=')                   # Comp               
     ;

operacio: '(' operacio ')'                                        # Parentesis
     | operacio ( '*' | '/' ) operacio                            # MultDiv
     | operacio ( '+' | '-' ) operacio                            # SumaResta
     | Id                                                         # FinalId
     | Num                                                        # FinalNum
     ;

             
Num : [0-9]+ ('.' [0-9]+)? ;
Id : [a-zA-Z_]+;
WS  : [ \t\n\r]+ -> skip ;