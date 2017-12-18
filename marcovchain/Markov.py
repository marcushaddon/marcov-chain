"""Module of classes for implementing a Markov Chain."""

import random
import json
from collections import defaultdict as dd
from helpers import weighted_random_choice


class MarkovState(object):
    """Class for implimenting a possible state of a markov chain."""

    def __init__(self, state, states=None):
        """Initialize an instance of a markov state."""
        self.state = state
        self.states = states or dd(int)

    def next(self):
        """Choose next state."""
        if self.states is not None:
            choices = [(self.states[state], state) for state in self.states]
            return weighted_random_choice(choices)
        return None

    def recordtransition(self, state, amt=1):
        """Increment weight of edge between state and provided state."""
        self.states[state] += amt

    def freeze(self):
        """Prepare for pickling."""
        self.states = dict(self.states)

    def unfreeze(self):
        """Re-prepare for training after unpickling."""
        self.states = dd(int, self.states)


class MarkovChain(object):
    """Class for implementing a Markov Chain."""

    def __init__(self, states=None):
        """Initialize instance of MarkovChain."""
        self.state = None
        self.states = states or {}
        self.temp = 0
        self._frozen = False

    def addstate(self, state):
        """Add state to possible states of Markov Chain."""
        if state not in self.states:
            self.states[state] = MarkovState(state)

    def getstate(self, state):
        """Get specified state (or create it if it doesn't exist)."""
        if not state in self.states:
            self.states[state] = MarkovState(state)
        return self.states[state]

    def setstate(self, state):
        """Set state of Markov."""
        if state not in self.states:
            return False
        self.state = self.states[state]
        return True

    def next(self):
        """Transition to next state."""
        if self.state is None or self.state.next() is None:
            choice = random.choice(self.states.keys())
            self.state = self.states[choice]
        else:
            nextstate = self.state.next()
            self.state = self.states[nextstate[1]]
        return self.state.state

    def freeze(self):
        """Prepare for pickling."""
        for state in self.states:
            self.states[state].freeze()
        self._frozen = True

    def unfreeze(self):
        """Re-prepare for training after unpickling."""
        for state in self.states:
            self.states[state].unfreeze()
        self._frozen = False

    def to_json(self):
        """Preserve a 'trained' chain in JSON form."""
        if not self._frozen:
            self.freeze()
        return json.dumps({state: self.states[state].states for state in self.states})

    @classmethod
    def from_json(cls, jsonfile):
        """Reinitialize a chain from a json file."""
        with open(jsonfile, 'rb') as infile:
            states = json.load(infile)

        states = {state: MarkovState(state, states[state]) for state in states}
        inst = cls(states)
        inst.unfreeze()
        return inst
