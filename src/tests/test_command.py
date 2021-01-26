"""Test the commands of the REPL."""
import unittest
from typing import Union, cast

import core.command as command
import core.command_data as command_data
from core.command import Options
from core.log import Log
from graph.control_flow_graph import ControlFlowGraph as CFG
from graph.graph import EdgeListGraph, EdgeListType
from tests.unit_utils import captured_output

# pylint does not understand decorators :(
# pylint: disable=no-value-for-parameter
# pylint: disable=W0511
# pylint: disable=W0612


class TestController(unittest.TestCase):
    """Test the methods of the Controller object."""

    def setUp(self) -> None:
        """Create a new instance of the Controller."""
        self.controller = command.Controller(Log(display_output=False))

    def test_graph_generator_names(self) -> None:
        """Check that we can get the names of all the files we can convert."""
        names = self.controller.get_graph_generator_names()
        expected_names = [".cpp", ".c", ".jar", ".class", ".java", ".py"]
        self.assertEqual(list(names), expected_names)

    def test_get_graph_generator(self) -> None:
        """Check that we can get the converter from the file extension."""
        converter = self.controller.get_graph_generator(".py")
        self.assertEqual(converter.name(), "Python")


class TestCommandMultithreading(unittest.TestCase):
    """Test the multithreading implementation of the command object."""

    def test_init(self) -> None:
        """Test the initialization with multithreading."""
        with captured_output() as (out, err):
            command.Command("", False, True, None)
        expected_msg = "MULTITHREADING ENABLED"
        self.assertTrue(expected_msg in out.getvalue())
        self.assertTrue(len(err.getvalue().strip()) == 0)


class TestCommandInvalid(unittest.TestCase):
    """Test each command with invalid inputs."""

    def setUp(self) -> None:
        """Create a new instance of the Command object without the wrapping object."""
        self.command = command.Command("", False, False, None)
        self.opts = Options()

    # ==== do_to_klee_format =====
    def test_to_klee_format_invalid_type(self) -> None:
        """
        Test the klee format command with an invalid input.

        Verify that we get the correct error when attempting to convert non-C code into
        a klee-compatible format.
        """
        with captured_output() as (out, err):
            # self.command.do_to_klee_format("examplefile.wrongextension")
            pass

    def test_to_klee_format_nonexistant_file(self) -> None:
        """
        Test the klee format command with an invalid input.

        Test that if we call klee_format for a file name refering to a
        non-existant file, we get an error.
        """
        with captured_output() as (out, err):
            # self.command.do_to_klee_format("nonexistantfile.c")
            pass

    # ==== Test do_klee_replay ====
    def test_klee_replay_invalid_type(self) -> None:
        """
        Test the klee replay command with an invalid input.

        See if we get the correct error when we try to call klee_replay
        on a file with the wrong extension.
        """
        with captured_output() as (out, err):
            self.command.do_klee_replay(self.opts, "somefile.wrongextension")

    def test_klee_replay_nonexistant_file(self) -> None:
        """Test that if we call klee_replay on a nonexistant file, we get the correct error."""
        with captured_output() as (out, err):
            self.command.do_klee_replay(self.opts, "nonexistantFile.ktest")

    # ==== Test do_convert ====
    def test_convert_nonexistant_file(self) -> None:
        """
        Test convert command given nonexistant file.

        Verify that we get the proper error when we try to call
        convert on a file that does not exist.
        """
        with captured_output() as (out, err):
            # self.command.do_convert("somefile.py")
            pass

    def test_convert_invalid_type(self) -> None:
        """
        Test convert command given invalid type.

        Verify that we get the proper error when we try to call convert
        on a file containing source code of a type we do not know how to
        convert.
        """
        with captured_output() as (out, err):
            # self.command.do_convert("testfile.invalidextension")
            pass

    def test_show_metric_invalid(self) -> None:
        """
        Test show command with inexistant object.

        Verify that we get the correct error when we try to call show for
        an inexistant object.
        """
        with captured_output() as (out, err):
            self.command.do_show(self.opts, command_data.ObjTypes.METRIC.value, "foo")

    def test_list_invalid_type(self) -> None:
        """
        Test list command with invalid type.

        Verify that if we pass in an object type that does not exist, the list command
        will show the correct error.
        """
        with captured_output() as (out, err):
            self.command.do_list(self.opts, "Somerandomtype")


class TestCommandKlee(unittest.TestCase):
    """This class is used to test all klee-related commands given valid inputs."""

    def setUp(self) -> None:
        """
        Create a new instance of the command object without the wrapping object.

        Note that in these tests we use the Command object directly.
        """
        self.command = command.Command("", False, False, None)
        self.opts = Options()

    # ==== do_to_klee_format =====
    def test_to_klee_format_valid(self) -> None:
        """Verify that we can convert a valid file to a KLEE-compatible format."""
        with captured_output() as (out, err):
            self.command.do_to_klee_format(self.opts, "examplefile.c")
        self.assertTrue(len(err.getvalue()) == 0)

    # ==== Test do_klee_to_bc =====
    def test_klee_to_bc(self) -> None:
        """See if we can convert a klee formatted file to a .bc file."""
        with captured_output() as (out, err):
            pass
        self.assertTrue(len(err.getvalue()) == 0)

    # ==== Test do_klee_replay ====
    def test_klee_replay_valid(self) -> None:
        """Verify that tests can be replayed given a valid test file generated by KLEE."""
        with captured_output() as (out, err):
            self.command.do_klee_replay(self.opts, "samplefile.ktest")
        self.assertTrue(len(err.getvalue()) == 0)


class TestCommand(unittest.TestCase):
    """Test each command with valid inputs."""

    valid_commands: dict[str, tuple[int, Union[float, int]]] = {}

    @classmethod
    def setUpClass(cls) -> None:
        """
        Register all of the known commands.

        Create a dictionary that maps each command name to a 2-tuple that has the minimum number
        of arguments to the maximum number of arguments.
        """
        cls.valid_commands = {
            "klee_replay": (1, 1),
            "convert": (1, float('inf')),
            "list": (1, 1),
            "metrics": (1, 1),
            "show": (2, 2),
            "klee_to_bc": (0, 0),
            "to_klee_format": (1, 1),
            "klee": (1, 1),
            "export": (2, 2),
            "delete": (2, 2),
            "import": (1, float('inf')),
            "cd": (1, 1),
            "ls": (0, 0),
            "mv": (2, 2),
            "rm": (1, 1),
            "mkdir": (1, 1),
            "pwd": (1, 1),
        }

    def setUp(self) -> None:
        """
        Create a new instance of the Command object without the wrapping object.

        Note that in these tests we use the Command object directly.
        """
        self.command = command.Command(curr_path="/app/code/tests/dotFiles", debug_mode=False,
                                       multi_threaded=False, repl_wrapper=None)
        self.opts = Options()

    def test_num_args_invalid(self) -> None:
        """Check that commands throw errors when given an incorrect number of arguments."""
        with captured_output() as (out, err):
            for valid_command in self.valid_commands:
                function_name = "do_" + valid_command
                method = getattr(self.command, function_name)
                min_num_args = self.valid_commands[valid_command][0]
                max_num_args = self.valid_commands[valid_command][1]
                if min_num_args > 0:
                    # res = method("")
                    # TODO: assert that result is none
                    pass
                if max_num_args != float('inf'):
                    # res = method("a " * (max_num_args + 1))
                    pass
                    # TODO: assert that the result is none

    # === Test do_quit ===
    # pylint: disable=E1121
    def test_quit(self) -> None:
        """Check that exiting the REPL works."""
        with self.assertRaises(SystemExit):
            self.command.do_quit(self.opts)

    # === directory functions. ===
    # pylint: disable=E1121
    def test_directories(self) -> None:
        """Check that all functions related to working with directories work."""
        with captured_output() as (out, err):
            self.command.do_pwd(self.opts)

        self.assertTrue("/app/code/tests/dotFiles" in out.getvalue())

        with captured_output() as (out, err):
            self.command.do_ls(self.opts)

        expected_files = ["dotTest.dot", "testgraph.dot", "testsimple.dot"]
        self.assertTrue(all(check_file in out.getvalue() for check_file in expected_files))

        with captured_output() as (out, err):
            self.command.do_cd(self.opts, "/app/code/tests/")
            out.truncate(0)
            out.seek(0)
            self.command.do_pwd(self.opts)

        self.assertTrue("/app/code/tests" in out.getvalue())
        self.assertTrue(len(err.getvalue()) == 0)

        # self.command.do_mkdir("")
        # self.command.do_rm("")
        # self.command.do_mv("")

    # ==== Test do_convert =====
    def test_convert_valid_type(self) -> None:
        """
        Test convert command with a file of source code.

        See if we can convert a file containing source code of a type
        we recognize to a Graph representing its control flow.
        """
        with captured_output() as (out, err):
            # self.command.do_convert("testfile.py") # TODO
            pass

    # TODO: convert recursive

    # === Test do_metrics ===
    def test_do_metrics_valid(self) -> None:
        """Compute metrics for stored graphs."""
        # TODO
        with captured_output() as (out, err):
            self.command.do_metrics(self.opts, "*")
            self.command.do_metrics(self.opts, "foo")

        self.assertTrue(len(out.getvalue()) == 0)
        self.assertTrue(len(err.getvalue()) == 0)

    # ==== Test do_show =====
    def test_show_metric_valid(self) -> None:
        """
        Check show command with metric of a specific name.

        Verify that calling the show command with a valid metric name will
        display the metric value in the REPL.
        """
        self.command.data.bc_files["foo"] = b"bar"
        self.command.data.klee_formatted_files["foo"] = "bar"
        self.command.data.klee_stats["foo"] = self.command.data.klee_stat(tests=0, paths=0,
                                                                          instructions=0, delta_t=0,
                                                                          timeout=0)
        with captured_output() as (out, err):
            self.command.data.metrics["foo"] = [("123", 1), ("123", 1)]
            self.command.do_show(self.opts, command_data.ObjTypes.METRIC.value,
                                 "foo")
        self.assertTrue(len(err.getvalue()) == 0)
        # TODO
        self.assertTrue(len(out.getvalue()) != 0)

        with captured_output() as (out, err):
            self.command.do_show(self.opts, command.ObjTypes.KLEE.value,
                                 "foo")
        self.assertTrue(len(err.getvalue()) == 0)
        self.assertTrue(len(out.getvalue()) != 0)

        with captured_output() as (out, err):
            self.command.do_show(self.opts, command.ObjTypes.ALL.value, "")
        self.assertTrue(len(err.getvalue()) == 0)
        self.assertTrue(len(out.getvalue()) != 0)

    def test_show_graph_valid(self) -> None:
        """
        Check show command with a graph of specific name.

        Verify that we get the correct output graw if we call the show function
        for a valid graph name.
        """
        with captured_output() as (out, err):
            graph = EdgeListGraph(cast(EdgeListType, []), 1)
            self.command.data.graphs["foo"] = CFG(graph)
            self.command.do_show(self.opts, command.ObjTypes.GRAPH.value, "foo")

    def test_show_klee(self) -> None:
        """Check that we can show klee objects."""
        with captured_output() as (out, err):
            self.command.do_show(self.opts, command_data.ObjTypes.KLEE_BC.value, "foo")
        with captured_output() as (out, err):
            self.command.do_show(self.opts, command_data.ObjTypes.KLEE_STATS.value, "foo")
        with captured_output() as (out, err):
            self.command.do_show(self.opts, command_data.ObjTypes.KLEE_FILE.value, "foo")
        with captured_output() as (out, err):
            self.command.do_show(self.opts, command_data.ObjTypes.KLEE.value, "foo")

    def test_show_all_types_valid(self) -> None:
        """
        Check show command with wildcard operator for type.

        Verify that we can use the wildcard operator to show all objects (objects
        of all types) for a given name.
        """
        with captured_output() as (out, err):
            self.command.data.graphs["foo"] = CFG(EdgeListGraph(cast(EdgeListType, []), 1))
            self.command.data.metrics["foo"] = [("123", 1)]
            self.command.do_show(self.opts, command_data.ObjTypes.ALL.value, "foo")

    def test_show_all_names_valid(self) -> None:
        """
        Check show command with wildcard operator for name.

        Verify that we can use the wildcard operator to show all objects
        of a given type.
        """
        with captured_output() as (out, err):
            self.command.data.graphs["foo"] = CFG(EdgeListGraph(cast(EdgeListType, []), 1))
            self.command.data.graphs["bar"] = CFG(EdgeListGraph(cast(EdgeListType, []), 1))
            self.command.do_show(self.opts, command_data.ObjTypes.GRAPH.value,
                                 command.ObjTypes.ALL.value)

    # ==== Test do_list =====
    def test_list_graphs(self) -> None:
        """
        Check list command with graph type argument.

        Verify that calling list with graph type displays all of the graphs the
        REPL knows about.
        """
        with captured_output() as (out, err):
            self.command.do_list(self.opts, command_data.ObjTypes.GRAPH.value)

    def test_list_metrics(self) -> None:
        """
        Check list command with metric type argument.

        Verify that calling list with metric type displays all of the metrics the
        REPL knows about.
        """
        with captured_output() as (out, err):
            self.command.do_list(self.opts, command_data.ObjTypes.METRIC.value)

        # TODO
        self.assertTrue(len(err.getvalue()) == 0)
        self.assertTrue(len(out.getvalue()) != 0)

    def test_list_klee(self) -> None:
        """Check list command with klee arguments."""
        # TODO
        with captured_output() as (out, err):
            self.command.do_list(self.opts, command_data.ObjTypes.KLEE_BC.value)
        self.assertTrue(len(err.getvalue()) == 0)
        self.assertTrue(len(out.getvalue()) != 0)

        with captured_output() as (out, err):
            self.command.do_list(self.opts, command_data.ObjTypes.KLEE_STATS.value)
        self.assertTrue(len(err.getvalue()) == 0)
        self.assertTrue(len(out.getvalue()) != 0)

        with captured_output() as (out, err):
            self.command.do_list(self.opts, command_data.ObjTypes.KLEE_FILE.value)
        self.assertTrue(len(err.getvalue()) == 0)
        self.assertTrue(len(out.getvalue()) != 0)

        with captured_output() as (out, err):
            self.command.do_list(self.opts, command_data.ObjTypes.KLEE.value)
        self.assertTrue(len(err.getvalue()) == 0)
        self.assertTrue(len(out.getvalue()) != 0)

    def test_list_all(self) -> None:
        """
        Check list with wildcard.

        Verify that we can use the wildcard operator to list objects of all types through
        the list command.
        """
        with captured_output() as (out, err):
            self.command.do_list(self.opts, command_data.ObjTypes.ALL.value)

    # ==== Test do_delete ======
    def test_delete_graph_valid(self) -> None:
        """
        Check delete graph.

        Verify that if we call the delete command with the name of a Graph that the REPL
        knows about, that Graph will be deleted from the REPL.
        """
        with captured_output() as (out, err):
            obj_type = command.ObjTypes.GRAPH
            obj_name = "sample_graph"
            self.command.data.graphs['sample_graph'] = CFG(EdgeListGraph(cast(EdgeListType, []), 1))
            self.command.data.graphs['sample_graph'] = CFG(EdgeListGraph(cast(EdgeListType, []), 1))
            self.command.data.metrics['sample_graph'] = [('abc', 1)]
            self.command.do_delete(self.opts, str(obj_type), str(obj_name))

    def test_delete_metric_valid(self) -> None:
        """
        Check delete metric.

        Verify that if we call the delete command with the name of a Graph that the REPL does
        not know about, we get the correct error.
        """
        with captured_output() as (out, err):
            obj_type = command.ObjTypes.METRIC
            obj_name = "sample_metric"
            graph = CFG(EdgeListGraph(cast(EdgeListType, []), 1))
            self.command.data.metrics['sample_metric'] = [('foo', 1)]
            self.command.data.metrics['sample_metric'] = [('bar', 1)]
            self.command.data.graphs['sample_metric'] = graph
            self.command.do_delete(self.opts, str(obj_type), str(obj_name))

    def test_delete_all_types_valid(self) -> None:
        """
        Check wildcard in delete.

        Verify that we can use the wildcard operator with the delete command to delete objects all
        all types matching a given name.
        """
        with captured_output() as (out, err):
            obj_type = command.ObjTypes.ALL
            obj_name = "sample_name"
            graph = CFG(EdgeListGraph(cast(EdgeListType, []), 1))
            self.command.data.graphs['sample_name'] = graph
            self.command.data.metrics['sample_name'] = [('foo', 1)]

            self.command.data.graphs['sample_name'] = graph
            self.command.data.metrics['sample_name'] = [('b', 1)]
            self.command.do_delete(self.opts, str(obj_type), str(obj_name))

    def test_delete_all_names_valid(self) -> None:
        """Verify that we can use the wildcard operator to delete all objects of a given type."""
        with captured_output() as (out, err):
            # Delete * name
            obj_type = command.ObjTypes.GRAPH
            obj_name = "*"
            self.command.data.graphs['sample_name'] = CFG(EdgeListGraph(cast(EdgeListType, []), 1))
            self.command.data.graphs['sample_name'] = CFG(EdgeListGraph(cast(EdgeListType, []), 1))
            self.command.data.graphs['sample_name'] = CFG(EdgeListGraph(cast(EdgeListType, []), 1))
            self.command.data.metrics['sample_name'] = [("123", 1)]

            self.command.do_delete(self.opts, str(obj_type), str(obj_name))

    # TODO: test invalid


if __name__ == '__main__':
    unittest.main()
