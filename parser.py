import math
from platform import node
from AST import IfNode, ComparisonNode, BlockNode, AssignmentNode, StringAssignmentNode, VariableDeclarationNode, OutputNode, InputNode
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.variables = {}
        self.output_tokens = []

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def advance(self):
            self.position += 1

    def match(self, token_type, duration=None):
        tok = self.current_token()
        if tok and tok.type == token_type and (duration is None or tok.duration == duration):
            self.advance()
            return tok
        return None

    def parse_variable_declaration(self):
        # Match declaration motif: dotted eighth, 16th, quarter
        if (self.match("NOTE", "eighth.") and
            self.match("NOTE", "16th") and
            self.match("NOTE", "quarter")):

            var_name_tokens = []
            while self.current_token() and self.current_token().type == "CHORD":
                var_name_tokens.append(self.current_token().value)
                self.advance()

            var_name = "-".join(var_name_tokens)
            if var_name:
                return VariableDeclarationNode(var_name)

        return None

    def parse_variable_assignment(self):
        if (self.match("NOTE", "eighthts") and
            self.match("NOTE", "eighthts") and
            self.match("NOTE", "eighthts")):

            var_name_tokens = []
            note_assignment = False
            
            while self.current_token() and (self.current_token().type == "CHORD"):
                var_name_tokens.append(self.current_token().value)
                self.advance()
                

            var_name = "-".join(var_name_tokens)
            if len(var_name_tokens) < 2:
                return None
            if var_name not in self.variables:
                return f"Error: Undeclared variable '{var_name}'"

            value = 0
            duration_map = {
                "16th": 0.25,
                "eighth": 0.5,
                "quarter": 1.0,
                "half": 2.0,
                "whole": 4.0,
            }

            while self.current_token() and self.current_token().type == "NOTE":
                note_assignment = True
                note = self.current_token()
                val = duration_map.get(note.duration)
                next_note = self.tokens[self.position + 1] if self.position + 1 < len(self.tokens) else None

                if next_note and isinstance(next_note.degree, int) and isinstance(note.degree, int):
                    if next_note.degree > note.degree:
                        if val:
                            value += val
                        self.advance()
                    elif next_note.degree < note.degree:
                        if val:
                            value -= val
                        self.advance()
                else:
                    if val:
                        value += val
                    self.advance()
                    break

            if self.current_token() and self.current_token().type == "REST" and not note_assignment:
                self.advance()
            var_name_tokens = []

            while self.current_token() and self.current_token().type == "CHORD" and not note_assignment:
                var_name_tokens.append(self.current_token().value)
                self.advance()

            if not note_assignment and len(var_name_tokens) > 0:
                var_name_value = "-".join(var_name_tokens)
                if len(var_name_tokens) < 2:
                    return None
                if var_name_value not in self.variables:
                    return f"Error: Undeclared variable '{var_name_value}'"

                return AssignmentNode(var_name, self.variables[var_name_value].value)


            return AssignmentNode(var_name, value)

        return None
    


    def parse_string_assignment(self):
        if (self.match("NOTE", "16th") and
            self.match("NOTE", "16th") and
            self.match("NOTE", "16th") and
            self.match("NOTE", "16th")):

            var_name_tokens = []
            while self.current_token() and self.current_token().type == "REST":
                self.advance()
            while self.current_token() and self.current_token().type == "CHORD":
                var_name_tokens.append(self.current_token().value)
                self.advance()

            var_name = "-".join(var_name_tokens)
            if len(var_name_tokens) < 2:
                return None
            if var_name not in self.variables:
                return f"Error: Undeclared variable '{var_name}'"

            tonic_degree = -1
            chars = []

            while self.current_token():
                token = self.current_token()

                if tonic_degree == -1 and token.type == "REST":
                    self.advance()
                    continue
                if tonic_degree == -1 and token.type == "NOTE" and isinstance(token.degree, int):
                    tonic_degree = token.degree
                    self.advance()
                    continue
                if token.type == "REST":
                    self.advance()
                    break
                if token.type == "NOTE" and isinstance(token.degree, int):
                    interval = abs(token.degree - tonic_degree)
                    if token.duration == 'eighth':
                        interval += 7
                    elif token.duration == 'quarter':
                        interval += 14
                    elif token.duration == 'half':
                        interval += 21
                    elif token.duration == 'whole':
                        interval += 28
                    char = chr(ord('A') + interval)
                    chars.append(char)
                self.advance()

            string_value = "".join(chars)
            return StringAssignmentNode(var_name, string_value)

        return None

    def parse_output(self):
            # Get the variable name
            var_name_tokens = []
            var_length = 0
            counter = 0
            while self.current_token() and self.current_token().type == "REST":
                #self.advance()
                return None
                counter += 1
                if counter > 14:
                    print("Warning: too many RESTs, possible infinite loop.")
                    break
                #self.advance()
                
            while self.current_token() and self.current_token().type == "CHORD":
                var_name_tokens.append(self.current_token().value)
                self.advance()
            var_name = "-".join(var_name_tokens)
            var_length = len(var_name_tokens)
            if var_length < 2:
                return None
            var_name_tokens = []
            if var_name == '':
                return None


            if var_name not in self.variables:
                print(f'variable {var_name} not found')
                return f"Error: Undeclared variable '{var_name}'"
            
            while self.current_token() and self.current_token().type == "REST":
                self.advance()

            while self.current_token() and self.current_token().type == "CHORD":
                var_name_tokens.append(self.current_token().value)
                self.advance()
                var_name2 = "-".join(var_name_tokens)
                if len(var_name_tokens) > var_length:
                    self.position -= 3
                    return None

                if var_name2 == var_name:
                    var_name_tokens = []
                    while self.current_token() and self.current_token().type == "REST":
                        self.advance()

                    while self.current_token() and self.current_token().type == "CHORD":
                        var_name_tokens.append(self.current_token().value)
                        self.advance()
                        cadence_name = "-".join(var_name_tokens)
                        if cadence_name == 'CHORD_V-CHORD_I':

                            return OutputNode(var_name)
                        else:
                            self.position -= 7
                            return None
            self.position -= 3  # Restore position if no output found
            return None
    
    def parse_input(self):
        var_name_tokens = []
        var_length = 0

        # Skip leading RESTs
        while self.current_token() and self.current_token().type == "REST":
            return None

        while self.current_token() and self.current_token().type == "CHORD":
            var_name_tokens.append(self.current_token().value)
            self.advance()
        var_name = "-".join(var_name_tokens)
        var_length = len(var_name_tokens)
        if var_length < 2:
            return None
        if var_name == '':
            return None

        if var_name not in self.variables:
            print(f'variable {var_name} not found')
            return f"Error: Undeclared variable '{var_name}'"

        while self.current_token() and self.current_token().type == "REST":
            self.advance()
        
        var_name_tokens = []
        
        while self.current_token() and self.current_token().type == "CHORD":
            var_name_tokens.append(self.current_token().value)
            self.advance()
            var_name2 = "-".join(var_name_tokens)
            if len(var_name_tokens) > var_length:
                self.position -= 3
                return None
            
        if var_name == var_name2:
            # Look for cadence CHORD_I - CHORD_V
            cadence_tokens = []
            while self.current_token() and self.current_token().type == "REST":
                self.advance()
            while self.current_token() and self.current_token().type == "CHORD":

                cadence_tokens.append(self.current_token().value)
                self.advance()
                if len(cadence_tokens) > var_length:
                    self.position -= 3
                    return None
                if len(cadence_tokens) == 2:
                    if "-".join(cadence_tokens) == 'CHORD_I-CHORD_V':
                        return InputNode(var_name)
                    else:
                        self.position -= 7
                        return None

        self.position -= 3  # Restore position if no cadence match
        return None

    
    def parse_statement(self):
        if_node = self.parse_if()
        if if_node:
            return if_node
        return None


    def parse_body(self):
        statements = []
        max_statements = 10
        count = 0

        while self.current_token() and count < max_statements:
            # Check for Authentic Cadence (V - I)
            if (
                self.current_token().type == 'CHORD' and self.current_token().value == 'CHORD_V' and
                self.position + 1 < len(self.tokens) and
                self.tokens[self.position + 1].type == 'CHORD' and self.tokens[self.position + 1].value == 'CHORD_I'
            ):
                # Advance past the cadence tokens
                self.advance()
                self.advance()
                break  # End the block

            pos_backup = self.position  # Save current position

            stmt = (
                self.parse_variable_assignment() or
                self.parse_string_assignment() or
                self.parse_output()
            )

            if stmt:
                statements.append(stmt)
            else:
                self.position = pos_backup  # Restore position
                self.advance()  # Now safe to advance one token

            count += 1

        return BlockNode(statements)

    


    def parse_if(self):
        # Look for Half Cadence (I-V)
        var_name_tokens = []
        while self.current_token() and self.current_token().type == "REST":
            return None
            #self.advance()
        if self.current_token() and self.current_token().type == "CHORD":
            var_name_tokens.append(self.current_token().value)
            var_name_tokens.append(self.tokens[self.position + 1].value)
        cadence = "-".join(var_name_tokens)
        if cadence != 'CHORD_I-CHORD_V':
            return None  # Not an if statement

        self.advance()  # Move past the first CHORD
        self.advance()  # Move past the second CHORD
        # Parse the condition expression
        condition = self.parse_expression()
        if not condition:
            return None

        # Parse the block
        body = self.parse_body()
        return IfNode(condition, body)

    
    def parse_expression(self):
        tokens = []
        first = None
        second = None
        op = None
        expression = ()
        var_name_tokens = []
        while self.current_token() and self.current_token().type == "REST":
            self.advance()
        while self.current_token() and self.current_token().type == "CHORD" and first is None:
            var_name_tokens.append(self.current_token().value)
            self.advance()
        first = "-".join(var_name_tokens)
        var_name_tokens = []
        
        
        while self.current_token() and self.current_token().type == "REST":
            self.advance()
        
        while self.current_token() and self.current_token().type == "CHORD" and second is None and first:
            var_name_tokens.append(self.current_token().value)
            self.advance()
        second = "-".join(var_name_tokens)
        var_name_tokens = []



        if first not in self.variables:
            print(f'variable {first} not found')
            return f"Error: Undeclared variable '{first}'"
        if second not in self.variables:
            print(f'variable {second} not found')
            return f"Error: Undeclared variable '{second}'"
        

        while self.current_token() and self.current_token().type == "REST":
            self.advance()
        
        while self.current_token() and self.current_token().type == "NOTE":
            tokens.append(self.current_token())
            self.advance()
            if len(tokens) > 2:
                break
        if len(tokens) == 2:
            if abs(tokens[0].degree - tokens[1].degree) == 4:
                op = "GREATER"
            elif abs(tokens[0].degree - tokens[1].degree) == 3:
                op = "LESSER"
            elif abs(tokens[0].degree - tokens[1].degree) == 0:
                op = "EQUAL"
            else:
                print(f"Error: Invalid comparison between {tokens[0].degree} and {tokens[1].degree}")
                return None


        

        return ComparisonNode(first, op, second)

    def evaluate(self, node):
        if isinstance(node, BlockNode):
            results = []
            for stmt in node.statements:
                result = self.evaluate(stmt)
                if result is not None:
                    results.append(result)
            return results

        elif isinstance(node, IfNode):
            condition_result = self.evaluate(node.condition)
            if condition_result:
                return self.evaluate(node.body)
            return None

        elif isinstance(node, ComparisonNode):
            left_var = self.variables.get(node.left)
            right_var = self.variables.get(node.right)
            if left_var is None or right_var is None:
                return False  #compariso failing

            left_val = left_var.value
            right_val = right_var.value

            if node.operator == "GREATER":
                return left_val > right_val
            elif node.operator == "LESSER":
                return left_val < right_val
            elif node.operator == "EQUAL":
                return left_val == right_val
            return False

        elif isinstance(node, VariableDeclarationNode):
            if node.var_name not in self.variables:
                self.variables[node.var_name] = Variable(node.var_name)
                return f"Declared variable: {node.var_name}"
            else:
                return f"Warning: Variable '{node.var_name}' already declared"

        elif isinstance(node, AssignmentNode):
            if node.var_name in self.variables:
                self.variables[node.var_name].value = node.value
                return f"Assigned {node.value} to {node.var_name}"
            else:
                return f"Error: Variable '{node.var_name}' not declared"

        elif isinstance(node, StringAssignmentNode):
            if node.var_name in self.variables:
                self.variables[node.var_name].value = node.string_value
                return f"Assigned string \"{node.string_value}\" to {node.var_name}"
            else:
                return f"Error: Variable '{node.var_name}' not declared"

        elif isinstance(node, str):
            if node in self.variables:
                return f"Output: {self.variables[node].value}"
            return f"Error: Variable '{node}' not declared"
        elif isinstance(node, OutputNode):
            if node.var_name in self.variables:
                return f"Output: {self.variables[node.var_name].value}"
            return f"Error: Variable '{node.var_name}' not declared"
        elif isinstance(node, InputNode):
            user_input = input(f"Enter value for {node.var_name}: ")
            # Try to parse to number, fallback to string
            try:
                value = float(user_input) if '.' in user_input else int(user_input)
            except ValueError:
                value = user_input
            self.variables[node.var_name].value = value
            return f"Input received for {node.var_name}: {value}"


        return None




    def parse(self):
        results = []
        max_skips = 20
        rest_streak = 0

        while self.current_token():
            if self.current_token().type == "REST":
                rest_streak += 1
            else:
                rest_streak = 0

            if rest_streak > max_skips:
                print("Stopping parser due to excessive trailing rests.")
                break

            node = (
                self.parse_statement() or
                self.parse_output() or
                self.parse_input() or  
                self.parse_variable_declaration() or
                self.parse_variable_assignment() or
                self.parse_string_assignment() 
            )

            # 🧼 Catch and print string errors directly
            if isinstance(node, str) and node.startswith("Error:"):
                print(f"Evaluated: {node}")
                results.append(node)
            elif node:
                result = self.evaluate(node)
                if result:
                    if isinstance(result, list):
                        for item in result:
                            print(f"Evaluated: {item}")
                            results.append(item)
                    else:
                        print(f"Evaluated: {result}")
                        results.append(result)
            else:
                self.advance()

        return results




class Variable:
    def __init__(self, name: str, value=None):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Variable({self.name} = {self.value})"
