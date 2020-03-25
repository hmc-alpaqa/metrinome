"""
This class knows how to convert from java source code to graph objects.
"""

from graph import Graph
from lang_to_cfg.javaextractor.app import App # type: ignore

class JavaConvert():
    """
    JavaConvert is able to convert java files to graphs
    """
    def __init__(self) -> None:
        """
        Create a new Java coverter.
        """

    # pylint: disable=R0201
    def to_graph(self, filename: str, file_extension: str) -> Graph:
        """
        Creates a CFG from a Java source file.
        """
        if file_extension in [".java", ".class"]:
            converter = App((filename + file_extension).strip(), export=False)
            converter.run_live(jar=False)
            return Graph([], [], 0, 1)

        converter = App((filename + file_extension).strip(), export=False)
        converter.run_live(jar=True)
        return Graph([], [], 0, 1)
