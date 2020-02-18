from pycparser import c_parser, c_ast, parse_file, c_generator
from collections import defaultdict
import uuid 

class FuncVisitor(c_ast.NodeVisitor): 
    def __init__(self, logger): 
        self.logger = logger
        self.generator = c_generator.CGenerator()
        self.vars = defaultdict(list)
        super().__init__() 

    def define_var(self, name: str, declaration: str, varname: str): 
        self.vars[name].append((f"{declaration};\n", varname))

    def visit_FuncDef(self, node):
        # Node is a pycparser.c_ast.funcdef
        args = node.decl.type.args # type ParamList
        self.logger.i(f"Looking at {node.decl.name}()")
        if args is not None:
            params = args.params # List of TypeDecl 
            for i, param in enumerate(params): 
                self.logger.d(f"\tParameter {i}: Name: {param.name}")
                print(f"HERE IS THE PARAM: {param.name}")
                self.define_var(node.decl.name, self.generator.visit(param), param.name)            
        else: 
            self.logger.d(f"\t{node.decl.name} has no parameters.")

class KleeUtils:
    def __init__(self, logger): 
        self.logger = logger
    
    def show_func_defs(self, filename: str):
        self.logger.d(f"Going to parse file {filename}")
        try:
            ast = parse_file(filename, use_cpp=True, cpp_path='gcc', cpp_args=['-E', r'-Iutils/fake_libc_include'])
            self.logger.d(f"Going to visit functions.")
            v = FuncVisitor(self.logger)
            v.visit(ast)
        except Exception as e:
            self.logger.i(f"Here is the error {e}.") 
            self.logger.i(f"Could not parse file {filename}")
            return None

        UUIDS = set()
        kleeFormattedFiles = dict()
        for funcName in v.vars.keys():
            variables = v.vars[funcName]
            varNames = []

            f = ""
            f += "#include <klee/klee.h>\n"
            f += f"#include <{filename}>\n"
            f += "int main() {\n"
            for var in variables:
                f += "\n"

                f += f"\t{var[0]}"

                name = uuid.uuid4()
                while name in UUIDS:
                    name = uuid.uuid4()
                UUIDS.add(name)

                f += f"\tklee_make_symbolic(&{var[1]}, sizeof({var[1]}), \"{str(name).replace('-', '')}\");\n"

                varNames.append(var[1])

            f += f"\treturn {funcName}({', '.join(varNames)});\n"
            f += "}\n"
            kleeFormattedFiles[funcName] = f
        return kleeFormattedFiles