import re
class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 1
        self.current_note = self.source_code[self.position] if self.source_code else None

    def advance(self):
        self.position += 1
        if self.position < len(self.source_code):
            self.current_note = self.source_code[self.position]
        else:
            self.current_note = None

    def tokenize(self):
        """Tokenize the source code into a list of tokens."""
        tokens = []
        while self.current_note is not None:
            if self.current_note.isChord:
                tokens.append(Token('CHORD', self.current_note.degree, self.current_note.figure, f'CHORD_{self.current_note.degree}'))
            elif self.current_note.isRest:
                tokens.append(Token('REST', self.current_note.degree, self.current_note.figure, f'REST_{self.current_note.degree}'))
            else:
                tokens.append(Token('NOTE', self.current_note.degree, self.current_note.figure, f'NOTE_{self.current_note.degree}'))

            self.advance()
        return tokens
    
class Token:
    def __init__(self, type_, degree, duration, value):
        self.type = type_
        self.degree = int(degree) if degree.isdigit() else degree
        self.duration = duration
        self.value = value
        self.num = self.degree


    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.degree}, {self.duration})"
    
    def roman_to_int(self, symbol):
        return int(symbol[-1]) if symbol[-1].isdigit() else 0