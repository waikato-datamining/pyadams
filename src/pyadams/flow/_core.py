import json

import jpype
from jpype import JClass
from typing import Optional, Dict, List
from pyadams.core.classes import JavaObject


class Actor(JavaObject):

    def __init__(self, jobject=None, classname: str = None):
        """
        Initializes the actor.

        :param jobject: the Java object to use, None if classname provided
        :param classname: the classname to use for instantiation, ignored if jobject provided
        :type classname: str
        """
        if (jobject is None) and (classname is not None):
            jobject = JClass(classname)()
        if jobject is None:
            raise Exception("Either jobject or classname must be provided!")
        self.enforce_type(jobject, "adams.flow.core.Actor")
        super().__init__(jobject)

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

    @property
    def root(self) -> Optional['Actor']:
        """
        Returns the root actor.

        :return: the actor, None if not available
        :rtype: Actor
        """
        r = self.jobject.getRoot()
        if r is None:
            return None
        else:
            return Actor(r)

    @property
    def is_finished(self) -> bool:
        """
        Returns whether the actor has finished.

        :return: True if finished
        :rtype: bool
        """
        return self.jobject.isFinished()

    @property
    def is_executed(self) -> bool:
        """
        Returns whether the actor has been executed.

        :return: True if executed
        :rtype: bool
        """
        return self.jobject.isExecuted()

    @property
    def is_stopped(self) -> bool:
        """
        Returns whether the actor has been stopped.

        :return: True if stopped
        :rtype: bool
        """
        return self.jobject.isStopped()

    @property
    def is_headless(self) -> bool:
        """
        Returns whether the actor is used in headless mode.

        :return: True if headless mode
        :rtype: bool
        """
        return self.jobject.isHeadless()

    @property
    def parent(self) -> Optional['Actor']:
        """
        Returns whether the parent actor if available.

        :return: the parent, None if not available
        :rtype: Actor
        """
        return self.jobject.getParent()

    def stop_execution(self, msg: str = None):
        """
        Stops the execution.

        :param msg: the optional message
        :type msg: str
        """
        if msg is None:
            self.jobject.stopExecution()
        else:
            self.jobject.stopExecution(msg)

    def apply_dict(self, d: Dict):
        """
        Configures itself using the dictionary of options (in JSON format).

        :param d: the dictionary of options to use
        :type d: dict
        """
        self.apply_json(json.dumps(d))

    def to_dict(self) -> Dict:
        # TODO
        pass

    @classmethod
    def from_dict(cls, classname: str, d: Dict) -> 'Actor':
        """
        Instantiating an actor from a dictionary (in JSON format).

        :param classname: the classname of the actor
        :type classname: str
        :param d: the dictionary of options to use
        :type d: dict
        :return: the actor instance
        :rtype: Actor
        """
        result = Actor(classname=classname)
        result.apply_dict(d)
        return result

    def apply_json(self, j: str):
        """
        Configures itself from a JSON string.

        :param j: the JSON string of options to use
        :type j: str
        """
        from net.minidev.json.parser import JSONParser
        parser = JSONParser(JSONParser.MODE_JSON_SIMPLE)
        jsonobj = parser.parse(j)
        consumer = JClass("adams.core.option.JsonConsumer")()
        consumer.consume(self.jobject, jsonobj)

    def to_json(self) -> str:
        # TODO
        pass

    @classmethod
    def from_json(cls, classname: str, j: str) -> 'Actor':
        """
        Instantiating an actor from a JSON string.

        :param classname: the classname of the actor
        :type classname: str
        :param j: the JSON string of options to use
        :type j: str
        :return: the actor instance
        :rtype: Actor
        """
        result = Actor(classname=classname)
        result.apply_json(j)
        return result

    def apply_args(self, args: List[str]):
        """
        Configures itself from a list of command-line args.

        :param args: the list of command-line options
        :type args: list
        """
        consumer = JClass("adams.core.option.ArrayConsumer")()
        consumer.consume(self.jobject, jpype.JString[:](args))

    def to_args(self) -> List[str]:
        # TODO
        pass

    @classmethod
    def from_args(cls, classname: str, args: List[str]) -> 'Actor':
        """
        Instantiating an actor from a list of command-line args.

        :param classname: the classname of the actor
        :type classname: str
        :param args: the list of command-line options
        :type args: list
        :return: the actor instance
        :rtype: Actor
        """
        result = Actor(classname=classname)
        result.apply_args(args)
        return result
