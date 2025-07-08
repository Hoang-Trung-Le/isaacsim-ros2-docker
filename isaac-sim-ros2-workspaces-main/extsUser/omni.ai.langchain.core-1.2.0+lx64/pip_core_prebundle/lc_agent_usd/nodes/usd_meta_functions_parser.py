import ast


def extract_function_signatures(filename: str) -> str:
    with open(filename, "r") as file:
        code = file.read()

    # Parse the code into an AST
    parsed_code = ast.parse(code)

    # Extract the function definitions
    functions = [node for node in parsed_code.body if isinstance(node, ast.FunctionDef)]

    # Generate the desired output
    output = ""
    for func in functions:
        func_name = func.name
        args = [arg.arg + ": " + ast.unparse(arg.annotation) for arg in func.args.args]
        return_annotation = ast.unparse(func.returns) if func.returns else "None"
        docstring = ast.get_docstring(func)

        output += f"def {func_name}({', '.join(args)}) -> {return_annotation}:\n"
        if docstring:
            output += f'    """{docstring}"""\n'
        output += "    ...\n\n"

    return output.strip()
