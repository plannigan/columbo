import columbo


def went_left(answers: columbo.Answers) -> bool:
    return answers["which_door"] == "left"


def went_right(answers: columbo.Answers) -> bool:
    return answers["which_door"] == "right"


def outcome(answers: columbo.Answers) -> str:
    if answers.get("has_key", False):
        return "You try the the key on the lock. With a little jiggling, it finally opens. You open the gate and leave."
    if answers.get("has_hammer", False):
        return "You hit the lock with the hammer and it falls to the ground. You open the gate and leave."
    return (
        "Unable to open the gate yourself, you yell for help. A farmer in the nearby field hears you. "
        "He reaches into his pocket and pulls out a key to unlock the gate and open it. "
        "As you walk through the archway he says, "
        '"What I don\'t understand is how you got in there. This is the only key."'
    )


interactions = [
    columbo.Echo(
        "You wake up in a room that you do not recognize. "
        "In the dim light, you can see a large door to the left and a small door to the right."
    ),
    columbo.Choice(
        "which_door",
        "Which door do you walk through?",
        options=["left", "right"],
        default="left",
    ),
    columbo.Echo(
        "You step into a short hallway and the door closes behind you, refusing to open again. "
        "As you walk down the hallway, there is a small side table with a key on it.",
        should_ask=went_left,
    ),
    columbo.Confirm(
        "has_key",
        "Do you pick up the key before going through the door at the other end?",
        should_ask=went_left,
        default=True,
    ),
    columbo.Echo(
        "You step into smaller room and the door closes behind, refusing to open again. "
        "The room has a single door on the opposite side of the room and a work bench with a hammer on it.",
        should_ask=went_right,
    ),
    columbo.Confirm(
        "has_hammer",
        "Do you pick up the hammer before going through the door at the other side?",
        should_ask=went_right,
        default=True,
    ),
    columbo.Echo(
        "You enter a small courtyard with high walls. There is an archway that would allow you to go free, "
        "but the gate is locked."
    ),
    columbo.Echo(outcome),
]

user_answers = columbo.get_answers(interactions)
print(user_answers)
