from sorting import Santa
from overrides import overrides

class SantaImpl(Santa):

    @overrides
    def sort(self, gifts: list) -> list:
        # This is WIP

        entities = {}
        for gift in gifts:
            if gift not in entities:
                entities[gift] = 0

            entities[gift] += 1


        return gifts
