class SymbolTable:
    def __init__(self):
        self.variables = {}
        self.position = 0

    def getter(self, variable):
        if variable in self.variables:
            return self.variables[variable]
        raise NameError(f'Variable {variable} not found in SymbolTable')

    def setter(self, variable, typ, value):
        if value == None:
            self.position += 4
            self.variables[variable] = [typ, value, self.position]
        else:
            if variable in self.variables:
                if self.variables[variable][0] == typ:
                    self.variables[variable][1] = value
            else:
                raise NameError(f'Variable {variable} not declared before assigment')