class IfNode:
    def __init__(self, condition, body):
        self.condition = condition  # e.g., ComparisonNode
        self.body = body  # e.g., BlockNode

    def __repr__(self):
        return f"IfNode(condition={self.condition}, body={self.body})"

class ComparisonNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator  # 'EQUAL', 'GREATER', 'LESSER'
        self.right = right

    def __repr__(self):
        return f"ComparisonNode({self.left} {self.operator} {self.right})"

class BlockNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"BlockNode(statements={self.statements})"
    
class AssignmentNode:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

class StringAssignmentNode:
    def __init__(self, var_name, string_value):
        self.var_name = var_name
        self.string_value = string_value
class VariableDeclarationNode:
    def __init__(self, var_name):
        self.var_name = var_name

class OutputNode:
    def __init__(self, var_name):
        self.var_name = var_name

class InputNode:
    def __init__(self, var_name):
        self.var_name = var_name

    def __repr__(self):
        return f"InputNode({self.var_name})"


