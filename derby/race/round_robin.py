from collections import deque

class RaceBase(object):
    MAX_ROUNDS = 30

    def __init__(self, lanes, cars, rounds):
        self.rounds = min(rounds, self.MAX_ROUNDS)
        self.cars = cars
        self.lanes = lanes

    def generate_heats(self, current_round):
        """
        Create the heats for a single round.
        Should return a list of heats containing a the list of cars
        """
        raise NotImplementedError

    def list_racer_opponent(self, rounds):
        racers = [[] for i in self.cars]
        for rd in rounds:
            for h in rd:
                for l in h:
                    racers[l].extend(h)
        return racers

    def list_racer_lanes(self, rounds):
        totals = [[0 for j in self.lanes] for i in self.cars]
        for rd in rounds:
            for h in rd:
                for i, l in enumerate(h):
                    totals[l][i] += 1
        return totals


class RoundRobin(RaceBase):
    def generate_rounds(self):
        rounds = []
        for r in range(1, self.rounds + 1):
            rounds.append(self.generate_heats(r))
        return rounds

    def generate_heats(self, current_round):
        def chunks(l, n, rotate=0):
            c = []
            for i in range(0, len(l), n):
                d = deque(l[i:i+n])
                d.rotate(-rotate)
                c.append(list(d))
            return c

        lineup = []
        for offset in range(current_round):
            lineup += self.cars[offset::current_round]
        return chunks(lineup, self.lanes, current_round)
