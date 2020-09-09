from pathlib import Path
from appdirs import user_config_dir
import configparser

from .process_flights import version, AirspaceHandler

# Config

config_dir = Path(user_config_dir("flight_processing"))
config_file = config_dir / "flight_processing.conf"

if not config_dir.exists():
    config_template = (Path(__file__).parent / "flight_processing.conf").read_text()
    config_dir.mkdir(parents=True)
    config_file.write_text(config_template)

config = configparser.ConfigParser()
config.read(config_file.as_posix())