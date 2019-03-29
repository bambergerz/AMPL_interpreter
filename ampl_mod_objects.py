class ModFile:
    def __init__(self, name):
        self.name = name
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    def create_file(self):
        with open(self.name + ".mod", "w") as fileHandle:
            fileHandle.writelines("\n".join(self.lines))


class CrossProduct:
    def __init__(self, x, y):
        assert isinstance(x, Set)
        assert isinstance(y, Set)
        self.x = x
        self.y = y
        self.msg = self.__str__()

    def __str__(self):
        return self.x.name + " cross " + self.y.name


class Within:
    def __init__(self, cross=None):
        if isinstance(cross, CrossProduct):
            self.space = cross
        self.msg = self.__str__()

    def __str__(self):
        return " within (" + str(self.space) + ")"


class Set:
    def __init__(self, name, set_initializer=None):
        assert isinstance(name, str)
        if set_initializer is None:
            set_initializer = ""
        self.name = name
        self.addressed_in_dat = False
        self.set_initializer = set_initializer
        self.msg = self.__str__()

    def __str__(self):
        return "set " + self.name + str(self.set_initializer) + ";"


class Constraint:
    def __init__(self, x, y):
        assert isinstance(x, Argument)
        assert isinstance(y, Argument)
        self.x = x
        self.y = y
        self.msg = ""

    def __str__(self):
        return self.msg


class Argument:
    def __init__(self):
        self.msg = ""


class SetArgument(Argument):
    def __init__(self, set_name=None):
        self.set_name = set_name
        super(SetArgument, self).__init__()

    def __str__(self):
        return "{" + self.set_name + "}"


class IntegerArgument(Argument):
    def __init__(self, x):
        """

        :param x: an int which represents an integer
        """

        super(IntegerArgument, self).__init__()
        self.integer = x

    def __str__(self):
        return str(self.integer)


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


class Param:
    def __init__(self, name, set=None, constraint=None):
        self.name = name
        self.set = set
        self.constraint = constraint

    def __str__(self):
        if isinstance(self.set, Set):
            return "param " + self.name + " in " + self.set.name
        if isinstance(self.constraint, Constraint):
            return "param " + self.name + " " + str(self.constraint) + ";"


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
    file.add_line(str(verticies))
    file.add_line(str(edges))
    file.add_line(str(source))
    file.add_line(str(sink))
    file.add_line(str(capacity))
    file.create_file()
    print(verticies)
    print(edges)
    print(source)
    print(sink)
    print(capacity)
