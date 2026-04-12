from fastapi import FastAPI
from pydantic import BaseModel
from my_env import EmailEnv, Action
from typing import Optional

app = FastAPI()

envs = {}

# ------------------ Models ------------------

class ResetInput(BaseModel):
    task: str

class StepInput(BaseModel):
    label: str

# ------------------ Routes ------------------

@app.get("/")
def home():
    return {"message": "EmailEnv running"}


@app.post("/reset")
def reset(input: Optional[ResetInput] = None):

    # ✅ Default task if no input
    task = "easy"

    if input and input.task:
        if input.task not in ["easy", "medium", "hard"]:
            return {"error": "Invalid task"}
        task = input.task

    envs["current"] = EmailEnv(task)
    obs = envs["current"].reset()

    return {
        "observation": {"email": obs.email}
    }

@app.post("/step")
def step(action: StepInput):
    env = envs.get("current")

    if not env:
        return {"error": "Call /reset first"}

    obs, reward, done, info = env.step(Action(label=action.label))

    return {
        "observation": {"email": obs.email},
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return {"status": "running"}
