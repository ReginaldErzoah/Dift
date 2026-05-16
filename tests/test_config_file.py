import json

import yaml
from typer.testing import CliRunner

from dift.cli import compare_app

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

runner = CliRunner()


def test_cli_filepath_override_config(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_data = {"old_dataset": "examples/old.csv", "new_dataset": "examples/new.csv"}
    config_file.write_text(yaml.dump(config_data))

    result = runner.invoke(compare_app, [
        "examples/old.csv", 
        "examples/old.csv", 
        "--key", "customer_id",
        "--config", str(config_file),
        "--report", "json"
    ])
    assert '"row_delta": 0' in result.stdout

    
def test_cli_threshold_priority(tmp_path):
    config_file = tmp_path / "priority_config.yaml"
    config_data = {
        "old_dataset": "examples/old.csv",
        "new_dataset": "examples/old.csv",
        "threshold": 0.2,
    }
    config_file.write_text(yaml.dump(config_data))

    result = runner.invoke(compare_app, [
        "--config", str(config_file),
        "--threshold", "0.5",
        "--report", "json"
    ])

    assert result.exit_code == 0
    # if the cli input correctly overrides the config file, then we expect a drift_threshhold of 0.5 in the output
    assert '"drift_threshold": 0.5' in result.stdout
    assert '"drift_threshold": 0.2' not in result.stdout


def test_yaml_config(tmp_path):
    config_file = tmp_path / "test_config.yaml"
    content = {"old_dataset": "examples/old.csv", "new_dataset": "examples/new.csv"}
    config_file.write_text(yaml.dump(content))

    result = runner.invoke(compare_app, ["--config", str(config_file)])
    assert result.exit_code == 0
    assert "Dift Dataset Comparison" in result.stdout


def test_toml_config(tmp_path):
    config_file = tmp_path / "test_config.toml"
    content = 'old_dataset = "examples/old.csv"\nnew_dataset = "examples/new.csv"'
    config_file.write_text(content)

    result = runner.invoke(compare_app, ["--config", str(config_file)])
    assert result.exit_code == 0
    assert "Dift Dataset Comparison" in result.stdout


def test_json_config(tmp_path):
    config_file = tmp_path / "test_config.json"
    content = {"old_dataset": "examples/old.csv", "new_dataset": "examples/new.csv"}
    config_file.write_text(json.dumps(content))

    result = runner.invoke(compare_app, ["--config", str(config_file)])
    assert result.exit_code == 0
    assert "Dift Dataset Comparison" in result.stdout
