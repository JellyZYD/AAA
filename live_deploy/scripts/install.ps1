$ErrorActionPreference = "Stop"
python -m pip install -e ".[data]"
python -m qihuo_signal env-check

