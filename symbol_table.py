
from dataclasses import dataclass, field


@dataclass
class Symbol:
    name: str
    kind: str
    type_name: str | None = None
    line: int | None = None


@dataclass
class Scope:
    name: str
    parent: "Scope | None" = None
    symbols: dict[str, Symbol] = field(default_factory=dict)

    def define(self, symbol: Symbol) -> bool:
        if symbol.name in self.symbols:
            return False

        self.symbols[symbol.name] = symbol
        return True

    def resolve(self, name: str) -> Symbol | None:
        scope = self

        while scope is not None:
            if name in scope.symbols:
                return scope.symbols[name]

            scope = scope.parent

        return None


class SymbolTable:
    def __init__(self):
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope

    def enter_scope(self, name: str):
        self.current_scope = Scope(
            name=name,
            parent=self.current_scope
        )

    def exit_scope(self):
        if self.current_scope.parent is None:
            raise RuntimeError("Cannot exit global scope")

        self.current_scope = self.current_scope.parent

    def define(self, symbol: Symbol) -> bool:
        return self.current_scope.define(symbol)

    def resolve(self, name: str) -> Symbol | None:
        return self.current_scope.resolve(name)
