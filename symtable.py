class SymbolTable:
    def __init__(self):
        self.variables = {}

    def getter(self, variable):
        if variable in self.variables:
            return self.variables[variable]
        raise NameError(f'Variable {variable} not found in SymbolTable')

    def setter(self, variable, typ, value):
        if value == None:
            self.variables[variable] = [typ, value]

        else:
            #variable = variable.value
            if variable in self.variables:
                if self.variables[variable][0] == typ:
                    self.variables[variable][1] = value
            else:
                raise NameError(f'Variable {variable} not declared before assigment')