import os
from collections import deque
from enum import IntEnum, unique
import regex

__all__ = ['walk']

@unique
class _FSWalkMatchResult(IntEnum):
    no_match = 1
    match = 0
    partial = -1


def _match(rule, path):
    m = regex.fullmatch(rule, path, partial=True)
    if not m:
        return _FSWalkMatchResult.no_match
    # Seems we cannot get a complete match result out of a
    # partial match object
    m = regex.fullmatch(rule, path)
    if not m:
        return _FSWalkMatchResult.partial
    return _FSWalkMatchResult.match


def walk(path, rules, base_path=None):
    def normalize_relpath(relpath):
        return '' if relpath == os.path.curdir else relpath

    if base_path is None:
        base_path = path
    abspath = os.path.abspath(path)
    relpath = os.path.relpath(path, base_path)
    relpath = normalize_relpath(relpath)
    file_type = 'dir' if os.path.isdir(abspath) else 'file'

    inner_rules = []
    for rule in rules:
        match_result = _match(rule, relpath)
        if match_result == _FSWalkMatchResult.match:
            yield ('match', file_type, relpath, abspath, rule)
            return
        elif match_result == _FSWalkMatchResult.partial:
            inner_rules.append(rule)
    if not inner_rules:
        yield ('nomatch', file_type, relpath, abspath, None)
        return

    nomatch_buffer = deque()
    has_matched_children = False
    if not os.path.isdir(abspath):
        yield ('nomatch', file_type, relpath, abspath, None)
        return
    for item in os.listdir(abspath):
        item_abspath = os.path.join(abspath, item)
        for ret in walk(item_abspath, inner_rules, base_path):
            if ret[0] == 'match':
                has_matched_children = True
                while nomatch_buffer:
                    yield nomatch_buffer.popleft()
                yield ret
            else:
                nomatch_buffer.append(ret)

    if has_matched_children:
        while nomatch_buffer:
            yield nomatch_buffer.popleft()
    else:
        yield ('nomatch', file_type, relpath, abspath, None)
