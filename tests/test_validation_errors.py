import pytest

from dift.utils.validation import (
    ValidationError,
    dependency_help_for_uri,
    validate_config_path,
    validate_html_template,
    validate_output_options,
)


def test_rejects_output_and_output_dir_together():
    with pytest.raises(ValidationError) as exc:
        validate_output_options("report.json", "reports")

    assert "--output" in str(exc.value)
    assert "--output-dir" in str(exc.value)


def test_rejects_invalid_html_template():
    with pytest.raises(ValidationError) as exc:
        validate_html_template("unknown")

    assert "Unsupported HTML template" in str(exc.value)
    assert "dark" in str(exc.value)


def test_rejects_missing_config_file():
    with pytest.raises(ValidationError) as exc:
        validate_config_path("missing.yaml")

    assert "Config file not found" in str(exc.value)


def test_rejects_invalid_config_extension(tmp_path):
    config = tmp_path / "config.txt"
    config.write_text("invalid", encoding="utf-8")

    with pytest.raises(ValidationError) as exc:
        validate_config_path(str(config))

    assert "Unsupported config file type" in str(exc.value)


def test_dependency_help_for_bigquery():
    message = dependency_help_for_uri("bigquery://project.dataset.table")

    assert "google-cloud-bigquery" in message
    assert "db-dtypes" in message


def test_dependency_help_for_snowflake():
    message = dependency_help_for_uri(
        "snowflake://user:password@account/db/schema:orders"
    )

    assert "snowflake-sqlalchemy" in message


def test_dependency_help_for_redshift():
    message = dependency_help_for_uri(
        "redshift+redshift_connector://user:password@host:5439/db:orders"
    )

    assert "redshift-connector" in message