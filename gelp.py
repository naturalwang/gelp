#!/usr/bin/python3

import sys
import os
import json

from dataclasses import dataclass, asdict

log = print

__version__ = 1.0
__author__ = 'ran'

home_dir = os.path.expanduser('~')
db_file = '.gelp.json'
db_path = os.path.join(home_dir, db_file)

gelp_dict = {}


@dataclass
class GelpItem:
    command: str
    desc: str = ''

    def pretty_text(self) -> str:
        cmd = Color.light_blue(self.command)
        desc = Color.light_purple(self.desc)
        text = f'{cmd} {desc}'
        return text

    def pretty_print(self) -> None:
        text = self.pretty_text()
        log(text)


class Color:
    colors = {
        'light_red': '1;31',
        'light_green': '1;32',
        'light_blue': '1;34',
        'light_purple': '1;35',
        'light_cyan': '1;36',
        'no_color': '0',
    }
    # Black        0;30     Dark Gray     1;30
    # Red          0;31     Light Red     1;31
    # Green        0;32     Light Green   1;32
    # Brown/Orange 0;33     Yellow        1;33
    # Blue         0;34     Light Blue    1;34
    # Purple       0;35     Light Purple  1;35
    # Cyan         0;36     Light Cyan    1;36
    # Light Gray   0;37     White         1;37
    
    # RED='\033[0;31m'
    # NC='\033[0m' # No Color
    
    @classmethod
    def light_purple(cls, text: str):
        c = cls.colors['light_purple']
        nc = cls.colors['no_color']
        prefix = f'\033[{c}m'
        suffix = f'\033[{nc}m'
        return f'{prefix}{text}{suffix}'
    
    @classmethod
    def light_blue(cls, text: str):
        c = cls.colors['light_blue']
        nc = cls.colors['no_color']
        prefix = f'\033[{c}m'
        suffix = f'\033[{nc}m'
        return f'{prefix}{text}{suffix}'
    
    @classmethod
    def light_cyan(cls, text: str):
        c = cls.colors['light_cyan']
        nc = cls.colors['no_color']
        prefix = f'\033[{c}m'
        suffix = f'\033[{nc}m'
        return f'{prefix}{text}{suffix}'


def init() -> None:
    path = db_path
    if not os.path.exists(path):
        path = './gelp.json'
    if not os.path.exists(path):
        return
    with open(path, 'r') as f:
        content = f.read()
        try:
            gelp_dict.update(json.loads(content))
        except:
            pass


def usage() -> None:
    doc = """
gelp usage:
    $ gelp <action>
        print gelp for action
    $ gelp <action> "action description"
        save gelp for action
"""
    log(doc.strip())


def print_gelp() -> None:
    spoon = sys.argv[1]
    not_found = ['gelp action "{}" not found'.format(spoon)]
    gelps = gelp_dict.get(spoon, not_found)
    for i, g in enumerate(gelps):
        item = GelpItem(**g)
        item.pretty_print()


def print_gelp_all() -> None:
    # log('gelp_dict', gelp_dict)
    for spoon, items in gelp_dict.items():
        color_spoon = Color.light_cyan(f'[{spoon}]')
        item_texts = [GelpItem(**item).pretty_text() for item in items]
        # log('item_texts', item_texts)
        content = '\n'.join(item_texts)
        log(color_spoon)
        log(f'{content}')


def save_gelp() -> None:
    spoon = sys.argv[1]
    # log(f'gelp action "{spoon}" saved')
    cmd = sys.argv[2]
    desc = ' '.join(sys.argv[3:])

    item = GelpItem(cmd, desc)
    # log('item', asdict(item))
    gelp_dict[spoon] = gelp_dict.get(spoon, []) + [asdict(item)]
    with open(db_path, 'w') as f:
        text = json.dumps(gelp_dict, indent=2, ensure_ascii=False)
        f.write(text)


def __main() -> None:
    init()
    
    argc = len(sys.argv)
    log('sys.argv', sys.argv, argc)
    if argc == 2:
        if sys.argv[1] == '-a':
            action = print_gelp_all
        else:
            action = print_gelp
    elif argc == 3 or argc >= 4:
        action = save_gelp
    else:
        action = usage
    action()


if __name__ == '__main__':
    __main()