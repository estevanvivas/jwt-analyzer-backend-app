from pathlib import Path
from automata.tm.dtm import DTM
from turing_machine.loader import load_tm

config_path = Path(__file__).parent / 'b64_encode_tm_config.json'

if not config_path.exists():
    raise FileNotFoundError(f"Config file not found: {config_path}")

b64_encode_tm: DTM = load_tm(str(config_path))
