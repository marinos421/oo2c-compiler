
from oosListener import oosListener


class SemanticAnalyzer(oosListener):

    def __init__(self, collector):
        self.collector = collector
        self.errors = list(collector.errors)

        self.current_class = None
        self.current_scope = collector.table.global_scope

    # --------------------------
    # Existing type checks
    # --------------------------

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

    # --------------------------
    # Class scopes
    # --------------------------

    def enterClass_def(self, ctx):
        for parent_ctx in ctx.class_name()[1:]:
            self.check_type(
                parent_ctx.getText(),
                parent_ctx.start.line
            )

        name = ctx.class_name(0).getText()
        self.enter_class_scope(name)

    def exitClass_def(self, ctx):
        self.exit_class_scope()

    def enterClass_main_def(self, ctx):
        name = ctx.getChild(1).getText()
        self.enter_class_scope(name)

    def exitClass_main_def(self, ctx):
        self.exit_class_scope()

    def enter_class_scope(self, name):
        self.current_class = name
        self.current_scope = self.collector.class_scopes[name]

    def exit_class_scope(self):
        self.current_scope = self.collector.table.global_scope
        self.current_class = None

    # --------------------------
    # Method scopes
    # --------------------------

    def enterConstructor_def(self, ctx):
        self.check_type(
            ctx.class_name().getText(),
            ctx.start.line
        )
        self.enter_method_scope("__init__")

    def exitConstructor_def(self, ctx):
        self.exit_method_scope()

    def enterMethod_def(self, ctx):
        self.enter_method_scope(ctx.ID().getText())

    def exitMethod_def(self, ctx):
        self.exit_method_scope()

    def enterMethod_main_def(self, ctx):
        self.enter_method_scope("main")

    def exitMethod_main_def(self, ctx):
        self.exit_method_scope()

    def enter_method_scope(self, name):
        self.current_scope = self.collector.method_scopes[
            (self.current_class, name)
        ]

    def exit_method_scope(self):
        self.current_scope = self.collector.class_scopes[
            self.current_class
        ]

    # --------------------------
    # Variable resolution
    # --------------------------

    def check_variable(self, token):
        name = token.getText()
        symbol = self.current_scope.resolve(name)

        if symbol is None or symbol.kind not in (
            "variable", "parameter", "field"
        ):
            self.errors.append(
                f"Semantic error at line {token.symbol.line}: "
                f"Undeclared variable '{name}'"
            )

    def check_identifier_usage(self, ctx):
        identifiers = ctx.ID()

        if not identifiers:
            return

        # self.x: member checking will be added later
        if ctx.getChild(0).getText() == "self":
            return

        # x or obj.x: check the variable or receiver
        self.check_variable(identifiers[0])

    def enterReference(self, ctx):
        self.check_identifier_usage(ctx)

    def enterAssign_target(self, ctx):
        self.check_identifier_usage(ctx)
        
    
    
    def enterObject_method_call(self, ctx):
        # Example: obj.calculate(10)
        # Check that the receiver is a class object.

        # self.obj.method() will be handled later.
        if ctx.getChild(0).getText() == "self":
            return

        receiver = ctx.ID()
        name = receiver.getText()

        symbol = self.current_scope.resolve(name)

        if symbol is None:
            self.check_variable(receiver)
            return

        # Only variables, parameters and fields can be receivers.
        if symbol.kind not in ("variable", "parameter", "field"):
            self.errors.append(
                f"Semantic error at line {receiver.symbol.line}: "
                f"Invalid method receiver '{name}'"
            )
            return

        # An integer cannot have methods.
        if symbol.type_name == "int":
            self.errors.append(
                f"Semantic error at line {receiver.symbol.line}: "
                f"Invalid method receiver '{name}': "
                f"expected an object, got int"
            )
            return
        
        
        # Find the receiver's class.
        class_name = symbol.type_name
        class_scope = self.collector.class_scopes.get(class_name)

        if class_scope is None:
            return

        # Find the requested method.
        method_name = ctx.func_call().ID().getText()
        method_symbol = class_scope.symbols.get(method_name)

        if method_symbol is None or method_symbol.kind != "method":
            self.errors.append(
                f"Semantic error at line {ctx.start.line}: "
                f"Unknown method '{method_name}' "
                f"in class '{class_name}'"
            )
            return
        
        
        # Get the declared parameters of the method.
        method_scope = self.collector.method_scopes.get(
            (class_name, method_name)
        )

        if method_scope is None:
            return

        expected_count = sum(
            1
            for symbol in method_scope.symbols.values()
            if symbol.kind == "parameter"
            and symbol.name != "self"
        )

        # Count arguments supplied in the method call.
        arglist = ctx.func_call().arguments().arglist()
        actual_count = len(arglist.expression())

        if expected_count != actual_count:
            self.errors.append(
                f"Semantic error at line {ctx.start.line}: "
                f"Argument count mismatch for method "
                f"'{method_name}': expected {expected_count}, "
                f"got {actual_count}"
            )
            return

        
        # Check argument types only when counts match.
        expected_parameters = [
            param
            for param in method_scope.symbols.values()
            if param.kind == "parameter"
            and param.name != "self"
        ]

        arguments = arglist.expression()

        for index, (parameter, argument) in enumerate(
            zip(expected_parameters, arguments), start=1
        ):
            expected_type = parameter.type_name
            actual_type = self.get_expression_type(argument)

            # Unknown expression types are handled separately.
            if actual_type is None:
                continue

            if expected_type != actual_type:
                self.errors.append(
                    f"Semantic error at line {argument.start.line}: "
                    f"Argument type mismatch in method "
                    f"'{method_name}', argument {index}: "
                    f"expected '{expected_type}', "
                    f"got '{actual_type}'"
                )



    

    def get_factor_type(self, ctx):
        if ctx.INTEGER() is not None:
            return "int"

        if ctx.expression() is not None:
            return self.get_expression_type(ctx.expression())

        reference = ctx.reference()

        if reference is None:
            # Method calls will be checked later.
            return None

        # Only simple identifiers for now.
        if len(reference.ID()) != 1:
            return None

        name = reference.ID(0).getText()

        if reference.getText() != name:
            return None

        symbol = self.current_scope.resolve(name)

        if symbol is None:
            return None

        if symbol.kind not in ("variable", "parameter", "field"):
            return None

        return symbol.type_name

    
    def get_term_type(self, ctx):
        factor_types = [
            self.get_factor_type(factor)
            for factor in ctx.factor()
        ]

        # A single factor needs no multiplication check.
        if len(factor_types) == 1:
            return factor_types[0]

        # Unknown types will be handled in later stages.
        if None in factor_types:
            return None

        if any(t != "int" for t in factor_types):
            self.errors.append(
                f"Semantic error at line {ctx.start.line}: "
                f"Arithmetic operators require int operands"
            )
            return None

        return "int"

    def get_expression_type(self, ctx):
        term_types = [
            self.get_term_type(term)
            for term in ctx.term()
        ]

        # Avoid reporting extra errors when a child
        # expression could not be typed.
        if None in term_types:
            return None

        has_sign = bool(ctx.optional_sign().getText())
        has_operations = len(term_types) > 1

        if not has_sign and not has_operations:
            return term_types[0]

        if any(t != "int" for t in term_types):
            self.errors.append(
                f"Semantic error at line {ctx.start.line}: "
                f"Arithmetic operators require int operands"
            )
            return None

        return "int"



    def enterAssignment_stat(self, ctx):
        target = ctx.assign_target()

        # For now, only simple variables.
        if len(target.ID()) != 1:
            return

        name = target.ID(0).getText()

        if target.getText() != name:
            return

        symbol = self.current_scope.resolve(name)

        # Undeclared variables are checked separately.
        if symbol is None:
            return

        if symbol.kind not in ("variable", "parameter", "field"):
            return

        expected_type = symbol.type_name
        actual_type = self.get_expression_type(
            ctx.expression()
        )

        # More complex expressions will be checked later.
        if actual_type is None:
            return

        if expected_type != actual_type:
            self.errors.append(
                f"Semantic error at line {ctx.start.line}: "
                f"Type mismatch: cannot assign "
                f"'{actual_type}' to '{expected_type}'"
            )
            
            
    def enterReturn_stat(self, ctx):
        # The current scope belongs to the enclosing method.
        method_scope = self.current_scope

        # Constructor and main return checks
        # will be handled separately.
        if method_scope.name in ("__init__", "main"):
            return

        class_scope = method_scope.parent

        if class_scope is None:
            return

        method_symbol = class_scope.symbols.get(
            method_scope.name
        )

        if method_symbol is None:
            return

        if method_symbol.kind != "method":
            return

        expected_type = method_symbol.type_name

        # Void-like methods are handled separately.
        if expected_type == "-":
            return

        actual_type = self.get_expression_type(
            ctx.expression()
        )

        # Unknown expression types are checked elsewhere.
        if actual_type is None:
            return

        if expected_type != actual_type:
            self.errors.append(
                f"Semantic error at line {ctx.start.line}: "
                f"Return type mismatch: expected "
                f"'{expected_type}', got '{actual_type}'"
            )

