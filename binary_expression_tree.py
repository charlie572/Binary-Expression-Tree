"""A BinaryExpressionTree class that can be used to convert between infix and postfix"""

def get_symbols(text, indices=False):
    """Iterate over symbols in a string

    A symbol is a number or a character. Whitespace is ignored.

    :param text: The text containing the symbols
    :type text: str
    :param indices: If True, the indices of the first character in each symbol will be yielded.
    :type indices: bool
    """
    symbol = ""
    symbol_index = 0  # the index of the first character in the symbol
    for i, char in enumerate(text):
        if char.isnumeric():
            symbol += char
        else:
            # yield the last symbol if it was a number
            if symbol:
                if indices:
                    yield symbol, symbol_index
                else:
                    yield symbol
                
                symbol = ""

            # yield the current symbol if it isn't whitespace
            if char != " ":
                if indices:
                    yield char, i
                else:
                    yield char

            symbol_index = i + 1

    # yield the final symbol
    if symbol:
        if indices:
            yield symbol, symbol_index
        else:
            yield symbol


class Node:
    """Contains data and two pointers to other nodes"""
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class BinaryExpressionTree:
    """Stores an expression in a binary tree

    This can be used to convert between infix and postfix expressions.
    """
    OPERATORS = ['/', '*', '+', '-']
    
    def __init__(self, root):
        self.root = root

    @staticmethod
    def from_postfix(text):
        """Create a tree from a postfix expression

        :param text: the expression
        :type text: str
        :return: a tree to represent the expression
        :rtype: BinaryExpressionTree
        """
        stack = []
        for symbol in get_symbols(text):
            if symbol in BinaryExpressionTree.OPERATORS:
                root = Node(symbol)
                root.right = stack.pop()
                root.left = stack.pop()
                stack.append(root)
            else:
                stack.append(Node(symbol))

        return BinaryExpressionTree(stack.pop())

    @staticmethod
    def from_infix(text):
        """Create a tree from an infix expression

        :param text: the expression
        :type text: str
        :return: a tree to represent the expression
        :rtype: BinaryExpressionTree
        """
        operators = BinaryExpressionTree.OPERATORS

        # This function works by identifying the operator with the lowest precedence, then making recursive
        # calls to the left and right operands.

        # identify lowest operator
        lowest_operator = -1  # corresponds to an index in BinaryExpressionTree.OPERATORS
        lowest_operator_index = None
        brackets_level = 0
        lowest_operator_brackets_level = -1
        for symbol, i in get_symbols(text, indices=True):
            if symbol == "(":
                brackets_level += 1
            elif symbol == ")":
                brackets_level -= 1
            elif lowest_operator_brackets_level == -1 or brackets_level <= lowest_operator_brackets_level:
                if symbol in operators:
                    # this operator has lower precedence if it is in fewer brackets or if it has a lower BIDMAS precedence
                    if brackets_level < lowest_operator_brackets_level or operators.index(symbol) >= lowest_operator:
                        lowest_operator = operators.index(symbol)
                        lowest_operator_index = i
                        lowest_operator_brackets_level = brackets_level

        if lowest_operator_index is None:
            # There are no operators, so this string should only be one operand.
            # Return the operand.
            for symbol in get_symbols(text):
                if symbol not in "()":
                    return BinaryExpressionTree(Node(symbol))

        # get left and right operands
        left = text[:lowest_operator_index]
        right = text[lowest_operator_index + 1:]
        left = BinaryExpressionTree.from_infix(left).root
        right = BinaryExpressionTree.from_infix(right).root

        # add the operands to the root
        root = Node(operators[lowest_operator], left, right)

        return BinaryExpressionTree(root)
        

    def get_postfix(self, root=None):
        """Get the postfix expression

        If no root is specified, the root of the tree is used.
        
        :param root: The first node to visit
        :type root: Node
        """
        if root is None:
            root = self.root
        
        result = ""

        if root.left:
            result += self.get_postfix(root.left) + " "

        if root.right:
            result += self.get_postfix(root.right) + " "

        result += root.data

        return result

    def get_infix(self, root=None):
        """Get the infix expression

        If no root is specified, the root of the tree is used.
        
        :param root: The first node to visit
        :type root: Node
        """
        if root is None:
            root = self.root
        
        result = ""

        if root.left:
            result += self.get_infix(root.left) + " "

        result += root.data
        
        if root.right:
            result += " " + self.get_infix(root.right)

        if root.left or root.right:
            result = "(" + result + ")"
        
        return result


def main():
    running = True
    while running:
        running = False
        
        notation = input("Do you want to input infix or postfix? (i/p): ")
        expression = input("Enter expression: ")
        
        if notation == 'i':
            tree = BinaryExpressionTree.from_infix(expression)
        elif notation == 'p':
            tree = BinaryExpressionTree.from_postfix(expression)
        else:
            print("You must input i or p.")
            running = True
            continue

        print(f"Infix:   {tree.get_infix()}")
        print(f"Postfix: {tree.get_postfix()}")


if __name__ == "__main__":
    main()


        
