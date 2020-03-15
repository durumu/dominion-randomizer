from lib import shortname
import sys

answers = []

for line in sys.stdin:
    for fullname in line.split(','):
        answers.append(shortname(fullname))

print(*answers, sep='\n')
