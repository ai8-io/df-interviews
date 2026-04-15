# Round 3A — System design (candidate brief)

## What this round is

- **Format:** Conversation with a whiteboard or shared drawing surface (or sketching on paper you hold up to camera). You do **not** need to write production code.
- **Duration:** About **35–40 minutes**, plus a short break before the live coding round.
- **Goal:** We want to see how you **structure a problem**, **make tradeoffs**, and **reason about real-world constraints** (latency, cost, failure, security, user experience, migration). There is rarely a single “correct” architecture.

## What to do in the first few minutes

- **Listen to the full prompt** your interviewers give you on the call.
- **Ask clarifying questions** before you lock into a design. Examples: scale (ten customers vs thousands), who the users/operators are, whether this is greenfield or an evolution from an existing system, latency expectations, compliance boundaries, and what “MVP” vs “ideal” means for this exercise.
- **State assumptions explicitly** if the prompt leaves something open. We care that you know you’re assuming, not that your assumptions match ours perfectly.

## How the conversation usually flows

1. You propose an approach (top-level components, data flow, and main interfaces).
2. You go deeper on the areas you think matter most.
3. Interviewers may **pick an area to stress-test** (failure modes, cost, consistency, UX while something slow happens, incremental rollout, etc.). This is normal — it is not a hint that you “got the question wrong.”

## What we tend to care about (general)

Without binding any specific interview:

- **End-to-end thinking** — not only servers and databases, but what the user or operator experiences while things start, run, fail, or wait.
- **Tradeoffs** — e.g. isolation vs cold start, consistency vs complexity, simplicity of MVP vs a roadmap to something stronger.
- **Operational reality** — crashes, partial failures, idempotency, backoff, and what “safe” means when agents or automation can take side-effecting actions.
- **Incremental change** — how you would move from today’s system toward a better one without a risky big-bang cutover.

---

## Design scenarios (read the one that matches your interview)

Your invite or your interviewers will indicate whether the role is **platform / runtime–oriented** or **AI / agent-quality–oriented**. **You will only be asked one path in the interview**; the other is included here so you are not surprised by the repo layout.

### A — Platform / runtime–oriented scenario

> We have an AI platform where agents do work for businesses — research, writing, data processing, outreach, and similar tasks. Today, all agents run in a **monolithic Python service** on Kubernetes. Every tool call is a stateless Python function. **Code execution** is the only workload that already runs in a **sandbox**, and that sandbox creates a **fresh instance per call**.
>
> We want to move toward **per-agent (or per-task) isolation** — for example **dedicated containers** or an equivalent isolation boundary — for three reasons:
>
> 1. **Security** — agents need to execute arbitrary code (scripts, data processing, package installs). We do not want that in a shared process with other tenants or sessions.
> 2. **Capabilities (“skills”)** — we want to ship **pre-made scripts and environments** an agent can use without a full product deploy for every new capability.
> 3. **Isolation and scaling** — concurrent agents currently share process and memory; a runaway agent can hurt others, and there is no hard boundary between sessions.
>
> **Your task:** Design the **runtime architecture** for going from the monolithic agent service to **isolated per-task (or per-agent) execution** that can run code, use those capabilities, and **stream results back to users in real time**.

Use only what your interviewers confirm on the call for stack, scale, and constraints.

### B — AI / agent-quality–oriented scenario

> Same starting picture: an AI platform where agents do work for businesses, today in a **monolithic Python service**, and we want **isolated per-agent containers** (or equivalent isolation) for security and scaling.
>
> **Focus for you:** Assume another team owns **container orchestration and lifecycle**. You own **what runs inside the execution environment** and **how it talks to the rest of the platform**.
>
> Specifically, we want your design to cover:
>
> 1. **Skills** — How should pre-made scripts and capabilities (data processing, PDF work, charts, scraping, etc.) be structured so agents can **discover** them, **compose** them, and use them **safely** — without a code deploy for every new script an operator adds?
> 2. **Agent ↔ platform boundary** — The agent runs isolated but must read business data, write outputs, call external systems (e.g. messaging, calendars, CRMs), and **stream** updates to users in real time. What is the **contract** at the boundary? What is the agent allowed to do, and how does data get in and out?
> 3. **Quality and regression** — Agents do real work for paying customers. **“Good”** differs by use case (e.g. recruiting vs legal drafting). How would you **know** an agent is good enough, and how would you **catch regressions** after you change prompts, tools, or models?

Again, treat any extra context (tech stack, scale, protocols) as **provided live** if your interviewers choose to share it.

---

## After the design round

You will have a short break, then **Round 3B — live coding** in the chatbot project. Use the README in `round_3b_live_coding/deepflow-interview-chatbot/` for environment setup.

Good luck — think aloud, challenge your own first idea, and enjoy the problem.
