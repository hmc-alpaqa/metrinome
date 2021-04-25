"""This class knows how to convert from java source code to graph objects."""
import os
from typing import Optional

from glob2 import glob  # type: ignore

from core.env import Env, KnownExtensions
from core.log import Log
from graph.control_flow_graph import ControlFlowGraph, Metadata
from graph.graph import EdgeListGraph
from lang_to_cfg import converter


class JavaConvert(converter.ConverterAbstract):
    """
    JavaConvert is able to convert java files to graphs.

    Interacts with the java program that extracts CFGs from Java source code.
    """

    # pylint: disable=super-init-not-called
    def __init__(self, logger: Log) -> None:
        """Create a new Java converter."""
        self.logger: Log = logger
        self._output_folder = Env.TMP_DOT_PATH
        self._input_folder = Env.TMP_PATH

    def name(self) -> str:
        """Get the name of the Java converter."""
        return "Java"

    # pylint: disable=R0201
    def to_graph(self, filename: str, file_extension: str) -> Optional[dict[str, ControlFlowGraph]]:
        """Create a CFG from a Java source file."""
        #Env.clean_temps()

        check_ending = filename.endswith('sources') or filename.endswith('javadoc') or \
            filename.endswith('tests')
        if file_extension == '.jar' and check_ending:
            return None

        path = ""
        fname = filename + file_extension
        self.logger.v_msg(f"processing {fname}")

        if file_extension == ".jar":
            self.runcmd(f"jar xf {fname}", cwd=self._input_folder)
            fname = self._input_folder
            path = f"{self._output_folder}/tmp/*.dot"

        if file_extension == ".java":
            self.runcmd(f"javac {fname} -source 1.7 -target 1.7 -d {self._input_folder}")
            name = os.path.basename(filename)
            fname = f"{self._input_folder}/{name}.class"

        output_path = Env.get_output_path(fname)
        cmd = f"java -cp {Env.CFG_EXTRACTOR_JAR} extractor.Extractor -i {fname} -o {output_path}"
        if (err := self.runcmd(cmd, cwd="/app/code")[1]) is not None:
            error = str(err)
            if "FileNotFoundException" in error:
                self.logger.e_msg(f"Java was unable to generate {fname}")
                return None

        self.logger.d_msg("Generated .dot files")

        graphs = {}
        if path == "":
            path = f"{output_path}/*.dot"

        dot_files = glob(path)
        for file in dot_files:
            graphs[file] = ControlFlowGraph.from_file(file, EdgeListGraph,
                                                      [Metadata.with_language(KnownExtensions.Java)])
        Env.clean_temps()
        return graphs
