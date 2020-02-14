"""Custom Runner to track statistics. """

from backpack import extend
from deepobs.pytorch.testproblems.testproblem import TestProblem
from deepobs.pytorch.testproblems import (
    mnist_logreg,
    cifar10_3c3d,
    cifar100_allcnnc,
    fmnist_2c2d,
)

SUPPORTED = (
    mnist_logreg,
    fmnist_2c2d,
    cifar10_3c3d,
    cifar100_allcnnc,
)


def integrate_backpack(testproblem):
    """Add BackPACK functionality to a DeepOBS test problem.

    Parameters:
    -----------
    testproblem : TestProblem instance from deepobs.pytorch

    Returns:
    --------
    Extended testproblem.
    """
    _check_can_be_integrated(testproblem)

    def extend_loss_func(testproblem):
        testproblem._old_loss = testproblem.loss_function

        def new_lossfunc(reduction="mean"):
            return extend(testproblem._old_loss(reduction=reduction))

        testproblem.loss_function = new_lossfunc

    extend(testproblem.net)
    extend_loss_func(testproblem)

    return testproblem


def _check_can_be_integrated(testproblem):
    """Check if the DeepOBS problem can be extended with BackPACK."""

    def check_is_deepobs_problem(testproblem):
        testproblem_class = testproblem.__class__
        if not issubclass(testproblem_class, (TestProblem,)):
            raise ValueError("Expect TestProblem, got {}".format(testproblem_class))

    def check_supported_by_backpack(testproblem):
        if not isinstance(testproblem, SUPPORTED):
            raise ValueError(
                "{} currently not supported. Working problems: {}".format(
                    testproblem_class, SUPPORTED
                )
            )

    check_is_deepobs_problem(testproblem)
    check_supported_by_backpack(testproblem)
