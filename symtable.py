class SymbolTable:
    def __init__(self):
        self.symbols = {'return': [None, None]}
        self.functions = {}


    def getter_symbol(self, typ):
        if typ in self.symbols.keys():
            if self.symbols[typ][0] is not None:
                return self.symbols[typ]
            else:
                raise  NameError(f'Symbol {typ} has no value')
        else:
            raise  NameError(f'Symbol {typ} not in symbol table')
    
    def setter_symbol(self, typ, value):
        if typ in self.symbols.keys():
            self.symbols[typ][0] = value
        else:
            raise  NameError(f'Symbol {typ} not defined')

    def getter_type(self, typ):
        if typ in self.symbols.keys():
            return self.symbols[typ][1]
        else:
            raise  NameError(f'Type {typ} not in symbols table')

    def setter_type(self, value, typ):
        if (value not in self.functions.keys() and value not in self.symbols.keys()):
            self.symbols[value] = [None, typ]
        else:
            raise  NameError(f'Type {value} already in symbols or functions table')
    
    def getter_function(self, function):
        if function in self.functions.keys():
            return self.functions[function]
        else:
            raise  NameError(f'Function {function} not in functions table')

    def setter_function(self, func_symbol, func, typ):
        if (func_symbol not in self.functions.keys() and func_symbol not in self.symbols.keys()):
            self.functions[func_symbol] = [func, typ]
        else:
            raise  NameError(
                f'Func Symbol {func_symbol} already in symbol/func table')
    
    def getter_return(self):
        return self.symbols['return']
    
    def setter_return(self, value, typ):
        self.symbols['return'] = [value, typ]
