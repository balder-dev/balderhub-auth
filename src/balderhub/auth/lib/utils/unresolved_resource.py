from __future__ import annotations

from abc import ABC, abstractmethod

from .base_resource import BaseResource
from .resource import Resource


class UnresolvedResource(BaseResource, ABC):
    """
    This is the base class for all unresolved resource types.
    """

    class Parameter:
        """
        Base class for parameters that are used to resolve an unresolved resource.
        """

    def __init__(self, **kwargs):
        """
        :param kwargs: additional keyword arguments
        """
        super().__init__(**kwargs)

    @abstractmethod
    def get_resolved_resource(self, param: Parameter) -> Resource:
        """
        Resolves the resource with the given parameter.

        :param param: the parameter for the unresolved resource
        :return: the resolved resource
        """
