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
        """ Max Delta """
        max_delta = 0
        observation = {}
        for index, gift in enumerate(giftorder):
            if gift not in observation:
                observation[gift] = 0

            max_delta = max(max_delta, index - observation[gift] - 1)
            observation[gift] = index

        for obs in observation.values():
            max_delta = max(max_delta, len(giftorder) - obs - 1)

        return max_delta

    def sorting_statistics(self, giftorder: list) -> (float, float, float):
        """ Max delta & Goal & Random & Order """
        random_giftorder = copy(giftorder)
        random.shuffle(random_giftorder)

        counts = Counter(giftorder)
        random_eval = self.evaluate_sort(random_giftorder)
        heuristic_eval = self.evaluate_sort(giftorder)
        goal_eval = int(len(giftorder) / (min(counts.values()) + 1))
        order_eval = max((sum(counts.values()) - min(counts.values()) * (len(counts) - 2)) + 1, len(counts))

        return heuristic_eval, goal_eval, random_eval, order_eval

    @abstractmethod
    def sort(self, gifts: list) -> list:
        pass
