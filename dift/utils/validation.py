from __future__ import annotations

from pathlib import Path

SUPPORTED_LOCAL_EXTENSIONS = {
    ".csv",
    ".parquet",
    ".xlsx",
    ".xls",
    ".json",
}

SUPPORTED_REPORT_FORMATS = {
    "console",
    "json",
    "csv",
    "excel",
    "html",
}

SUPPORTED_HTML_TEMPLATES = {
    "default",
    "clean",
    "compact",
    "enterprise",
    "dark",
}


class ValidationError(ValueError):
    """Raised when user input validation fails."""


def validate_output_options(output: str | None, output_dir: str | None) -> None:
    if output and output_dir:
        raise ValidationError(
            "Use either --output or --output-dir, not both.\n"
            "Example:\n"
            "  dift old.csv new.csv --report json --output report.json\n"
            "  dift old.csv new.csv --report json --output-dir reports/"
        )


def validate_local_dataset_path(path: str) -> None:
    dataset_path = Path(path)

    if not dataset_path.exists():
        raise ValidationError(
            f"Dataset not found: {path}\n"
            "Check that the file path is correct.\n"
            "Example:\n"
            "  dift examples/old.csv examples/new.csv"
        )

    suffix = dataset_path.suffix.lower()

    if suffix not in SUPPORTED_LOCAL_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_LOCAL_EXTENSIONS))
        raise ValidationError(
            f"Unsupported dataset type '{suffix}'.\n"
            f"Supported local file types: {supported}\n"
            "For databases, use a supported connector URI such as:\n"
            "  sqlite:///examples/old.db:customers"
        )


def validate_html_template(template: str) -> None:
    if template not in SUPPORTED_HTML_TEMPLATES:
        supported = ", ".join(sorted(SUPPORTED_HTML_TEMPLATES))
        raise ValidationError(
            f"Unsupported HTML template '{template}'.\n"
            f"Supported templates: {supported}\n"
            "Example:\n"
            "  dift old.csv new.csv --report html --template dark"
        )


def validate_config_path(config: str | None) -> None:
    if config is None:
        return

    config_path = Path(config)

    if not config_path.exists():
        raise ValidationError(
            f"Config file not found: {config}\n"
            "Provide a valid config file path.\n"
            "Example:\n"
            "  dift --config config.yaml"
        )

    if config_path.suffix.lower() not in {".json", ".yaml", ".yml", ".toml"}:
        raise ValidationError(
            f"Unsupported config file type '{config_path.suffix}'.\n"
            "Supported config types: .json, .yaml, .yml, .toml"
        )


def dependency_help_for_uri(uri: str) -> str:
    if uri.startswith("duckdb://"):
        return "DuckDB support requires: pip install duckdb"

    if uri.startswith("bigquery://"):
        return (
            "BigQuery support requires: "
            "pip install google-cloud-bigquery db-dtypes"
        )

    if uri.startswith(("sqlite:///",)):
        return "SQLite support requires SQLAlchemy: pip install sqlalchemy"

    if uri.startswith(("postgres://", "postgresql://", "postgresql+psycopg2://")):
        return "PostgreSQL support requires: pip install sqlalchemy psycopg2-binary"

    if uri.startswith("postgresql+psycopg://"):
        return "PostgreSQL support requires: pip install sqlalchemy psycopg"

    if uri.startswith(("mysql://", "mysql+pymysql://")):
        return "MySQL support requires: pip install sqlalchemy pymysql"

    if uri.startswith(("redshift+psycopg2://", "redshift+redshift_connector://")):
        return (
            "Redshift support requires: "
            "pip install sqlalchemy-redshift redshift-connector"
        )

    if uri.startswith(("snowflake://", "snowflake+snowflake://")):
        return "Snowflake support requires: pip install snowflake-sqlalchemy"

    return "Install the required connector dependency and try again."