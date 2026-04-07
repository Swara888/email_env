from fastapi import FastAPI
from pydantic import BaseModel
from my_env import EmailEnv, Action
import uvicorn

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


# ✅ ADD THIS (VERY IMPORTANT)
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# ✅ ALSO ADD THIS
if __name__ == "__main__":
    main()
