#!/usr/bin/env python3

from random import SystemRandom


def rnd():
    r = SystemRandom()
    results = [r.choice(r'''ABCDEFGHJKMNPQRSTVWXYabcdefghjkmnpqrstvwxy0123456789!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''') for x in range(16)]
    return ''.join(results)


if __name__ == '__main__':
    print(rnd())
