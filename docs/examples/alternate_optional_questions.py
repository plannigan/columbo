import columbo

initial_user_answers = columbo.get_answers(
    [columbo.Confirm("has_dog", "Do you have a dog?", default=True)]
)
if initial_user_answers["has_dog"]:
    interactions = [
        columbo.Echo(
            "Because you have have a dog, we want to ask you some more questions.",
        ),
        columbo.BasicQuestion(
            "dog_name",
            "What is the name of the dog?",
            default="Kaylee",
        ),
        columbo.BasicQuestion(
            "dog_breed",
            "What is the breed of the dog?",
            default="Basset Hound",
        ),
    ]
    user_answers = columbo.get_answers(interactions, answers=initial_user_answers)
else:
    user_answers = initial_user_answers

print(user_answers)
