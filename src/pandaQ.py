from antlr4 import *
from pandaQLexer import pandaQLexer
from pandaQParser import pandaQParser
from pandaQVisitor import pandaQVisitor
import streamlit as st
import pandas as pd


class EvalVisitor(pandaQVisitor):

    def __init__(self):
        # Create a session in order to save symbol table
        if 'session' not in st.session_state:
            st.session_state['session'] = {}

        # Loading a possible symbol table
        self.ts = st.session_state['session']
        self.es_subquery = 0

    def visitRoot(self, ctx):
        [statement] = list(ctx.getChildren())
        self.visit(statement)

    def visitPreSelect(self, ctx):
        [select, _] = list(ctx.getChildren())
        self.visit(select)

    def visitAssig(self, ctx):
        [id, _, select, _] = list(ctx.getChildren())
        self.visit(select)
        self.ts[id.getText()] = self.df
        st.session_state['session'] = self.ts

    def visitPlot(self, ctx):
        # Don't want to plot ids, nonsense
        numeros = self.ts[id.getText()].select_dtypes(include=["number"])
        numeros_sin_id = [num for num in numeros if not num.endswith("_id")]
        st.line_chart(numeros[numeros_sin_id])

    def visitSelect(self, ctx):
        [_, ids, _, taules, extras] = list(ctx.getChildren())

        self.visit(taules)

        self.visit(extras)

        self.visit(ids)

        if self.es_subquery == 0:
            st.table(self.df)

        else:
            self.es_subquery -= 1
            return self.df

    def visitIdTaula(self, ctx):
        [taula] = list(ctx.getChildren())
        id = taula.getText()

        # Symbol table
        if id in self.ts:
            self.df = self.ts[id]

        # Reading table
        else:
            nomarchiu = id + ".csv"
            self.df = pd.read_csv("../data/" + nomarchiu)

    def visitInnerJoin(self, ctx):
        L = list(ctx.getChildren())
        taulaini = L.pop(0)
        self.df = pd.read_csv("../data/" + taulaini.getText() + '.csv')

        # Reverse list in order to ease the id extraction.
        L.reverse()
        # 'inner join' Id1 'on' Id2 '=' Id3
        id3 = map(lambda i: i.getText(), L[::6])
        id2 = map(lambda i: i.getText(), L[2::6])
        id1 = map(lambda i: i.getText(), L[4::6])

        # Inner join of all tables.
        for taula, on1, on2 in zip(id1, id2, id3):
            taula = pd.read_csv("../data/" + taula + '.csv')
            self.df = pd.merge(self.df, taula, left_on=on1,
                               right_on=on2, how='inner')

    def visitIdent(self, ctx):
        ids = list(ctx.getChildren())[0::2]
        L = []
        for i in ids:
            L.append(self.visit(i))
        self.df = self.df[L]

    def visitAll(self, ctx):
        pass

    def visitCampNoCalculat(self, ctx):
        [id] = list(ctx.getChildren())
        return (id.getText())

    def visitCampCalculat(self, ctx):
        [operacio, _, id] = list(ctx.getChildren())
        self.df[id.getText()] = self.visit(operacio)
        return (id.getText())

    def visitExtra(self, ctx):
        [where, orderby] = list(ctx.getChildren())
        self.visit(where)
        self.visit(orderby)

    def visitExtraWhere(self, ctx):
        L = list(ctx.getChildren())

        # If there's a where, we apply the condition in order to filter by columns on our dataframe
        if L:
            [_, where] = L
            exp_bool = self.visit(where)
            self.df = self.df.query(exp_bool)

    def visitSubquery(self, ctx):
        [_, id, _, _, select, _] = list(ctx.getChildren())

        # Tracking subqueries (es_subquery != 0 means it's a subquery and how deep it goes)
        copia_df = self.df
        self.es_subquery += 1

        subquery = self.visit(select)
        self.df = copia_df
        L = self.df.columns.tolist()

        # In order to filter, we inner join the tables.
        self.df = pd.merge(self.df, subquery, on=id.getText(), how='inner')
        self.df = self.df[L]

    def visitExtraOrder(self, ctx):
        L = list(ctx.getChildren())

        if L:
            [_, order] = L
            self.visit(order)

    def visitOrder_by(self, ctx):
        # id asc/desc "," id asc/desc "," ...
        fills = list(ctx.getChildren())

        # Get ids and type of sorting
        ascfills = fills[1::3]
        ids = fills[0::3]
        asc = []
        noms = []

        for i in ids:
            noms.append(i.getText())
        for i in ascfills:
            asc.append(self.visit(i))

        # Order by
        self.df = self.df.sort_values(by=noms, ascending=asc)

    def visitTipusOrd(self, ctx):
        L = list(ctx.getChildren())

        # Decides ascending / descending sorting
        if not L:
            return True
        elif L[0].getText() == 'ASC' or L[0].getText() == 'asc':
            return True
        else:
            return False

    def visitComparacio(self, ctx):
        [numid1, simbol, numid2] = list(ctx.getChildren())
        textnumid1 = numid1.getText()
        textsimbol = self.visit(simbol)
        textnumid2 = numid2.getText()

        # If it's a string it gets quoted
        if not textnumid2.isnumeric():
            textnumid2 = f"'{numid2.getText()}'"

        exp_bool = f'{textnumid1} {textsimbol} {textnumid2}'
        return exp_bool

    def visitComparacioParentesis(self, ctx):
        [_, comp, _] = list(ctx.getChildren())

        textcomp = self.visit(comp)
        exp_bool = f'( {textcomp} )'
        return exp_bool

    def visitComparacioAndOr(self, ctx):
        [comp1, andor, comp2] = list(ctx.getChildren())

        textcomp1 = self.visit(comp1)
        textandor = andor.getText()
        textcomp2 = self.visit(comp2)
        exp_bool = f'{textcomp1} {textandor} {textcomp2}'
        return exp_bool

    def visitComparacioNot(self, ctx):
        [_, comp] = list(ctx.getChildren())

        textcomp = self.visit(comp)
        exp_bool = f'not {textcomp}'
        return exp_bool

    def visitComp(self, ctx):
        [comp] = list(ctx.getChildren())

        if comp.getText() == '=':
            return '=='
        elif comp.getText() == '<>':
            return '!='
        else:
            return comp.getText()

    def visitParentesis(self, ctx):
        [_, operacio, _] = list(ctx.getChildren())
        return (self.visit(operacio))

    def visitMultDiv(self, ctx):
        [camp1, op, camp2] = list(ctx.getChildren())
        if op.getText() == '*':
            columna = self.visit(camp1) * self.visit(camp2)
            return columna
        else:
            columna = self.visit(camp1) / self.visit(camp2)
            return columna

    def visitFinalId(self, ctx):
        [id] = list(ctx.getChildren())
        return self.df[id.getText()]

    def visitFinalNum(self, ctx):
        [num] = list(ctx.getChildren())
        return (float(num.getText()))


# Streamlit interface
user_input = st.text_area("Query:")
if st.button("Submit"):

    lexer = pandaQLexer(InputStream(user_input))
    token_stream = CommonTokenStream(lexer)
    parser = pandaQParser(token_stream)
    tree = parser.root()

    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = EvalVisitor()
        visitor.visit(tree)

    else:
        print(parser.getNumberOfSyntaxErrors(), ' sintax errors.')
        print(tree.toStringTree(recog=parser))
