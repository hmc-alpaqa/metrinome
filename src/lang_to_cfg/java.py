"""This class knows how to convert from java source code to graph objects."""
import sys
sys.path.append("/app/code/")
from graph import Graph
from log import Log
from env import Env
from typing import Dict, Optional
import shlex
from subprocess import Popen, PIPE
from os.path import basename

class JavaConvert():
    """
    JavaConvert is able to convert java files to graphs.
    
    Interacts with the java program that extracts CFGs from Java source code.
    """

    def __init__(self, logger) -> None:
        """Create a new Java coverter."""
        self.log = logger
        self.output_folder = Env.OUTPUT_PATH

    def name(self) -> str:
        return "Java"

    # pylint: disable=R0201
    def to_graph(self, filename: str, file_extension: str) -> Optional[Dict[str, Graph]]:
        """Create a CFG from a Java source file."""
        Env.clean_temps()

        if file_extension == '.jar' and (filename.endswith('sources') \
            or filename.endswith('javadoc') or filename.endswith('tests')):
            return

        filename += file_extension
        self.log.v_msg(f"processing {filename}")
        if not (file_extension in [".java", ".class"]):
            self.runcmd(f"jar xf {filename}", cwd=Env.TMP_PATH)
            filename = Env.TMP_PATH

        self.run_cfg_extractor(filename)

    def run_cfg_extractor(self, input_class):
        """Run the java program that will extract the CFG from Java classes."""
        output_path = Env.get_output_path(basename(input_class))
        self.runcmd(f"java {Env.CFG_EXTRACTOR} -i {input_class} -o {output_path}")

    def runcmd(self, cmd, cwd=None):
        """Run a command in the shell."""
        self.log.d_msg(f"cmd: {cmd}\n  with params: cwd={cwd}")
        process = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE, cwd=cwd, shell=False)
        out, err = process.communicate()
        if out:
            self.log.d_msg(f"cmd output: {out}")
        if err:
            self.log.d_msg(f"cmd output: {err}")

        return out, err

    def __run_cfg_extractor_live(self, input_class):
            """Run the java program that will extract the CFG from Java classes."""
            project = Env.get_basename(input_class)
            output_path = Env.get_output_path(project)
            self.shell.clean_cmd(output_path)
            if self.export:
                pass
            #    additional_cmd = f"-i {input_classes} -o {output_path} -p test"
            else:
                pass
                # additional_cmd = f"-i {input_classes} -p test"
            cmd = f"java -jar {Env.CFG_EXTRACTOR} -i {input_class.strip()}" + \
                f" -o {output_path.strip()}"
            print(f"===== HERE IS THE COMMAND === {cmd}")
            self.shell.runcmd(cmd)
