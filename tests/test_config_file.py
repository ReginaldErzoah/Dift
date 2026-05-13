import subprocess
import sys
import yaml
def test_cli_config_file_overrides_defaults(sample_csv_files, tmp_path):
    old_csv, new_csv = sample_csv_files
    
    config_path = tmp_path / "test_config.yaml"
    
    config_data = {
        "threshold": 0.99,
        "report": "console"
    }
    config_path.write_text(yaml.dump(config_data))

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(new_csv),
            "--config",
            str(config_path),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Numeric drift" not in result.stdout