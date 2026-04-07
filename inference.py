import os
from openai import OpenAI
from my_env import EmailEnv, Action

API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
API_KEY = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)


def log_start(task):
    print(f"[START] task={task} env=email-env model={MODEL_NAME}", flush=True)


def log_step(step, action, reward, done):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null",
        flush=True,
    )


def log_end(success, steps, score, rewards):
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


def run_task(task):
    env = EmailEnv(task)
    log_start(task)

    obs = env.reset()
    rewards = []

    for step in range(3):
        prompt = f"""
        Step {step}:
        Email: {obs.email}
        
        Choose one:
        - spam
        - important
        - ignore
        - reply
        - urgent
        
        Only output one word.
        """

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )

        action_text = response.choices[0].message.content.strip().lower()

        # safety fallback
        if action_text not in ["spam", "important", "ignore"]:
            action_text = "ignore"

        action = Action(label=action_text)

        obs, reward, done, _ = env.step(action)
        rewards.append(reward)

        log_step(step + 1, action_text, reward, done)

        if done:
            break

    score = sum(rewards) / len(rewards)
    success = score > 0.3

    log_end(success, len(rewards), score, rewards)


if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run_task(task)


import time
time.sleep(120)