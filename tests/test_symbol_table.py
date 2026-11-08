
from symbol_table import Symbol, SymbolTable


def test_symbol_table():
    table = SymbolTable()

    # Global declaration
    assert table.define(
        Symbol("Person", "class", "Person")
    )

    # Duplicate declaration
    assert not table.define(
        Symbol("Person", "class", "Person")
    )

    # Enter class scope
    table.enter_scope("Person")

    assert table.define(
        Symbol("age", "field", "int")
    )

    # Find symbol in current scope
    assert table.resolve("age") is not None

    # Find symbol in parent scope
    assert table.resolve("Person") is not None

    # Unknown symbol
    assert table.resolve("unknown") is None

    # Exit class scope
    table.exit_scope()

    # Class field is not visible globally
    assert table.resolve("age") is None


if __name__ == "__main__":
    test_symbol_table()
    print("Symbol table tests passed!")
