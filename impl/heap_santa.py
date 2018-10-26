from santa import Santa
from overrides import overrides
from collections import Counter
import heapq


class SantaImpl(Santa):
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

