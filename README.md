# Smart Exam Scheduler

A capstone project prototype that generates an exam timetable using **Graph Coloring with Backtracking**.

## Features
- Add subjects and student enrollments.
- Build a conflict graph from shared student enrollments.
- Assign exam slots using a Backtracking graph-coloring algorithm.
- Display the generated timetable.
- Download the timetable as CSV.
- Show the number of assignment attempts made by the search.

## How it works
- Each subject is a vertex.
- An edge connects two subjects if at least one student is enrolled in both.
- Each color represents an exam slot.
- Adjacent vertices cannot receive the same color.

## Setup

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
streamlit run app.py
```

## Project structure

```text
Smart-Exam-Scheduler/
├── app.py
├── graph_coloring.py
├── data.py
├── requirements.txt
├── README.md
└── assets/
```

## Notes
This is an educational prototype. Real exam scheduling may also need room capacity, exam duration, faculty availability, holidays, and institution-specific rules.
