---
title: Email Triage Environment
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# AI Email Triage Environment

## Overview
This project simulates a real-world email classification system where an AI agent categorizes emails into:
- spam
- important
- ignore

## Tasks
- Easy: Obvious spam emails
- Medium: Work-related emails
- Hard: Ambiguous emails

## Action Space
- spam
- important
- ignore

## Observation Space
- Email text

## Reward System
- Correct classification: 1.0
- Partially correct: 0.5
- Incorrect: 0.0

## How it Works
The agent reads an email and chooses a label. The environment returns a reward based on correctness.

## How to Run
The environment runs automatically using Docker and executes `inference.py`.

## Motivation
Email overload is a real-world problem. This environment helps train AI agents to triage emails efficiently.