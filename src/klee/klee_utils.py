"""Handles work with klee, which does symbollic execution and test generation of C code."""

import uuid
from collections import defaultdict
from typing import DefaultDict, Dict, List, Set, Tuple

from pycparser import c_ast, c_generator, parse_file  # type: ignore

from core.log import Log


class FuncVisitor(c_ast.NodeVisitor):
    """
    Look at a single C function an gather the information for Klee.

    The FuncVisitor visits each function once and then visits all of the variable
    definitions in the function definition in order to get their names and types.
    """

    def __init__(self, logger: Log) -> None:
        """Create a new instance of FuncVisitor."""
        self.logger = logger
        self._generator = c_generator.CGenerator()
        self._vars: DefaultDict[str, List[Tuple[str, str]]] = defaultdict(list)
        self._types: DefaultDict[str, str] = defaultdict(str)
        super().__init__()

    def define_var(self, name: str, declaration: str, varname: str) -> None:
        """Look at a single variable declaration in the C code."""
        self._vars[name].append((f"{declaration};\n", varname))

    # pylint: disable=C0103
    # disable invalid-name as this name is required by the library.
    def visit_FuncDef(self, node: c_ast.Node) -> None:
        """
        Determine all of the arguments to functions.

        This function is called once for each function in the C source code.
        It determines all of the argument types needed to call the function.
        """
        # Node is a pycparser.c_ast.funcdef
        args = node.decl.type.args  # type ParamList.
        return_type = node.decl.type.type.type.names[0]
        self.logger.i_msg(f"Looking at {node.decl.name}()")
        self._types[node.decl.name] = return_type
        if args is not None:
            params = args.params  # List of TypeDecl.
            for i, param in enumerate(params):
                self.logger.d_msg(f"\tParameter {i}: Name: {param.name}")
                self.define_var(node.decl.name, self._generator.visit(param), param.name)
        else:
            self.logger.d_msg(f"\t{node.decl.name} has no parameters.")


class KleeUtils:
    """
    KleeUtils is used to make working with KLEE much easier in the REPL.

    This is used to parse C code and generate new Klee-compatible
    source code in order to make static analysis much easier.
    """

    def __init__(self, logger: Log) -> None:
        """Create a new instance of KleeUtils."""
        self.logger = logger

    def show_func_defs(self, filename: str, size: int = 10,
                       optimized: bool = False) -> Dict[str, str]:
        """
        Generate the set of klee-compatible files.

        Create a new set of files based on an existing file that are formatted properly
        to work with klee.
        """
        self.logger.d_msg(f"Going to parse file {filename}")
        if optimized:
            cppargs = ['-O3', '-nostdinc', '-E', r'-I/app/pycparser/utils/fake_libc_include']
        else:
            cppargs = ['-nostdinc', '-E', r'-I/app/pycparser/utils/fake_libc_include']
        ast = parse_file(filename, use_cpp=True, cpp_path='gcc', cpp_args=cppargs)
        self.logger.d_msg("Going to visit functions.")
        func_visitor = FuncVisitor(self.logger)
        func_visitor.visit(ast)

        uuids: Set[uuid.UUID] = set()
        klee_formatted_files = dict()
        for func_name in func_visitor._vars.keys():
            variables = [list(v) for v in func_visitor._vars[func_name]]
            var_names = []

            file_str = "#include <klee/klee.h>\n"
            file_str += f"#include <{filename}>\n"
            file_str += f"#define SIZE {size}\n"
            file_str += "int main() {\n"
            for var in variables:
                if var[0][-4:] == "[];\n":
                    var[0] = var[0].replace("[]", "[SIZE]")

                file_str += f"\n\t{var[0]}"

                name = uuid.uuid4()
                while name in uuids:
                    name = uuid.uuid4()
                uuids.add(name)

                file_str += f"\tklee_make_symbolic(&{var[1]}," + \
                            f" sizeof({var[1]}), \"{str(name).replace('-', '')}\");\n"

                var_names.append(var[1])

            if func_visitor._types[func_name] == 'void':
                file_str += f"\t{func_name}({', '.join(var_names)});\n"
                file_str += "\treturn 0;\n"
            else:
                file_str += f"\treturn {func_name}({', '.join(var_names)});\n"
            file_str += "}\n"
            klee_formatted_files[func_name] = file_str
        return klee_formatted_files
