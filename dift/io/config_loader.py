import json
import pathlib
import sys
from typing import Any, cast

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None


def load_config(file_path: str) -> dict[str, Any]:
    path = pathlib.Path(file_path)
    if not path.exists():
        print(
            f"Warning: Configuration file '{file_path}' not found. Using defaults.",
            file=sys.stderr,
        )
        return {}

    suffix = path.suffix.lower()

    try:
        if suffix == ".json":
            with open(path) as f:
                return cast(dict[str, Any], json.load(f))
        elif suffix == ".toml":
            if tomllib:
                with open(path, "rb") as f:
                    return cast(dict[str, Any], tomllib.load(f))
            else:
                print("Error: Install 'tomli' to use TOML configs.", file=sys.stderr)
                return {}

        elif suffix in [".yaml", ".yml"]:
            try:
                import yaml

                with open(path) as f:
                    return cast(dict[str, Any], yaml.safe_load(f))
            except ImportError:
                print("Error: Install 'PyYAML' to use YAML configs.", file=sys.stderr)
                return {}
    except Exception as e:
        print(f"Failed to parse {suffix} config: {e}", file=sys.stderr)
        return {}

    return {}
