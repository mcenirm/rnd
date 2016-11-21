#!/usr/bin/env python3

from random import SystemRandom


class MorselCategory():
    def __init__(self, characters=None):
        self.count = len(characters)
        if self.count < 1:
            raise ValueError('Characters should not be empty')
        self.characters = characters


DIGITS = MorselCategory(characters='0123456789')
SAFE_UPPER = MorselCategory(characters='ABCDEFGHJKMNPQRSTVWXY')
SAFE_LOWER = MorselCategory(characters='abcdefghjkmnpqrstvwxy')
PUNCT = MorselCategory(characters='''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''')


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


if __name__ == '__main__':
    result = DEFAULT_RULE.rnd()
    print(result)
