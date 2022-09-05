import os
import sys
from config import APPConfig
from apps.common.commands.manager import manager

sys.path.append(os.path.dirname(__file__))

activate_this = f'{APPConfig.ROOT_DIR}/venv/bin/activate_this.py'

with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))


if __name__ == '__main__':
    manager.run()
