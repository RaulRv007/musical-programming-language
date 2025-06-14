from song import Song
from lexer import Lexer
from parser import Parser
if __name__ == "__main__":
    # Create a Song instance with the file path
    song = Song('sheets/max_function.mxl')
    lexer = Lexer(song.processed)
    tokens = lexer.tokenize()
    print(f'Tokens: {tokens}')
    parser = Parser(tokens)
    results = parser.parse()
    print(f'Results: {results}')

