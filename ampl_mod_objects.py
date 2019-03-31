######################
### Infrastructure ###
######################


class ModFile:
    def __init__(self, name):
        """

        :param name: The name of this mod file we are making
        """
        self.name = name
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    def create_file(self):
        with open(self.name + ".mod", "w") as fileHandle:
            fileHandle.writelines("\n".join(self.lines))


class CrossProduct:
    def __init__(self, x, y):
        """

        :param x: a set object
        :param y: a set object
        """
        assert isinstance(x, Set)
        assert isinstance(y, Set)
        self.x = x
        self.y = y
        self.msg = self.__str__()

    def __str__(self):
        return self.x.name + " cross " + self.y.name


class Within:
    def __init__(self, cross=None):
        """

        :param cross: A cross product object or None
        """
        if isinstance(cross, CrossProduct):
            self.space = cross
        self.msg = self.__str__()

    def __str__(self):
        return " within (" + str(self.space) + ")"


class Tuple:
    def __init__(self, tup):
        """

        :param tup: A tuple of VariableArgument objects
        """
        assert isinstance(tup, tuple)
        for arg in tup:
            assert isinstance(arg, VariableArgument)
        self.tuple = tup
        self.msg = ""

    def __str__(self):
        result = "("
        for arg in self.tuple:
            result += str(arg.var)
            result += ","
        result = result[:-1]
        result += ")"
        return result


##################
### Constructs ###
##################

class Set:
    """
    An object used to define set instantiation in a .mod file
    For example:
        set VERTICIES;
        OR
        set EDGES within {<setA> cross <setB>};
    """
    def __init__(self, name, set_initializer=None):
        """

        :param name: the name of the set we are defining. A string
        :param set_initializer: If we need to specify more information about the
        set (e.g., that it is represented within a space of set x cross set y), then
        this argument contains an appropriate set initializer.
        """
        assert isinstance(name, str)
        if set_initializer is None:
            set_initializer = ""
        self.name = name
        self.addressed_in_dat = False
        self.set_initializer = set_initializer
        self.msg = self.__str__()

    def __str__(self):
        return "set " + self.name + str(self.set_initializer) + ";"


class Param:
    """
    An object used to define parameter initialization.

    In practice, parameters are variables (NOT decision variables) which
    are used to define the either the objective function, constraints,
    or both.

    For example:
        param SOURCE in VERTICIES
    """
    def __init__(self, name, set=None, constraint=None):
        """

        :param name: the name of this parameter. A string
        :param set: the name of the set in which the parameter can be found.
        :param constraint: A set constraint.
        """
        self.name = name
        self.set = set
        self.constraint = constraint

    def __str__(self):
        if isinstance(self.set, Set):
            return "param " + self.name + " in " + self.set.name
        if isinstance(self.constraint, Constraint):
            return "param " + self.name + " " + str(self.constraint) + ";"


class Variable:
    """
    An object used to define variable initialization.

    In practice, variables serve as decision variables in our problem.
    I.e., these are the independent variables of our optimization experiment.
    We try to maximize or minimize our objective by changing these values.

    For example:
        var FLOW {(i, j) in EDGES} >= 0, <= capacity[i,j]
    """
    def __init__(self, name, constraints):
        self.name = name
        self.constraints = constraints

    def __str__(self):
        result = "var " + self.name + " "

    # TODO: explore how variable constraints operate


#################
### Arguments ###
#################

class Argument:
    def __init__(self):
        self.msg = ""


class SetArgument(Argument):
    def __init__(self, set=None, tup=None):
        super(SetArgument, self).__init__()
        if isinstance(set, Set):
            self.set_name = set.name
        elif isinstance(set, str):
            self.set_name = set
        self.tuple = tup
        self.msg += self.__str__()

    def __str__(self):
        result = "{"
        if isinstance(self.tuple, Tuple):
            result += str(self.tuple) +\
                      " in " +\
                      self.set_name
        else:
            result += self.set_name
        result += "}"
        return result


class IntegerArgument(Argument):
    def __init__(self, x):
        super(IntegerArgument, self).__init__()
        self.integer = x
        self.msg += self.__str__()

    def __str__(self):
        return str(self.integer)


class VariableArgument(Argument):
    def __init__(self, var):
        super(VariableArgument, self).__init__()
        self.var = var
        self.msg += self.__str__()

    def __str__(self):
        return str(self.var)


###################
### Constraints ###
###################


class Constraint:
    def __init__(self, x, y):
        assert isinstance(x, Argument)
        assert isinstance(y, Argument)
        self.x = x
        self.y = y
        self.msg = ""

    def __str__(self):
        return self.msg


class GreaterThan(Constraint):
    def __init__(self, x, y):
        super(GreaterThan, self).__init__(x, y)
        self.msg += self.__str__()

    def __str__(self):
        return str(self.x) + " > " + str(self.y)


class GreaterThanEq(Constraint):
    def __init__(self, x, y):
        super(GreaterThanEq, self).__init__(x, y)
        self.msg += self.__str__()

    def __str__(self):
        return str(self.x) + " >= " + str(self.y)


class LessThan(Constraint):
    def __init__(self, x, y):
        super(LessThan, self).__init__(x, y)
        self.msg += self.__str__()
    
    def __str__(self):
        return str(self.x) + " < " + str(self.y)


class LessThanEq(Constraint):
    def __init__(self, x, y):
        super(LessThanEq, self).__init__(x, y)
        self.msg += self.__str__()

    def __str__(self):
        return str(self.x) + " <= " + str(self.y)


class Eq(Constraint):
    def __init__(self, x, y):
        super(Eq, self).__init__(x, y)
        self.msg += self.__str__()

    def __str__(self):
        return str(self.x) + " = " + str(self.y)


if __name__ == "__main__":

    file = ModFile("Rec2")
    verticies = Set("VERTICIES")
    edges = Set(
        name="EDGES",
        set_initializer=Within(
            cross=CrossProduct(
                x=verticies,
                y=verticies
            )
        )
    )
    source = Param(
        name="SOURCE",
        set=verticies)
    sink = Param(
        name="SINK",
        set=verticies)
    capacity = Param(
        name="capacity",
        constraint=GreaterThanEq(
            x=SetArgument(edges.name),
            y=IntegerArgument(0)
        )
    )
    tup_i_j = Tuple(
        tup=(
            VariableArgument("i"),
            VariableArgument("j")
        )
    )

    file.add_line(str(verticies))
    file.add_line(str(edges))
    file.add_line(str(source))
    file.add_line(str(sink))
    file.add_line(str(capacity))
    file.add_line(str(tup_i_j))
    file.create_file()
    print(verticies)
    print(edges)
    print(source)
    print(sink)
    print(capacity)
    print(tup_i_j)
