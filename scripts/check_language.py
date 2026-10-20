"""Catch East Asian script regressions in English-authored workspace files.

This is a focused regression guard, not a general language detector. It allows
scientific symbols, accented Latin names and immutable original evidence.
"""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SUFFIXES = {'.md', '.txt', '.toml', '.json', '.csv', '.py', '.yml', '.yaml'}
LOCAL_EVIDENCE = ('data/raw/', 'data/interim/', 'data/processed/', 'data/restricted/')
SCRIPT_RANGES = ((0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF),
                 (0x20000, 0x323AF), (0x3040, 0x30FF), (0xAC00, 0xD7AF))


def language_regressions(text):
    return [(line_number, f'U+{ord(character):04X}')
            for line_number, line in enumerate(text.splitlines(), 1)
            for character in line
            if any(start <= ord(character) <= end for start, end in SCRIPT_RANGES)]


def main():
    result = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
                            cwd=ROOT, capture_output=True, check=True)
    paths = sorted(set(result.stdout.decode().split('\0')) - {''})
    findings = []
    checked = 0
    for relative in paths:
        path = ROOT / relative
        if relative.startswith(LOCAL_EVIDENCE) or not path.is_file():
            continue
        if path.suffix.lower() not in SOURCE_SUFFIXES and path.name != 'Makefile':
            continue
        checked += 1
        findings.extend(f'{relative}:{line}: non-English script {codepoint}'
                        for line, codepoint in language_regressions(path.read_text(encoding='utf-8')))
    if findings:
        raise SystemExit('English-language regression detected:\n' + '\n'.join(findings[:30]))
    print(f'English-language regression check passed for {checked} authored files; local original evidence excluded.')


if __name__ == '__main__':
    main()
