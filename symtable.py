class SymbolTable:
    def __init__(self):
        self.variables = {}

    def getter(self, variable):
        if variable in self.variables.keys():
            return self.variables[variable]
        raise NameError(f'Variable {variable} not found in SymbolTable')

    def setter(self, variable, value):
        self.variables[variable] = value