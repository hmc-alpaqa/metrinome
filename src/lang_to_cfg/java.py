"""This class knows how to convert from java source code to graph objects."""
import sys
import os
sys.path.append("/app/code/")
from typing import Dict, Optional
from glob2 import glob  # type: ignore
from graph import Graph, GraphType
from env import Env
from lang_to_cfg import converter  # type: ignore
from log import Log


class JavaConvert(converter.ConverterAbstract):
    """
    JavaConvert is able to convert java files to graphs.

    Interacts with the java program that extracts CFGs from Java source code.
    """

    # pylint: disable=super-init-not-called
    def __init__(self, logger: Log) -> None:
        """Create a new Java converter."""
        self.logger: Log = logger
        self.output_folder = Env.TMP_DOT_PATH

    def name(self) -> str:
        """Get the name of the Java converter."""
        return "Java"

    # pylint: disable=R0201
    def to_graph(self, filename: str, file_extension: str) -> Optional[Dict[str, Graph]]:
        """Create a CFG from a Java source file."""
        Env.clean_temps()

        check_ending = filename.endswith('sources') or filename.endswith('javadoc') or \
            filename.endswith('tests')
        if file_extension == '.jar' and check_ending:
            return None

        path = ""
        fname = filename + file_extension
        self.logger.v_msg(f"processing {fname}")

        if file_extension == ".jar":
            self.runcmd(f"jar xf {fname}", cwd=Env.TMP_PATH)
            fname = Env.TMP_PATH
            path = f"{Env.TMP_DOT_PATH}/tmp/*.dot"

        if file_extension == ".java":
            self.runcmd(f"javac {fname} -d {Env.TMP_PATH}")
            name = os.path.basename(filename)
            fname = f"{Env.TMP_PATH}/{name}.class"

        output_path = Env.get_output_path(fname)
        cmd = f"java -jar {Env.CFG_EXTRACTOR_JAR} -i {fname} -o {output_path}"
        self.runcmd(cmd, cwd="/app/code")
        self.logger.d_msg("Generated .dot files")

        graphs = {}
        if path == "":
            path = f"{output_path}/*.dot"

        dot_files = glob(path)
        print(dot_files)
        for file in dot_files:
            graphs[file] = Graph.from_file(file, False, GraphType.EDGE_LIST)
        Env.clean_temps()
        return graphs
