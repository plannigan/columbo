import columbo

interactions = [
    columbo.Echo("Welcome to the Columbo example"),
    columbo.Acknowledge("Press enter to start"),
    columbo.BasicQuestion(
        "user",
        "What is your name?",
        default="Patrick",
    ),
    columbo.BasicQuestion(
        "user_email",
        lambda answers: f"""What email address should be used to contact {answers["user"]}?""",
        default="me@example.com",
    ),
    columbo.Choice(
        "mood",
        "How are you feeling today?",
        options={
            "happy": "😀",
            "sad": "😢",
            "sleepy": "🥱",
            "confused": "🤔",
        },
        default="happy",
    ),
    columbo.Confirm("likes_dogs", "Do you like dogs?", default=True),
]

answers = columbo.get_answers(interactions)
print(answers)
