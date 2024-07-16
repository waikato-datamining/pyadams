import inspect

from jpype import JClass, JException, JObject


def get_classname(obj):
    """
    Returns the classname of the JPype object, Python class or object.

    :param obj: the java object or Python class/object to get the classname for
    :type obj: object
    :return: the classname
    :rtype: str
    """
    if isinstance(obj, JObject):
        return obj.getClass().getName()
    elif inspect.isclass(obj):
        return obj.__module__ + "." + obj.__name__
    else:
        return get_classname(obj.__class__)


def is_instance_of(obj, class_or_intf_name):
    """
    Checks whether the Java object implements the specified interface or is a subclass of the superclass.

    :param obj: the Java object to check
    :type obj: JPype object
    :param class_or_intf_name: the superclass or interface to check, dot notation
    :type class_or_intf_name: str
    :return: true if either implements interface or subclass of superclass
    :rtype: bool
    """
    classname = get_classname(obj)
    # array? retrieve component type and check that
    if is_array(obj):
        classname = obj.getClass().getComponentType()
    ClassLocator = JClass("nz.ac.waikato.cms.locator.ClassLocator")
    result = ClassLocator.matches(class_or_intf_name, classname)
    if result:
        return True
    return ClassLocator.hasInterface(class_or_intf_name, classname)


def is_array(obj):
    """
    Checks whether the Java object is an array.

    :param obj: the Java object to check
    :type obj: JPype object
    :return: whether the object is an array
    :rtype: bool
    """
    return obj.getClass().isArray()


class JavaObject:
    """
    Basic Java object.
    """

    def __init__(self, jobject):
        """
        Initializes the wrapper with the specified Java object.

        :param jobject: the Java object to wrap
        :type jobject: JPype object
        """
        if jobject is None:
            raise Exception("No Java object supplied!")
        self.jobject = jobject
        self._property_path = None

    def __str__(self):
        """
        Just calls the toString() method.

        :rtype: str
        """
        return str(self.jobject)

    def __repr__(self):
        """
        Just calls the toString() method.

        :rtype: str
        """
        return str(self.jobject)

    def __unicode__(self):
        """
        Just calls the toString() method.

        :rtype: str
        """
        return str(self.jobject)

    @property
    def classname(self):
        """
        Returns the Java classname in dot-notation.

        :return: the Java classname
        :rtype: str
        """
        return self.jobject.getClass().getName()

    @property
    def jclass(self):
        """
        Returns the Java class object of the underlying Java object.

        :return: the Java class
        :rtype: JClass
        """
        return self.jobject.getClass()

    @property
    def is_serializable(self):
        """
        Returns true if the object is serialiable.

        :return: true if serializable
        :rtype: bool
        """
        return JavaObject.check_type(self.jobject, "java.io.Serializable")

    @classmethod
    def check_type(cls, jobject, intf_or_class):
        """
        Returns whether the object implements the specified interface or is a subclass.

        :param jobject: the Java object to check
        :type jobject: JPype object
        :param intf_or_class: the classname in Java notation (eg "weka.core.DenseInstance;")
        :type intf_or_class: str
        :return: whether object implements interface or is subclass
        :rtype: bool
        """
        return is_instance_of(jobject, intf_or_class)

    @classmethod
    def enforce_type(cls, jobject, intf_or_class):
        """
        Raises an exception if the object does not implement the specified interface or is not a subclass.

        :param jobject: the Java object to check
        :type jobject: JPype object
        :param intf_or_class: the classname in Java notation (eg "weka.core.DenseInstance")
        :type intf_or_class: str
        """
        if not cls.check_type(jobject, intf_or_class):
            raise TypeError("Object does not implement or subclass " + intf_or_class + ": " + get_classname(jobject))

    @classmethod
    def new_instance(cls, classname, options=None):
        """
        Creates a new object from the given classname using the default constructor, None in case of error.

        :param classname: the classname in Java notation (eg "weka.core.DenseInstance")
        :type classname: str
        :param options: the list of options to use, ignored if None
        :type options: list
        :return: the Java object
        :rtype: JPype object
        """
        try:
            if options is None:
                options = []
            return JClass("adams.core.option.OptionUtils").forName(JClass("java.lang.Object"), classname, options)
        except JException as e:
            print("Failed to instantiate " + classname + ": " + str(e))
            return None
