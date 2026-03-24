import balder

from balderhub.auth.lib.utils import Operation


class OperationHandlingFeature(balder.Feature):
    """
    This is the base feature class for handling operations.
    """

    def prepare_operation(self, operation: Operation) -> None:
        """
        Prepares the given operation.

        :param operation: the operation to prepare
        """

    def enter_operation(self, operation: Operation) -> bool:
        """
        Enters the given operation.

        :param operation: the operation to enter
        :return: True if the operation was entered successfully, False otherwise
        """
        raise NotImplementedError

    def leave_operation(self, operation: Operation) -> bool:
        """
        Leaves the given operation.

        :param operation: the operation to leave
        :return: True if the operation was left successfully, False otherwise
        """
        raise NotImplementedError

    def cleanup_operation(self, operation: Operation) -> None:
        """
        Cleans up the given operation.

        :param operation: the operation to clean up
        """
