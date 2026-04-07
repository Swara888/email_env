Hugging Face's logo

Spaces:
swara-123
/
emai 

like
0

App
Files
Community
Settings
emai
/
my_env.py

swara-123's picture
swara-123
Update my_env.py
6494b0b
verified
raw

Copy download link
history
blame
edit
delete
2.47 kB
from pydantic import BaseModel
from typing import Tuple, Dict
import random

# ------------------ Models ------------------

class Observation(BaseModel):
    email: str

class Action(BaseModel):
    label: str  # spam / important / ignore / reply / urgent

class Reward(BaseModel):
    score: float


# ------------------ Tasks ------------------

TASKS = {
    "easy": [
        ("Win a free iPhone now!!!", "spam"),
        ("Congratulations! You've won a lottery", "spam"),
        ("Limited offer! Buy now!", "spam"),
    ],
    "medium": [
        ("Meeting with client tomorrow at 10am", "important"),
        ("Please review the attached document", "important"),
        ("Project deadline extended by 2 days", "important"),
    ],
    "hard": [
        ("Weekly newsletter: productivity tips", "ignore"),
        ("Reminder: optional webinar on growth", "ignore"),
        ("Hey, just checking in about last week’s update", "important"),
    ]
}


# ------------------ Environment ------------------

class EmailEnv:
    def __init__(self, task="easy"):
        self.task = task
        self.data = TASKS[task]
        self.index = 0
        self.step_count = 0
        self.max_steps = 2
        self.correct_label = None

    def reset(self) -> Observation:
        import random
        self.index = random.randint(0, len(self.data)-1)
        self.step_count = 0
        self.correct_label = self.data[self.index][1]
        return Observation(email=self.data[self.index][0])

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict]:
        self.step_count += 1

        # Step 1: classification
        if self.step_count == 1:
            if action.label == self.correct_label:
                reward = 0.5
            else:
                reward = 0.0
            done = False
            return Observation(email="Decide action: reply / ignore / urgent"), reward, done, {}

        # Step 2: action decision
        elif self.step_count == 2:
            if self.correct_label == "important" and action.label in ["reply", "urgent"]:
                reward = 0.5
            elif self.correct_label == "spam" and action.label == "ignore":
                reward = 0.5
            else:
                reward = 0.0

            done = True
            return Observation(email=""), reward, done, {}


    def state(self) -> Dict:
        return {
            "task": self.task,
            "step_count": self.step_count
    }
