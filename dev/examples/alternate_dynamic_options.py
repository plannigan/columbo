import random

import columbo


def get_dog_breeds() -> list[str]:
    # In the real world this might actually be a GET request to an external server.
    possible_breeds = [
        "Basset Hound",
        "Great Dane",
        "Golden Retriever",
        "Poodle",
        "Dachshund",
    ]
    return random.choices(possible_breeds, k=random.randint(2, len(possible_breeds)))


all_dogs = get_dog_breeds()
interactions = [
    columbo.Choice(
        name="favorite",
        message="Which dog breed do you like best?",
        options=all_dogs,
        default=all_dogs[0],
    )
]
print(columbo.get_answers(interactions))
