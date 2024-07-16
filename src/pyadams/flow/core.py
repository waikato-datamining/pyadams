from pyadams.core.classes import JavaObject


class Actor(JavaObject):

    def set_up(self) -> str:
        """
        Calls the setUp() method.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        return self.jobject.setUp()

    def execute(self) -> str:
        """
        Calls the execute() method.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        return self.jobject.execute()

    def wrap_up(self):
        """
        Calls the wrapUp() method.
        """
        self.jobject.wrapUp()

    def clean_up(self):
        """
        Calls the wrapUp() method.
        """
        self.jobject.cleanUp()

    def to_commandline(self) -> str:
        """
        Calls the toCommandLine() method.

        :return: the command-line
        :rtype: str
        """
        return self.jobject.toCommandLine()
