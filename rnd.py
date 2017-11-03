#!/usr/bin/env python3

from random import SystemRandom
import string


class MorselCategory():
    def __init__(self, characters=None):
        self.count = len(characters)
        if self.count < 1:
            raise ValueError('Characters should not be empty')
        self.characters = ''.join(sorted(set(characters)))


# cf https://ux.stackexchange.com/a/53345
ambiguous_letters = {
    # 'B', # 8
    # 'D', # Q
    # 'G', # 6
    'I', # 1
    'l', # 1
    'O', # 0
    # 'Q', # D
    # 'S', # 5
    'Z', # 2
}

unsafe_letters = {
    'L',
    'U', # cf https://en.wikipedia.org/wiki/Base32#Crockford.27s_Base32
}

ambiguous_or_unsafe_letters = ambiguous_letters | unsafe_letters


DIGITS = MorselCategory(characters=string.digits)
SAFE_UPPER = MorselCategory(characters=set(string.ascii_uppercase)-ambiguous_or_unsafe_letters)
SAFE_LOWER = MorselCategory(characters=set(string.ascii_lowercase)-ambiguous_or_unsafe_letters)
PUNCT = MorselCategory(characters=string.punctuation)


class CategoryBasedRule():
    def __init__(self, length=12, category_quorum=1, random=SystemRandom()):
        self.length = length
        self.category_quorum = category_quorum
        self.random = random
        self.categories = []

    def addCategory(self, category):
        self.categories.append(category)

    def rnd(self):
        def elect_quorum(input_list, quorum_size, random):
            quorum = list(input_list)
            random.shuffle(quorum)
            return quorum[:quorum_size]

        def construct_template(categories, quorum_size, length, random):
            template = []
            quorum = elect_quorum(
                    categories,
                    quorum_size,
                    random,
                )
            for category in quorum:
                template.append(category)
            for i in range(len(template), length):
                category = random.choice(categories)
                template.append(category)
            random.shuffle(template)
            return template

        template = construct_template(
                self.categories,
                self.category_quorum,
                self.length,
                self.random,
            )
        value = ''.join([
            self.random.choice(category.characters) for category in template
        ])
        return value


DEFAULT_RULE = CategoryBasedRule(
        length=16,
        category_quorum=3,
    )
DEFAULT_RULE.addCategory(category=DIGITS)
DEFAULT_RULE.addCategory(category=SAFE_UPPER)
DEFAULT_RULE.addCategory(category=SAFE_LOWER)
DEFAULT_RULE.addCategory(category=PUNCT)

SAFARI_WORD_COUNT = 4
SAFARI_WORD_LENGTH = 3
SAFARI_RULE = CategoryBasedRule(length=SAFARI_WORD_LENGTH*SAFARI_WORD_COUNT, category_quorum=2)
SAFARI_RULE.addCategory(category=DIGITS)
SAFARI_RULE.addCategory(category=SAFE_UPPER)
SAFARI_RULE.addCategory(category=SAFE_LOWER)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == '--safari':
            result = SAFARI_RULE.rnd()
            result = '-'.join([result[i*SAFARI_WORD_LENGTH:(i+1)*SAFARI_WORD_LENGTH] for i in range(SAFARI_WORD_COUNT)])
        else:
            print('Usage: {} [--safari]'.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)
    else:
        result = DEFAULT_RULE.rnd()
    print(result)
