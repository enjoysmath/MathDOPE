import re

class AtomicSymbol:          
    alpha_regex = None
    greek_alphabet = None
    alphabet_parser = None
    numeric_regex = re.compile('-?[0-9]+')
    
    @staticmethod
    def next_symbol(sym:str, rev=None) -> str:
        if rev is None:
            rev = False
        if rev:
            num_dir = -1
        else:
            num_dir = 1
            
        if sym.isnumeric() or (len(sym) > 0 and sym[1:].isnumeric()):
            sym = str(int(sym) + num_dir)
            return sym
        
        if sym.isalpha():
            next_ord = ord(sym[0]) + num_dir
            if sym[0].isupper():
                if next_ord >= ord('A') + 26:
                    next_ord = ord('A')
                elif next_ord < ord('A'):
                    next_ord = ord('Z')
            else:
                if next_ord >= ord('a') + 26:
                    next_ord = ord('a')
                elif next_ord < ord('a'):
                    next_ord = ord('z')
                    
            return str(chr(next_ord))
        
                                   
AtomicSymbol.alpha_regex = r'[a-zA-Z]'
AtomicSymbol.alphabet_parser = re.compile(AtomicSymbol.alpha_regex)
    