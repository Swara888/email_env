from pydantic import BaseModel
from typing import Tuple, Dict
import random

# ------------------ Models ------------------

class Observation(BaseModel):
    email: str

class Action(BaseModel):
    label: str  # spam / important / ignore / reply / urgent

# ------------------ Tasks with Confidence ------------------

TASKS = {
    "easy": [
        ("Win a free iPhone now!!!", "spam", 0.95),
        ("Congratulations! You've won a lottery", "spam", 0.9),
        ("Limited offer! Buy now!", "spam", 0.9),
        ("Click here to claim reward", "spam", 0.85),
        ("Earn money fast!!!", "spam", 0.95),
        ("Free coupons available", "spam", 0.85),
        ("Act now! Offer expires soon", "spam", 0.9),
        ("Get rich quick scheme", "spam", 0.95),
        ("You've been selected!", "spam", 0.85),
        ("Exclusive deal for you", "spam", 0.9),
    ],
    "medium": [
        ("Meeting with client tomorrow at 10am", "important", 0.9),
        ("Please review the attached document", "important", 0.85),
        ("Project deadline extended by 2 days", "important", 0.8),
        ("Team standup at 9 AM", "important", 0.85),
        ("Submit your report by EOD", "important", 0.9),
        ("Client feedback received", "important", 0.85),
        ("Schedule interview for candidate", "important", 0.8),
        ("Update on project status", "important", 0.75),
        ("Urgent: server downtime issue", "important", 0.95),
        ("Reminder: submit timesheet", "important", 0.8),
        ("Code review needed", "important", 0.85),
        ("Deployment scheduled tonight", "important", 0.9),
        ("New task assigned", "important", 0.8),
        ("Meeting rescheduled", "important", 0.75),
        ("Important update from manager", "important", 0.85),
    ],
    "hard": [
        ("Weekly newsletter: productivity tips", "ignore", 0.6),
        ("Reminder: optional webinar on growth", "ignore", 0.65),
        ("Hey, just checking in about last week’s update", "important", 0.6),
        ("Special discount just for you", "spam", 0.7),
        ("Your subscription is expiring soon", "important", 0.75),
        ("Check out our new features", "ignore", 0.6),
        ("Friendly reminder about meeting", "important", 0.7),
        ("We miss you! Come back", "spam", 0.7),
        ("Update your account details", "important", 0.8),
        ("Join our community event", "ignore", 0.6),
        ("Limited time offer for premium users", "spam", 0.75),
        ("Security alert: unusual login detected", "important", 0.9),
        ("Newsletter: tech trends", "ignore", 0.65),
        ("Action required: verify your email", "important", 0.85),
        ("Don't miss out!", "spam", 0.7),
        ("Follow up on previous conversation", "important", 0.6),
        ("Casual check-in mail", "ignore", 0.5),
        ("Survey request", "ignore", 0.55),
        ("Promotion inside!", "spam", 0.7),
        ("Important notice from HR", "important", 0.9),

        # Realistic / phishing
        ("Cl1ck h3re n0w!!!", "spam", 0.95),
        ("Your bank account is locked! Click link now", "spam", 0.95),
        ("URGENT: verify your account immediately", "spam", 0.9),
        ("Re: last week's meeting notes", "important", 0.6),
    ]
}

# ------------------ Environment ------------------

class EmailEnv:
    def __init__(self, task="easy"):
        self.task = task
        self.data = TASKS[task]
        self.step_count = 0
        self.max_steps = 2
        self.correct_label = None
        self.confidence = 1.0
        self.first_action = None  # 🔥 memory

    def reset(self) -> Observation:
        self.index = random.randint(0, len(self.data) - 1)
        self.step_count = 0

        email, label, confidence = self.data[self.index]

        # 🔥 Dynamic variation (VERY IMPORTANT)
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

        # ✅ invalid action handling
        if action.label not in ["spam", "important", "ignore", "reply", "urgent"]:
            return Observation(email="Invalid action"), 0.0, True, {}

        self.step_count += 1

        # Step 1: classification
        if self.step_count == 1:
            self.first_action = action.label

            if action.label == self.correct_label:
                reward = 0.5 * self.confidence
            else:
                reward = 0.0

            return Observation(email="Decide action: reply / ignore / urgent"), reward, False, {}

        # Step 2: action decision with memory
        elif self.step_count == 2:

            if self.first_action != self.correct_label:
                reward = 0.0  # penalty if first step wrong

            elif self.correct_label == "important" and action.label in ["reply", "urgent"]:
                reward = 0.5
            elif self.correct_label == "spam" and action.label == "ignore":
                reward = 0.5
            elif self.correct_label == "ignore" and action.label == "ignore":
                reward = 0.5
            else:
                reward = 0.0

            return Observation(email=""), reward, True, {}

        return Observation(email=""), 0.0, True, {}
