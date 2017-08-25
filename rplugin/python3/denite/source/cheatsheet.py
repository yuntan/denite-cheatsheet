import os
from os.path import isfile, expanduser
from unicodedata import east_asian_width
from typing import Dict

from .base import Base


class Source(Base):

    def __init__(self, nvim):
        super().__init__(nvim)

        self.name = 'cheatsheet'
        self.kind = 'command'
        self.vars = {
            'cheatsheet_tsv': '~/.config/nvim/cheatsheet.tsv',
            'mapping_prefix': '⌘ ',
            'command_len_max': 30,
        }

        self._nvim = nvim

    def gather_candidates(self, context):
        columns = self._nvim.eval('&columns')
        ambiwidth = self._nvim.eval('&ambiwidth') == "double"

        path = expanduser(self.vars['cheatsheet_tsv'])
        if not isfile(path) or not os.access(path, os.R_OK):
            self._nvim.err_write(
                '{} dosen\'t exist or is not readable\n'.format(path))
            return []

        def is_valid_line(line: str) -> bool:
            # line with leading # is comment
            # line which has less or more than 4 columns is not valid
            return line and line[0] != '#' and len(line.split('\t')) == 4

        def get_cand(line: str) -> Dict[str, str]:
            genre, desc, mapping, command = line.split('\t')
            return {
                'genre': genre,
                'desc': desc,
                'mapping': mapping,
                'command': command[:-1],  # remove trailing \n
            }

        with open(path, 'r') as f:
            cands = [get_cand(line)
                     for line in f.readlines()
                     if is_valid_line(line)]

        def get_width(s: str):
            def get_eaw(c: str) -> int:
                w = east_asian_width(c)
                if w == 'F' or w == 'W': return 2
                if w == 'A' and ambiwidth: return 2
                return 1

            return sum([get_eaw(c) for c in s])

        width_genre = max([get_width(cand['genre']) for cand in cands]) + 2
        width_command = min(
            max([get_width(cand['command']) for cand in cands]),
            self.vars['command_len_max'])
        width_mapping = get_width(self.vars['mapping_prefix']) + \
            max([get_width(cand['mapping']) for cand in cands])

        # [GENRE] COMMAND -- DESC ⌘ MAPPING
        width_desc = (columns - 1  # denite right padding
                      - (width_genre + 1 + width_command + 4  # + width_desc
                         + 1 + width_mapping))

        def justify(s: str, width: int) -> str:
            s = s.ljust(width)
            while get_width(s) > width:
                s = s[:-1]
            return s

        s = '{genre} {command} -- {desc} {mapping}'
        return [{
            'word': s.format(
                genre=justify(
                    '[{}]'.format(cand['genre']) if cand['genre'] else '',
                    width_genre),
                command=justify(cand['command'], width_command),
                desc=justify(cand['desc'], width_desc),
                mapping=(self.vars['mapping_prefix']
                         + cand['mapping'] if cand['mapping'] else '')),
            'kind': 'command',
            'action__command': cand['command'],
        } for cand in cands]
