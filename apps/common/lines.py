import json
from config import ROOT_DIR


with open(f'{ROOT_DIR}/lines.json', mode='r') as f:
    LINES = json.load(f)


if __name__ == '__main__':
    print(LINES)

