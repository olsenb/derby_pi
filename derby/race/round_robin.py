

from base import RaceBase


class RoundRobin(RaceBase):

    def generate_heats(self, current_round):
        lineup = []
        for offset in range(current_round):
            lineup += self.cars[offset::current_round]
        return self.chunks(lineup, self.lanes, current_round)
