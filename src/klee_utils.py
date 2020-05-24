"""Handles work with klee, which does symbollic execution and test generation of C code."""

from typing import Dict, Set, Any
from collections import defaultdict
import uuid
from pycparser import c_ast, parse_file, c_generator  # type: ignore


class FuncVisitor(c_ast.NodeVisitor):
    """
    Look at a single C function an gather the information for Klee.

    The FuncVisitor visits each function once and then visits all of the variable
    definitions in the function definition in order to get their names and types.
    """

    def __init__(self, logger) -> None:
        """Create a new instance of FuncVisitor."""
        self.logger = logger
        self.generator = c_generator.CGenerator()
        self.vars: Dict[str, list] = defaultdict(list)
        self.types: Dict[str, str] = defaultdict(str)
        super().__init__()

    def define_var(self, name: str, declaration: str, varname: str):
        """Look at a single variable declaration in the C code."""
        self.vars[name].append((f"{declaration};\n", varname))

    # pylint: disable=C0103
    # disable invalid-name as this name is required by the library.
    def visit_FuncDef(self, node):
        """
        Determine all of the arguments to functions.

        This function is called once for each function in the C source code.
        It determines all of the argument types needed to call the function.
        """
        # Node is a pycparser.c_ast.funcdef
        args = node.decl.type.args  # type ParamList.
        return_type = node.decl.type.type.type.names[0]
        self.logger.i_msg(f"Looking at {node.decl.name}()")
        self.types[node.decl.name] = return_type
        if args is not None:
            params = args.params  # List of TypeDecl.
            for i, param in enumerate(params):
                self.logger.d_msg(f"\tParameter {i}: Name: {param.name}")
                print(f"Here is the parameter: {param.name}")
                self.define_var(node.decl.name, self.generator.visit(param), param.name)
        else:
            self.logger.d_msg(f"\t{node.decl.name} has no parameters.")


class KleeUtils:
    """
    KleeUtils is used to make working with KLEE much easier in the REPL.

    This is used to parse C code and generate new Klee-compatible
    source code in order to make static analysis much easier.
    """

    def __init__(self, logger) -> None:
        """Create a new instance of KleeUtils."""
        self.logger = logger

    def show_func_defs(self, filename: str):
        """
        Generate the set of klee-compatible files.

        Create a new set of files based on an existing file that are formatted properly
        to work with klee.
        """
        self.logger.d_msg(f"Going to parse file {filename}")
        ast = parse_file(filename, use_cpp=True, cpp_path='gcc',
                         cpp_args=['-E', r'-Iutils/fake_libc_include'])
        self.logger.d_msg(f"Going to visit functions.")
        func_visitor = FuncVisitor(self.logger)
        func_visitor.visit(ast)

        uuids: Set[Any] = set()  # TODO: change type
        klee_formatted_files = dict()
        for func_name in func_visitor.vars.keys():
            variables = [list(v) for v in func_visitor.vars[func_name]]
            var_names = []

            file_str = ""
            file_str += "#include <klee/klee.h>\n"
            file_str += f"#include <{filename}>\n"
            file_str += "#define SIZE 10\n"
            file_str += "int main() {\n"
            for var in variables:
                if var[0][-4:] == "[];\n":
                    var[0] = var[0].replace("[]", "[SIZE]")

                file_str += "\n"

                file_str += f"\t{var[0]}"

                name = uuid.uuid4()
                while name in uuids:
                    name = uuid.uuid4()
                uuids.add(name)

                file_str += f"\tklee_make_symbolic(&{var[1]}," + \
                            f" sizeof({var[1]}), \"{str(name).replace('-', '')}\");\n"

                var_names.append(var[1])

            if func_visitor.types[func_name] == 'void':
                file_str += f"\t{func_name}({', '.join(var_names)});\n"
                file_str += "\treturn 0;\n"
            else:
                file_str += f"\treturn {func_name}({', '.join(var_names)});\n"
            file_str += "}\n"
            klee_formatted_files[func_name] = file_str
        return klee_formatted_files
