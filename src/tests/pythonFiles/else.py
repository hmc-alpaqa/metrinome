# pylint: disable-all
"""Used for testing the python converter."""


def if_func() -> None:
    """Contains an if statement."""
    var_one = False
    if var_one == 2:
        var_two = 5
    elif var_one == 77:
        var_two = 6
    elif var_one == 78:
        var_two = 7
    else:
        var_two = 1
