from pydantic import BaseModel
from typing import Tuple, Dict
import random

# ------------------ Models ------------------

class Observation(BaseModel):
    email: str

class Action(BaseModel):
    label: str

# ------------------ Tasks ------------------

TASKS = {
    "easy": [
        ("Win a free iPhone now!!!", "spam", 0.95),
        ("Congratulations! You've won a lottery", "spam", 0.9),
        ("Limited offer! Buy now!", "spam", 0.9),
    ],
    "medium": [
        ("Meeting with client tomorrow at 10am", "important", 0.9),
        ("Please review the attached document", "important", 0.85),
        ("Project deadline extended by 2 days", "important", 0.8),
    ],
    "hard": [
        ("Weekly newsletter: productivity tips", "ignore", 0.6),
        ("Reminder: optional webinar on growth", "ignore", 0.65),
        ("Hey, just checking in about last week’s update", "important", 0.6),
        ("Your bank account is locked! Click link now", "spam", 0.95),
    ]
}

# ------------------ Environment ------------------

class EmailEnv:
    def __init__(self, task="easy"):
        self.task = task
        self.data = TASKS[task]
        self.step_count = 0
        self.correct_label = None
        self.confidence = 1.0
        self.first_action = None

    def reset(self) -> Observation:
        self.index = random.randint(0, len(self.data) - 1)
        self.step_count = 0

        email, label, confidence = self.data[self.index]

        # dynamic variation
        variations = [
            email,
            email.upper(),
            email + " !!!",
            email.replace("o", "0"),
            "URGENT: " + email,
            email + " please respond ASAP"
        ]

        email = random.choice(variations)

        self.correct_label = label
        self.confidence = confidence
        self.first_action = None

        return Observation(email=email)

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict]:

        # ✅ FIXED: no 0.0 reward
        if action.label not in ["spam", "important", "ignore", "reply", "urgent"]:
            return Observation(email="Invalid action"), 0.1, True, {}

        self.step_count += 1

        # ---------------- STEP 1 ----------------
        if self.step_count == 1:
            self.first_action = action.label

            if action.label == self.correct_label:
                reward = 0.4 * self.confidence   # always < 1
            else:
                reward = 0.1   # NOT 0

            return Observation(email="Decide action: reply / ignore / urgent"), reward, False, {}

        # ---------------- STEP 2 ----------------
        elif self.step_count == 2:

            if self.first_action != self.correct_label:
                reward = 0.1

            elif self.correct_label == "important" and action.label in ["reply", "urgent"]:
                reward = 0.6
            elif self.correct_label == "spam" and action.label == "ignore":
                reward = 0.6
            elif self.correct_label == "ignore" and action.label == "ignore":
                reward = 0.6
            else:
                reward = 0.2

            return Observation(email=""), reward, True, {}

        return Observation(email=""), 0.1, True, {}
