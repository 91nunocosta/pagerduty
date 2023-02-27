"""Test the command line interface for prototype-python-library"""
import os

from typer.testing import CliRunner

from pagerduty.cli import pagerduty

runner = CliRunner()


def test_app() -> None:
    """Test the command line interface for pagerduty"""
    result = runner.invoke(pagerduty, ["abilities", "list"])
    assert result.exit_code == 0
    assert len(result.output.strip().split(os.linesep)) > 2

    result = runner.invoke(pagerduty, ["abilities", "test", "teams"])
    assert result.exit_code == 0
    assert result.output.strip() == "yes"

    result = runner.invoke(pagerduty, ["users"])
    assert result.exit_code == 0
    assert len(result.output.strip().split(os.linesep)) >= 1

    result = runner.invoke(pagerduty, ["contacts", "PLOASXQ"])
    assert result.exit_code == 0
    assert len(result.output.strip().split(os.linesep)) >= 1
