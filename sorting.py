from abc import abstractmethod
from copy import copy
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
        """ Average max delta """
        losses = {}
        gifts = {}
        for index, gift in enumerate(giftorder):
            if gift not in gifts:
                gifts[gift] = 0
                losses[gift] = 0

            losses[gift] = max(index - gifts[gift], losses[gift])
            gifts[gift] = index

        for gift, occurrence in gifts.items():
            losses[gift] = max(len(giftorder) - occurrence, losses[gift])

        return sum(losses.values()) / len(losses)

    def sorting_statistics(self, giftorder: list) -> (float, float, float):
        """ Average max delta & Goal & Random """
        random_giftorder = copy(giftorder)
        random.shuffle(random_giftorder)

        random_eval = self.evaluate_sort(random_giftorder)
        heuristic_eval = self.evaluate_sort(giftorder)

        items = {}
        for item in giftorder:
            if item in items:
                items[item] += 1
            else:
                items[item] = 1

        """ 
        Math. 
        
        How to most efficiently divide giftorder 
        with item_occurrence elements
        """
        error = 0
        for item_occurrence in items.values():
            error += len(giftorder) / (item_occurrence + 1)

        goal_eval = error / len(items)

        return heuristic_eval, goal_eval, random_eval

    @abstractmethod
    def sort(self, gifts: list) -> list:
        pass
