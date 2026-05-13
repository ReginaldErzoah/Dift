import json
import pathlib


try:
    import tomllib  
except ImportError:
    try:
        import tomli as tomllib  
    except ImportError:
        tomllib = None

def load_config(file_path: str) -> dict:
    path = pathlib.Path(file_path)
    if not path.exists():
        return {}

    suffix = path.suffix.lower()

    try:
        if suffix == ".json":
            with open(path, "r") as f:
                return json.load(f)
        
        elif suffix == ".toml":
            if tomllib:
                with open(path, "rb") as f:
                    return tomllib.load(f)
            else:
                print("Error: Install 'tomli' to use TOML configs.")
                return {}

        elif suffix in [".yaml", ".yml"]:
            try:
                import yaml
                with open(path, "r") as f:
                    return yaml.safe_load(f)
            except ImportError:
                print("Error: Install 'PyYAML' to use YAML configs.")
                return {}
    except Exception as e:
        print(f"Failed to parse {suffix} config: {e}")
        return {}

    return {}