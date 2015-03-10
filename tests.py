class A:
    def __init__(self):
        self.x = 1

    @classmethod
    def println(cls):
        """Return.
        :return: return
        """
        print(cls.x)

    def println2(self):
        print(self.x)


a = A()
a.println2()
