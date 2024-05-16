import click.testing

from dradon import console


def test_main_succeeds():
    runner = click.testing.CliRunner()
    result = runner.invoke(console.main, ["examples/little_test.png"])
    assert result.exit_code == 0
