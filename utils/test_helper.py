import factory
from .strategies import TestStrategy


class TestHelper:
    @classmethod
    def get_data(cls, type: factory.Factory) -> dict:
        """ convert a model factory to dict """
        return factory.build(dict, FACTORY_CLASS=type)

    @staticmethod
    def compare_dict_data(received: dict, expected: list):
        """
        Compares the values of two dictionaries for matching keys.

        Args:
            received (dict): The actual dictionary received.
            expected (dict): The expected dictionary to compare against.

        Returns:
            tuple: A boolean indicating success, and a message detailing mismatched values if any.
        """
        results = []
        for value in expected:
            if value in received.keys():
                results.append(True)
            else:
                results.append(False)
        return all(results)


class TestStrategyRunner:
    """
    A class responsible for executing a given test strategy.

    This class defines a method `execute`, which takes a `TestStrategy` object as an argument, 
    invokes its `act()` method to perform the strategy's action, and then calls its `assert_()` 
    method to validate the expected behavior.

    Attributes:
    None

    Methods:
    execute(strategy: TestStrategy) -> None:
        Executes the action and validation steps of the provided strategy.
    """
    @classmethod
    def execute(cls, strategy: TestStrategy):
        """
        Executes the action and assertion of a given test strategy.

        This method performs the following steps:
        1. Calls the `act()` method of the provided strategy to perform its action.
        2. Calls the `assert_()` method of the provided strategy to validate the result.

        Args:
        strategy (TestStrategy): A strategy object that implements the `act()` and `assert_()` methods.

        Returns:
        None
        """
        # act
        strategy.act()

        # assert
        strategy.assert_()
