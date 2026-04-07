from fastapi import FastAPI
from pydantic import BaseModel
from my_env import EmailEnv, Action

app = FastAPI()

env = EmailEnv()

class StepInput(BaseModel):
    label: str

@app.post("/reset")
def reset():
    obs = env.reset()
    return {"email": obs.email}

@app.post("/step")
def step(action: StepInput):
    obs, reward, done, info = env.step(Action(label=action.label))
    return {
        "email": obs.email,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return {"state": "running"}
