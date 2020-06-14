"""This class knows how to convert from java source code to graph objects."""
import sys
sys.path.append("/app/code/")
sys.path.append("/app/code/lang_to_cfg")
from typing import Dict, Optional
from os.path import basename
from glob2 import glob  # type: ignore
from graph import Graph, GraphType
from env import Env
from converter import ConverterAbstract  # type: ignore


class JavaConvert(ConverterAbstract):
    """
    JavaConvert is able to convert java files to graphs.

    Interacts with the java program that extracts CFGs from Java source code.
    """

    def __init__(self, logger) -> None:
        """Create a new Java coverter."""
        self.logger = logger
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

        filename += file_extension
        self.logger.v_msg(f"processing {filename}")
        if not (file_extension in [".java", ".class"]):
            self.runcmd(f"jar xf {filename}", cwd=Env.TMP_PATH)
            filename = Env.TMP_PATH

        output_path = Env.get_output_path(basename(filename))
        self.runcmd(f"java -jar {Env.CFG_EXTRACTOR_JAR} -i {filename} -o {output_path}")
        self.logger.d_msg("Generated .dot files")
        graphs = {}
        dot_files = glob(f"{Env.TMP_DOT_PATH}/tmp/*.dot")
        for file in dot_files:
            graphs[file] = Graph.from_file(file, False, GraphType.EDGE_LIST)
        Env.clean_temps()
        return graphs
