import balder
from ...utils.unresolved_resource import UnresolvedResource


class UnresolvedResourceParameterConfig(balder.Feature):
    """
    This is a configuration feature that provides parameters for resolving unresolved resources.
    """

    def get_parameters_for(self, resource_rule) -> list[UnresolvedResource.Parameter]:
        """
        Returns a list of parameters that should be used to resolve the given unresolved resource rule.

        :param resource_rule: the resource rule that contains the unresolved resource
        :return: a list of parameters for resolving the unresolved resource
        """
        raise NotImplementedError()
