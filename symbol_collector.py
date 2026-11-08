
from oosListener import oosListener
from symbol_table import Symbol, SymbolTable


class SymbolCollector(oosListener):

    def __init__(self):
        self.table = SymbolTable()
        self.errors = []

        self.current_class = None

        # Keep scopes for semantic analysis later
        self.class_scopes = {}
        self.method_scopes = {}

    def add_symbol(self, name, kind, type_name, ctx):
        symbol = Symbol(
            name=name,
            kind=kind,
            type_name=type_name,
            line=ctx.start.line
        )

        if not self.table.define(symbol):
            self.errors.append(
                f"Line {ctx.start.line}: "
                f"Duplicate declaration of '{name}'"
            )

    # --------------------------
    # Classes
    # --------------------------

    def enterClass_def(self, ctx):
        name = ctx.class_name(0).getText()

        self.add_symbol(name, "class", name, ctx)

        self.current_class = name
        self.table.enter_scope(name)

        self.class_scopes[name] = self.table.current_scope

    def exitClass_def(self, ctx):
        self.table.exit_scope()
        self.current_class = None

    def enterClass_main_def(self, ctx):
        name = ctx.getChild(1).getText()

        self.add_symbol(name, "class", name, ctx)

        self.current_class = name
        self.table.enter_scope(name)

        self.class_scopes[name] = self.table.current_scope

    def exitClass_main_def(self, ctx):
        self.table.exit_scope()
        self.current_class = None

    # --------------------------
    # Constructors
    # --------------------------

    def enterConstructor_def(self, ctx):
        name = "__init__"

        self.add_symbol(
            name, "constructor", self.current_class, ctx
        )

        self.enter_method_scope(name, ctx)

    def exitConstructor_def(self, ctx):
        self.table.exit_scope()

    # --------------------------
    # Methods
    # --------------------------

    def enterMethod_def(self, ctx):
        name = ctx.ID().getText()
        return_type = ctx.return_type().getText()

        self.add_symbol(name, "method", return_type, ctx)

        self.enter_method_scope(name, ctx)

    def exitMethod_def(self, ctx):
        self.table.exit_scope()

    def enterMethod_main_def(self, ctx):
        name = "main"

        self.add_symbol(name, "method", "-", ctx)

        self.enter_method_scope(name, ctx)

    def exitMethod_main_def(self, ctx):
        self.table.exit_scope()

    def enter_method_scope(self, name, ctx):
        self.table.enter_scope(name)

        self.method_scopes[
            (self.current_class, name)
        ] = self.table.current_scope

        # Implicit self parameter
        self.add_symbol(
            "self", "parameter", self.current_class, ctx
        )

        if hasattr(ctx, "parameters") and ctx.parameters():
            parlist = ctx.parameters().parlist()

            types = parlist.types()
            identifiers = parlist.ID()

            for type_ctx, id_ctx in zip(types, identifiers):
                self.add_symbol(
                    id_ctx.getText(),
                    "parameter",
                    type_ctx.getText(),
                    ctx
                )

    # --------------------------
    # Variable declarations
    # --------------------------

    def enterDecl_line(self, ctx):
        type_name = ctx.types().getText()

        if self.table.current_scope.name == self.current_class:
            kind = "field"
        else:
            kind = "variable"

        for identifier in ctx.ID():
            self.add_symbol(
                identifier.getText(),
                kind,
                type_name,
                ctx
            )
