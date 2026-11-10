# Lab: trace the loop

An agent from scratch: a course registration assistant with no agent framework and no SDK.
The model is one HTTP POST, each tool is one file, and the loop is one short function.

| Section | When | What you do |
|---|---|---|
| **1 · FOLLOW THE AGENT** | during the lecture | run each step as the lecture reaches it, with the code open |
| **2 · THE TOOL AGENT** | lab | one tool call and its answer: where it works, and where it stops short |
| **3 · THE LOOP** | lab | the full agent: measure it, and move a rule |

## Setup

```bash
cp .env.example .env            # paste your Gemini key
uv sync
```

## Where everything is

```
main_1_ask.py ... main_9_memory.py    Section 1: one program, growing
reset.py                forget everything Main 9 saved
ask.py                  the finished agent on any request you type
run_suite.py            the trajectory suite
src/agent/loop.py       the finished loop
src/agent/model.py      one HTTP POST: the wire format
src/agent/messages.py   building and reading the conversation
src/agent/prompt.py     the instructions
src/agent/trace.py      one record per turn
src/agent/memory.py     prompt memory: notes in a file, put into the instructions
src/tools/              ONE TOOL PER FILE
src/tools/registry.py   a function becomes a declaration
src/tools/dispatch.py   the boundary: validate, then run
src/tools/session.py    who is asking
```

## Section 1 · Follow the agent

One program, nine versions. Each main is complete and adds to the one before it. Run each
when the lecture reaches it, and compare it with the last, for example
`diff main_3_invoke.py main_4_answer.py`.

| Main | Command | What it adds |
|---|---|---|
| 1 | `uv run main_1_ask.py` | ask the model: text comes back, nothing happens |
| 2 | `uv run main_2_register.py` | the tool declarations: a call is named, nothing runs |
| 3 | `uv run main_3_invoke.py` | run the tools that were named |
| 4 | `uv run main_4_answer.py` | send the results back and get an answer |
| 5 | `uv run main_5_loop.py` | repeat until a turn names no tool: the agent |
| 6 | `uv run main_6_boundary.py` | validate every call before it runs |
| 7 | `uv run main_7_trace.py` | record every turn; the loop moves to `src/agent/loop.py` |
| 8 | `uv run main_8_conversation.py` | keep the conversation when the loop ends |
| 9 | `uv run main_9_memory.py` | remember across conversations: a `remember` tool, and notes put into the instructions |

Mains 1 to 7 take your own request as an argument:
`uv run main_4_answer.py "Register me for two 3000-level CS courses."`
Mains 8 and 9 are conversations: type a request, and a blank line to quit.

Main 9 is the only program that keeps anything between runs: its notes, in `data/memory/`.
Run it twice. In the first, tell it a preference and ask it to remember. In the second, ask
for a course and watch the note in the instructions shape the answer. To start over:
`uv run reset.py`.

## Section 2 · The tool agent

Stop the agent after two turns: one to name the tools, one to answer from the results.
Predict what each request does before you run it.

```bash
uv run ask.py "What are the prerequisites for CS3300?" --max-steps 2
uv run ask.py "How many seats are left in CS2100 and CS2200?" --max-steps 2
uv run ask.py "Show me CS courses at the 3000 level." --max-steps 2
uv run ask.py "Help me register for 3 CS courses next semester that fit my schedule and satisfy my prereqs." --max-steps 2
```

1. Which requests finish? What do they have in common?
2. On the last request, what was found and what was enrolled? What would the next call have needed?
3. **Add a tool.** Create `src/tools/drop_course.py` and add it to `src/tools/__init__.py`.
   Run `uv run ask.py "Drop ENGL1010."`.
4. **Change a description.** Make the description in `src/tools/check_prereqs.py` vague and
   re-run a request that uses it. What changed in the calls?

## Section 3 · The loop

```bash
uv run ask.py "Help me register for 3 CS courses next semester that fit my schedule and satisfy my prereqs."
```

1. In the output, how many tokens did each turn add?
2. Read `data/suite/tasks.jsonl`. Success is read from the enrollment table. Run the
   recording, which needs no key, then live:

   ```bash
   uv run run_suite.py --replay
   uv run run_suite.py --runs 5
   ```

   Report success per slice with its interval, and the median and maximum steps.
3. **Move the rule.** The instruction stays; the check in `enroll` goes:

   ```bash
   uv run run_suite.py --runs 5 --slice blocked --no-enforce
   ```

   How many forbidden enrollments happened, and what is the interval on that rate? The report
   names the tasks that failed. Watch one of those requests turn by turn, with
   `ask.py "<the request>" --no-enforce` and then without the flag.

## Keep

The two blocked-slice results with their intervals, the tokens added per turn in one run,
and one forbidden enrollment's turns with a sentence on where the check would have run.
