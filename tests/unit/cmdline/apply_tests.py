from datetime import datetime
from unittest import TestCase

from mock import MagicMock

from blockwart.cmdline.apply import bw_apply, format_node_result
from blockwart.node import ApplyResult


class FakeNode(object):
    name = "nodename"

    def apply(self, interactive=False):
        assert interactive
        result = ApplyResult(self, (), ())
        result.start = datetime(2013, 8, 10, 0, 0)
        result.end = datetime(2013, 8, 10, 0, 1)
        return result


class ApplyTest(TestCase):
    """
    Tests blockwart.cmdline.apply.bw_apply.
    """
    def test_interactive(self):
        node1 = FakeNode()
        repo = MagicMock()
        repo.get_node.return_value = node1
        args = MagicMock()
        args.interactive = True
        args.target = "node1"
        output = list(bw_apply(repo, args))
        self.assertTrue(output[0].startswith("\nnodename: run started at "))
        self.assertTrue(output[1].startswith("\n  nodename: run completed after "))
        self.assertEqual(
            output[2],
            "  0 correct, 0 fixed, 0 aborted, 0 unfixable, 0 failed\n",
        )
        self.assertEqual(len(output), 3)


class FormatNodeResultTest(TestCase):
    """
    Tests blockwart.cmdline.apply.format_node_result.
    """
    def test_values(self):
        result = MagicMock()
        result.correct = 0
        result.fixed = 1
        result.aborted = 2
        result.unfixable = 3
        result.failed = 4
        self.assertEqual(
            format_node_result(result),
            "0 correct, 1 fixed, 2 aborted, 3 unfixable, 4 failed",
        )

    def test_zero(self):
        result = MagicMock()
        result.correct = 0
        result.fixed = 0
        result.aborted = 0
        result.unfixable = 0
        result.failed = 0
        self.assertEqual(
            format_node_result(result),
            "0 correct, 0 fixed, 0 aborted, 0 unfixable, 0 failed",
        )
