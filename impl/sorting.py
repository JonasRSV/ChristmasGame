from sorting import Santa
from overrides import overrides
import random

class SantaImpl(Santa):

    @overrides
    def sort(self, gifts: list) -> list:
        random.shuffle(gifts)
        return gifts
