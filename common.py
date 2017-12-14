from enum import IntEnum

class IssueType(IntEnum):
    STORY = 1
    DEFECT = 2

class Resolution(IntEnum):
    COMPLETED = 1
    INVALID = 7
    DUPLICATE = 8
    REJECTED = 9

"""
10-19: Initial states
20-29: Definition states
30-39: Work states
40-49: Verification states
90-100: Final states
"""
"""class State(Enum):
    CREATED = 10
    IN_REFINEMENT = 20
    READY_TO_START = 30
    IN_IMPLEMENTATION = 31
    READY_FOR_REVIEW = 40
    IN_REVIEW = 41
    CLOSED = 100
"""

class State(IntEnum):
    CREATED = 1
    ONGOING = 50
    CLOSED = 100


state_name = {
    State.CREATED: 'Created',
    State.ONGOING: 'Ongoing',
    State.CLOSED: 'Closed'
}

valid_transitions = {
    State.CREATED: [State.ONGOING, State.CLOSED],
    State.ONGOING: [State.CLOSED],
    State.CLOSED: [State.CREATED]
}
