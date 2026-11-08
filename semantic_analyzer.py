
from oosListener import oosListener


class SemanticAnalyzer(oosListener):

    def __init__(self, collector):
        self.collector = collector
        self.errors = list(collector.errors)

    def check_type(self, name, line):
        if name == "int":
            return

        symbol = self.collector.table.global_scope.symbols.get(name)

        if symbol is None or symbol.kind != "class":
            self.errors.append(
                f"Semantic error at line {line}: "
                f"Unknown type '{name}'"
            )

    def enterTypes(self, ctx):
        if ctx.class_name() is not None:
            self.check_type(
                ctx.class_name().getText(),
                ctx.start.line
            )

    def enterClass_def(self, ctx):
        # Check inherited class names
        for parent_ctx in ctx.class_name()[1:]:
            self.check_type(
                parent_ctx.getText(),
                parent_ctx.start.line
            )

    def enterConstructor_def(self, ctx):
        # The declared constructor type must exist
        self.check_type(
            ctx.class_name().getText(),
            ctx.start.line
        )
