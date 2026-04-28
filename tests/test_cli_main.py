import pytest

from cli.__main__ import main as cli_main


def test_cli_multiplexer_requires_query_text():
    with pytest.raises(SystemExit) as ei:
        cli_main(["query"])
    assert ei.value.code == 2


def test_cli_help_exits_zero():
    with pytest.raises(SystemExit) as ei:
        cli_main([])
    assert ei.value.code == 0
