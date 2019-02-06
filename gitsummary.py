import os
import subprocess

AUTHOR = '53rb3rn4r'


def parse_file(file):
    changed = insertions = deletions = 0
    for line_in_file in file:
        if 'file changed' in line_in_file or 'files changed' in line_in_file:
            line_in_file = line_in_file.strip()
            split_line = line_in_file.split(', ')
            for line in split_line:
                if ' changed' in line:
                    changed += get_int_from_line(line)
                elif '+' in line:
                    insertions += get_int_from_line(line)
                elif '-' in line:
                    deletions += get_int_from_line(line)
    return changed, insertions, deletions


def get_int_from_line(item):
    return int(item.split(' ')[0])


def summary_text(changed, insertions, deletions):
    return '%s\n%s\n%s' % (
        string_format(changed, 'files changed'),
        string_format(insertions, 'insertions'),
        string_format(deletions, 'deletions')
    )


def string_format(num, text, ljust=10):
    return '%s %s' % (str(num).ljust(ljust), text)


def main():
    filename = '.gitsummary'
    cmd = '''git log --author="%s" --oneline --shortstat > %s''' % (
        AUTHOR, filename
    )
    subprocess.run(cmd, shell=True, check=True)
    with open(filename) as f:
        file = f.readlines()
        changed, insertions, deletions = parse_file(file=file)
        text = summary_text(changed, insertions, deletions)
        print(text)
    os.remove(filename)


if __name__ == '__main__':
    main()
