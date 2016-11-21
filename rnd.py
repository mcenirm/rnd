#!/usr/bin/env python3

from random import SystemRandom


def rnd(characters=r'''ABCDEFGHJKMNPQRSTVWXYabcdefghjkmnpqrstvwxy0123456789!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''' ,length=16):
    r = SystemRandom()
    results = [r.choice(characters) for x in range(16)]
    return ''.join(results)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        result = rnd(characters=sys.argv[1])
    else:
        result = rnd()
    print(result)
