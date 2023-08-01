import ast
import textwrap


def extract_blocks_and_names(code):
    code = textwrap.dedent(code)
    functions = {}
    function_uses = {}
    helper_functions = {}
    current_function = [None]
    last_end_lineno = [0]

    def visit_FunctionDef(node):
        nonlocal last_end_lineno

        if current_function[0] and (not functions[current_function[0]]['end_lineno']
                                     or node.lineno < functions[current_function[0]]['end_lineno']):
            # We are inside a nested function, ignore it
            last_end_lineno[0] = node.lineno
            return
        current_function[0] = node.name
        functions[node.name] = {
            "name": node.name,
            "lineno": node.lineno,
            "end_lineno": getattr(node, "end_lineno", None) or node.lineno,
            "col_offset": node.col_offset
        }
        last_end_lineno[0] = functions[node.name]["end_lineno"]
        ast.NodeVisitor.generic_visit(visitor, node)
        current_function[0] = None

    def visit_Call(node):
        if isinstance(node.func, ast.Name) and current_function[0]:
            if node.func.id not in function_uses:
                function_uses[node.func.id] = []
            if current_function[0] not in function_uses[node.func.id]:
                function_uses[node.func.id].append(current_function[0])
        ast.NodeVisitor.generic_visit(visitor, node)

    visitor = ast.NodeVisitor()
    visitor.visit_FunctionDef = visit_FunctionDef
    visitor.visit_Call = visit_Call

    tree = ast.parse(code)
    visitor.visit(tree)

    function_codes = []
    # Reformat function names: replace underscores with spaces and capitalize each word
    function_names = [func['name'].replace('_', ' ').title() for func in functions.values()]

    for func in functions.values():
        start_line = func['lineno'] - 1
        if func['end_lineno']:
            end_line = func['end_lineno']
        else:
            end_line = len(code.split('\n'))  # take all lines till the end if 'end_lineno' is not available
        function_code = textwrap.dedent('\n'.join(code.split('\n')[start_line:end_line]))
        function_codes.append(function_code)

    for func_name, usage_list in function_uses.items():
        # Reformat function names: replace underscores with spaces and capitalize each word
        if func_name.replace('_', ' ').title() in function_names:  # if a function is called within another function
            helper_functions[func_name.replace('_', ' ').title()] = [u.replace('_', ' ').title() for u in usage_list]

    return function_codes, function_names, helper_functions
