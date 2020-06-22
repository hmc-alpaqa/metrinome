"""Test the commands of the REPL."""
import unittest
import sys
sys.path.append("/app/code/")
import command
from tests.unit_utils import captured_output

# pylint does not understand decorators :(
# pylint: disable=no-value-for-parameter


class TestCommandInvalid(unittest.TestCase):
    """Test each command with invalid inputs."""

    def setUp(self) -> None:
        """Create a new instance of the Command object without the wrapping object."""
        self.command = command.Command("", False, False, None)

    # ==== Test do_analyze ====
    # def test_analyze_invalid_name(self):
    #     """Test that we get an error when we pass a name for an object that does not exist."""
    #     with captured_output() as (out, err):
    #         self.command.do_analyze("invalid_name")
    #         print(out, err)

    # ==== do_to_klee_format =====
    def test_to_klee_format_invalid_type(self) -> None:
        """
        Test the klee format command with an invalid input.

        Verify that we get the correct error when attempting to convert non-C code into
        a klee-compatible format.
        """
        with captured_output() as (out, err):
            # self.command.do_to_klee_format("examplefile.wrongextension")
            print(out, err)

    def test_to_klee_format_nonexistant_file(self) -> None:
        """
        Test the klee format command with an invalid input.

        Test that if we call klee_format for a file name refering to a
        non-existant file, we get an error.
        """
        with captured_output() as (out, err):
            # self.command.do_to_klee_format("nonexistantfile.c")
            print(out, err)

    # ==== Test do_klee_replay ====
    def test_klee_replay_invalid_type(self) -> None:
        """
        Test the klee replay command with an invalid input.

        See if we get the correct error when we try to call klee_replay
        on a file with the wrong extension.
        """
        with captured_output() as (out, err):
            self.command.do_klee_replay("somefile.wrongextension")
            print(out, err)

    def test_klee_replay_nonexistant_file(self) -> None:
        """Test that if we call klee_replay on a nonexistant file, we get the correct error."""
        with captured_output() as (out, err):
            self.command.do_klee_replay("nonexistantFile.ktest")
            print(out, err)

    # ==== Test do_convert ====
    def test_convert_nonexistant_file(self) -> None:
        """
        Test convert command given nonexistant file.

        Verify that we get the proper error when we try to call
        convert on a file that does not exist.
        """
        with captured_output() as (out, err):
            # self.command.do_convert("somefile.py") # TODO
            print(out, err)

    def test_convert_invalid_type(self) -> None:
        """
        Test convert command given invalid type.

        Verify that we get the proper error when we try to call convert
        on a file containing source code of a type we do not know how to
        convert.
        """
        with captured_output() as (out, err):
            # self.command.do_convert("testfile.invalidextension")
            print(out, err)

    def test_show_metric_invalid(self) -> None:
        """
        Test show command with inexistant object.

        Verify that we get the correct error when we try to call show for
        an inexistant object.
        """
        with captured_output() as (out, err):
            self.command.do_show(command.ObjTypes.METRIC.value + " foo")
            print(out, err)

    def test_list_invalid_type(self) -> None:
        """
        Test list command with invalid type.

        Verify that if we pass in an object type that does not exist, the list command
        will show the correct error.
        """
        with captured_output() as (out, err):
            self.command.do_list("Somerandomtype")
            print(out, err)


class TestCommandKlee(unittest.TestCase):
    """This class is used to test all klee-related commands given valid inputs."""

    def setUp(self) -> None:
        """
        Create a new instance of the command object without the wrapping object.

        Note that in these tests we use the Command object directly.
        """
        self.command = command.Command("", False, False, None)

    # ==== do_to_klee_format =====
    def test_to_klee_format_valid(self) -> None:
        """Verify that we can convert a valid file to a KLEE-compatible format."""
        with captured_output() as (out, err):
            # self.command.do_to_klee_format("examplefile.c")
            print(out, err)

    # ==== Test do_klee_to_bc =====
    def test_klee_to_bc(self) -> None:
        """See if we can convert a klee formatted file to a .bc file."""
        with captured_output() as (out, err):
            print(out, err)

    # ==== Test do_klee_replay ====
    def test_klee_replay_valid(self) -> None:
        """Verify that tests can be replayed given a valid test file generated by KLEE."""
        with captured_output() as (out, err):
            self.command.do_klee_replay("samplefile.ktest")
            print(out, err)


class TestCommand(unittest.TestCase):
    """Test each command with valid inputs."""

    @classmethod
    def setUpClass(cls):
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
        }

    def setUp(self):
        """
        Create a new instance of the Command object without the wrapping object.

        Note that in these tests we use the Command object directly.
        """
        self.command = command.Command("", False, False, None)

    def test_num_args_invalid(self):
        """Check that commands throw errors when given an incorrect number of arguments."""
        with captured_output() as (out, err):
            for valid_command in self.valid_commands:
                function_name = "do_" + valid_command
                method = getattr(self.command, function_name)
                min_num_args = self.valid_commands[valid_command][0]
                max_num_args = self.valid_commands[valid_command][1]
                if min_num_args > 0:
                    # res = method("")
                    print(method)
                    # TODO: assert that result is none
                if max_num_args != float('inf'):
                    # res = method("a " * (max_num_args + 1))
                    pass
                    # TODO: assert that the result is none
            print(out, err)

    # ==== Test do_analyze ====
    # def test_analyze_all(self):
    #     """Test the analyze command given input * (meaning we should analyze all)."""
    #     with captured_output() as (out, err):
    #         self.command.do_analyze("*")
    #         print(out, err)

    # def test_analyze_valid_name(self):
    #     """Test that we can analyze a specific object."""
    #     with captured_output() as (out, err):
    #         self.command.do_analyze("some_name")
    #         print(out, err)

    # ==== Test do_convert =====
    def test_convert_valid_type(self) -> None:
        """
        Test convert command with a file of source code.

        See if we can convert a file containing source code of a type
        we recognize to a Graph representing its control flow.
        """
        with captured_output() as (out, err):
            # self.command.do_convert("testfile.py") # TODO
            print(out, err)

    # TODO: convert recursive

    # ==== Test do_show =====
    def test_show_metric_valid(self) -> None:
        """
        Check show command with metric of a specific name.

        Verify that calling the show command with a valid metric name will
        display the metric value in the REPL.
        """
        with captured_output() as (out, err):
            self.command.data.metrics["foo"] = ["123", "123"]
            command_input = f"{command.ObjTypes.METRIC.value} foo"
            self.command.do_show(command_input)
            print(out, err)

    def test_show_graph_valid(self) -> None:
        """
        Check show command with a graph of specific name.

        Verify that we get the correct output graw if we call the show function
        for a valid graph name.
        """
        with captured_output() as (out, err):
            self.command.data.graphs["foo"] = "123"
            self.command.do_show(command.ObjTypes.GRAPH.value + " " + "foo")
            print(out, err)

    def test_show_all_types_valid(self) -> None:
        """
        Check show command with wildcard operator for type.

        Verify that we can use the wildcard operator to show all objects (objects
        of all types) for a given name.
        """
        with captured_output() as (out, err):
            self.command.data.graphs["foo"] = "123"
            self.command.data.metrics["foo"] = "123"
            self.command.do_show(command.ObjTypes.ALL.value + " foo")
            print(out, err)

    def test_show_all_names_valid(self) -> None:
        """
        Check show command with wildcard operator for name.

        Verify that we can use the wildcard operator to show all objects
        of a given type.
        """
        with captured_output() as (out, err):
            self.command.data.graphs["foo"] = "123"
            self.command.data.graphs["bar"] = "456"
            self.command.do_show(command.ObjTypes.GRAPH.value + " " + command.ObjTypes.ALL.value)
            print(out, err)

    # ==== Test do_list =====
    def test_list_graphs(self) -> None:
        """
        Check list command with graph type argument.

        Verify that calling list with graph type displays all of the graphs the
        REPL knows about.
        """
        with captured_output() as (out, err):
            self.command.do_list(command.ObjTypes.GRAPH.value)
            print(out, err)

    def test_list_metrics(self) -> None:
        """
        Check list command with metric type argument.

        Verify that calling list with metric type displays all of the metrics the
        REPL knows about.
        """
        with captured_output() as (out, err):
            self.command.do_list(command.ObjTypes.METRIC.value)
            print(out, err)

    def test_list_all(self) -> None:
        """
        Check list with wildcard.

        Verify that we can use the wildcard operator to list objects of all types through
        the list command.
        """
        with captured_output() as (out, err):
            self.command.do_list(command.ObjTypes.ALL.value)
            print(out, err)

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
            self.command.data.graphs['sample_graph'] = 'foo'
            self.command.data.graphs['sample_graph'] = 'bar'
            self.command.data.metrics['sample_graph'] = 'abc'
            self.command.do_delete(str(obj_type) + " " + str(obj_name))
            print(out, err)

    def test_delete_metric_valid(self) -> None:
        """
        Check delete metric.

        Verify that if we call the delete command with the name of a Graph that the REPL does
        not know about, we get the correct error.
        """
        with captured_output() as (out, err):
            obj_type = command.ObjTypes.METRIC
            obj_name = "sample_metric"
            self.command.data.metrics['sample_metric'] = 'foo'
            self.command.data.metrics['sample_metric'] = 'bar'
            self.command.data.graphs['sample_metric'] = 'a'
            self.command.do_delete(str(obj_type) + " " + str(obj_name))
            print(out, err)

    def test_delete_all_types_valid(self) -> None:
        """
        Check wildcard in delete.

        Verify that we can use the wildcard operator with the delete command to delete objects all
        all types matching a given name.
        """
        with captured_output() as (out, err):
            obj_type = command.ObjTypes.ALL
            obj_name = "sample_name"
            self.command.data.graphs['sample_name'] = 'foo'
            self.command.data.metrics['sample_name'] = 'foo'

            self.command.data.graphs['sample_name'] = 'a'
            self.command.data.metrics['sample_name'] = 'b'
            self.command.do_delete(str(obj_type) + " " + str(obj_name))
            print(out, err)

    def test_delete_all_names_valid(self) -> None:
        """Verify that we can use the wildcard operator to delete all objects of a given type."""
        with captured_output() as (out, err):
            # Delete * name
            obj_type = command.ObjTypes.GRAPH
            obj_name = "*"
            self.command.data.graphs['sample_name'] = 'a'
            self.command.data.graphs['sample_name'] = 'b'
            self.command.data.graphs['sample_name'] = 'c'
            self.command.data.metrics['sample_name'] = 'b'

            self.command.do_delete(str(obj_type) + " " + str(obj_name))
            print(out, err)

    # TODO: test invalid


if __name__ == '__main__':
    unittest.main()
