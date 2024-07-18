import traceback

from jpype import JClass
from pyadams.core.classes import JavaObject
from typing import Union, List


class MessageCollection(JavaObject):

    def __init__(self, jobject=None):
        """
        Initializes the message collection.

        :param jobject: the object to wrap, creates a new instance if None
        """
        if jobject is None:
            jobject = JClass("adams.core.MessageCollection")()
        super().__init__(jobject)

    def clear(self):
        """
        Removes all message.
        """
        self.jobject.clear()

    def add(self, msg: Union[str, List[str]]):
        """
        Adds the message(s) to its internal list.

        :param msg: the message(s) to add
        :type msg: str or list
        """
        if isinstance(msg, str):
            self.jobject.add(msg)
        else:
            for s in msg:
                self.jobject.add(s)

    def add_exc(self, msg: str):
        """
        Adds the message to its internal list alongside the exception.

        :param msg: the message to add with the current exception
        :type msg: str
        """
        self.add(msg + "\n" + traceback.format_exc())

    def __len__(self):
        """
        Returns the number of stored messages.

        :return: the number of message
        :rtype: int
        """
        return self.jobject.size()
