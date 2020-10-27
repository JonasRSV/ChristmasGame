from santa import Santa
from overrides import overrides
from collections import Counter
from typing import List
import heapq
import numpy as np
import numba


class HeapSanta(Santa):
    @overrides
    def sort(self, gifts: list) -> list:
        """Heuristic for delivering gifts"""
        heap = [[
            int(len(gifts) / (count + 1)), count,
            int(len(gifts) / (count + 1)), name
        ] for name, count in Counter(gifts).items()]

        heapq.heapify(heap)
        order = []

        while heap:
            person = heapq.heappop(heap)
            if person[1] <= 0:
                continue
            order.append(person[3])
            person[1] -= 1
            person[0] += person[2]
            heapq.heappush(heap, person)

        return order


@numba.jit(nopython=True, forceobj=False)
def ga_fitness(gifts: np.ndarray, user_ids: np.ndarray):
    inverse_fitness = 0
    for user in user_ids:
        maximum_waiting_time = 0
        waiting_time = 0

        previous_gift = -1
        for gift in gifts:
            if waiting_time > maximum_waiting_time:
                maximum_waiting_time = waiting_time

            waiting_time += 1

            if gift == user:
                waiting_time = 0

            # Really bad
            if previous_gift == gift:
                inverse_fitness += 100

            previous_gift = gift

        inverse_fitness += waiting_time

    return 1 / inverse_fitness


class GaOptimizingSanta(Santa):

    @staticmethod
    @numba.jit(nopython=True)
    def __optimizer(gifts: np.ndarray, user_ids: np.ndarray, iterations: int):

        fitness = ga_fitness(gifts, user_ids)
        for _ in range(iterations):
            swaps = np.random.randint(1, 5)

            _from = np.random.randint(0, gifts.size, size=swaps)
            _to = np.random.randint(0, gifts.size, size=swaps)

            _candidate = gifts.copy()
            for i in range(swaps):
                _candidate[_from[i]], _candidate[_to[i]] = _candidate[_to[i]], _candidate[_from[i]]

            _candidate_fitness = ga_fitness(_candidate, user_ids)

            if _candidate_fitness > fitness:
                fitness = _candidate_fitness
                gifts = _candidate

        return gifts

    @overrides
    def sort(self, gifts: List[str]) -> List[str]:

        gifts = HeapSanta.sort(None, gifts)

        unique_classes = list(set(gifts))

        # Representing as integers will allow for faster computation
        unique_int_gifts = np.arange(len(unique_classes))
        int_gifts = np.array([unique_classes.index(elem) for elem in gifts])

        initial_fitness = ga_fitness(int_gifts, unique_int_gifts)

        order = GaOptimizingSanta.__optimizer(int_gifts, unique_int_gifts, iterations=2000000)

        final_fitness = ga_fitness(order, unique_int_gifts)

        return list(np.array(unique_classes)[order])
