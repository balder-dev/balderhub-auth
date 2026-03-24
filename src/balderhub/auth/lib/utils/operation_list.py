from __future__ import annotations

import copy
from typing import Iterable

from balderhub.auth.lib.utils.operation import Operation, OperationT


class OperationList:
    """
    This class represents a list of operations.
    """

    # todo make sure that these checks are done everywhere!

    def __init__(self, iterable: Iterable[OperationT] = None):
        """
        :param iterable: an optional iterable of operations to initialize the list with
        """

        self._operations = []

        if iterable is not None:
            for operation in iterable:
                self.append(operation)

    def __iter__(self) -> Iterable[OperationT]:
        return self._operations.__iter__()

    def __len__(self):
        return self._operations.__len__()

    def append(self, operation: OperationT):
        """
        Appends an operation to the list.

        :param operation: the operation to append
        """
        if not isinstance(operation, Operation):
            raise TypeError(f'Operation must be an instance of `{Operation.__name__}`')
        if operation in self._operations:
            raise ValueError(f'object `{operation}` can not be added multiple times')
        self._operations.append(operation)

    def extend(self, other: OperationList):
        """
        Extends the list with the operations from another `OperationList`.

        :param other: the other `OperationList` to extend this list with
        """
        if not isinstance(other, OperationList):
            raise TypeError(f'object must be an instance of `{OperationList.__name__}`')
        for cur_obj in other:
            if cur_obj not in self._operations:
                self._operations.append(cur_obj)

    def __sub__(self, other: OperationList) -> OperationList:
        """
        Subtracts the operations of another `OperationList` from this list.

        :param other: the other `OperationList` to subtract from this list
        :return: a new `OperationList` containing the result of the subtraction
        """
        if not isinstance(other, OperationList):
            raise TypeError(f'object must be an instance of `{OperationList.__name__}`')

        result = copy.copy(self._operations)
        # check that all elements of other are contained in the current one
        for cur_other in other:
            if cur_other not in self:
                raise ValueError(f'element `{cur_other}` from the list being subtracted is not present in the current '
                                 f'list')
            result.remove(cur_other)
        return self.__class__(result)
