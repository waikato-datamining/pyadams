from jpype import JClass
from pyadams.flow.core import Actor

_ActorUtils = None


def _get_actor_utils():
    """
    Returns the ActorUtils instance.

    :return: the JPype object of adams.flow.core.ActorUtils
    """
    global _ActorUtils
    if _ActorUtils is None:
        _ActorUtils = JClass("adams.flow.core.ActorUtils")
    return _ActorUtils


def is_standalone(actor: Actor) -> bool:
    """
    Tests whether the actor is a standalone.

    :param actor: the actor to check
    :type actor: Actor
    :return: whether the actor is a standalone
    :rtype: bool
    """
    return _get_actor_utils().isStandalone(actor.jobject)


def is_source(actor: Actor) -> bool:
    """
    Tests whether the actor is a source.

    :param actor: the actor to check
    :type actor: Actor
    :return: whether the actor is a source
    :rtype: bool
    """
    return _get_actor_utils().isSource(actor.jobject)


def is_transformer(actor: Actor) -> bool:
    """
    Tests whether the actor is a transformer.

    :param actor: the actor to check
    :type actor: Actor
    :return: whether the actor is a transformer
    :rtype: bool
    """
    return _get_actor_utils().isTransformer(actor.jobject)


def is_sink(actor: Actor) -> bool:
    """
    Tests whether the actor is a sink.

    :param actor: the actor to check
    :type actor: Actor
    :return: whether the actor is a sink
    :rtype: bool
    """
    return _get_actor_utils().isSink(actor.jobject)


def read(flow_file: str) -> Actor:
    """
    Reads the flow from disk and returns the actor.

    :param flow_file: the flow file to read
    :type flow_file: str
    :return: the Actor or None if failed to load
    :rtype: str
    """
    return Actor(_get_actor_utils().read(flow_file))


def write(flow_file: str, actor: Actor) -> bool:
    """
    Writes the actor to disk.

    :param flow_file: the flow file to write to
    :type flow_file: str
    :param actor: the Actor to write
    :type actor: Actor
    :return: whether writing was successful
    :rtype: bool
    """
    return _get_actor_utils().write(flow_file, actor.jobject)
