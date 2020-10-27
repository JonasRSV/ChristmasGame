from abc import abstractmethod
from copy import copy
from collections import Counter
import random


class Santa(object):
    """ Because Santa decided the order, okay? """

    def __init__(self, application_state: "State"):
        self.application_state = application_state

    def __call__(self, gifts) -> list:
        self.application_state.logger.info(" --- Sorting Gifts --- ")
        self.application_state.logger.info("Number of Gifts: {}".format(
            len(gifts)))

        giftorder = self.sort(copy(gifts))

        self.application_state.logger.info("Sorting Score: {}".format(
            self.evaluate_sort(giftorder)))

        return giftorder

    def evaluate_sort(self, giftorder: list) -> float:
        max_delta = {}
        observation = {}

        score = 0
        previous_gift = None
        for index, gift in enumerate(giftorder):
            if gift not in observation:
                observation[gift] = index

            if gift not in max_delta:
                max_delta[gift] = 0

            max_delta[gift] = max(max_delta[gift], index - observation[gift] - 1)
            observation[gift] = index

            if gift == previous_gift:
                score += 100

            previous_gift = gift

        score += sum(max_delta.values())

        return score

    def sorting_statistics(self, giftorder: list) -> (float, float, float):
        """ Max delta & Goal & Random & Order """
        random_giftorder = copy(giftorder)
        random.shuffle(random_giftorder)

        random_eval = self.evaluate_sort(random_giftorder)
        heuristic_eval = self.evaluate_sort(giftorder)

        return heuristic_eval, random_eval

    @abstractmethod
    def sort(self, gifts: list) -> list:
        pass
