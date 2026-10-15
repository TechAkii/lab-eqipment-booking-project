# Lab Equipment Booking System

## 1. Project Description

The Lab Equipment Booking System is a small web-based system developed to manage the booking of shared laboratory equipment.

The Faculty maintains equipment such as:

- Raspberry Pi kits
- Arduino kits
- Oscilloscopes
- VR headsets
- 3D printing equipment

The current manual booking process can lead to problems such as double bookings, lost booking records, difficulty checking equipment availability, and difficulty managing booking requests.

This system provides a centralized platform for students to request equipment bookings and for laboratory staff to manage equipment and approve or reject booking requests.

The system is developed as a Software Engineering mini project with emphasis on:

- Requirements and task management
- Git and GitHub
- Branches and pull requests
- Peer code review
- Software testing
- Continuous Integration (CI)
- Teamwork and reflection

---

## 2. User Roles

The system contains two user roles:

### Student

Students can:

- Register an account
- Log in
- Log out
- View available laboratory equipment
- Filter equipment by category
- Request equipment bookings
- View the status of their booking requests

### Staff

Staff members can:

- Log in
- Add equipment
- Edit equipment
- Delete equipment
- View equipment
- View booking requests
- Approve booking requests
- Reject booking requests
- Optionally provide a rejection reason

---

## 3. Functional Requirements

The system implements the following five mandatory functional requirements.

### FR-00 — Accounts and Login

Users must be able to:

- Register
- Log in
- Log out

The system supports two roles:

- Student
- Staff

Public registration creates Student accounts only.

Staff accounts are created using a documented setup method such as a seed script or command.

Passwords are not stored as plain text.

Students cannot access staff-only pages.

---

### FR-01 — Equipment Catalogue

Staff can:

- Add equipment
- Edit equipment
- Delete equipment

Each equipment item contains:

- Name
- Category
- Description
- Status

Equipment status can be:

- Available
- Out of service

All logged-in users can view the equipment list.

Users can filter equipment by category.

---

### FR-02 — Request a Booking

A student can request to book an equipment item.

A booking request contains:

- Equipment item
- Booking date
- Start time
- End time

A valid new booking request is initially stored with the status:

**Pending**

---

### FR-03 — Booking Validation

The system rejects invalid booking requests and displays an understandable error message.

The following validation rules are implemented:

1. The end time must be later than the start time.
2. A booking must last at least 30 minutes.
3. A booking must last no more than 4 hours.
4. A booking cannot start in the past.
5. Equipment marked as Out of service cannot be booked.
6. A new booking cannot overlap an existing Pending or Approved booking for the same equipment.

Exact endpoint-to-endpoint bookings are allowed.

For example:

```text
Existing booking: 10:00 ───── 11:00
New booking:                  11:00 ───── 12:00
                              ↑
                              Allowed
```

However:

```text
Existing booking: 10:00 ───── 11:00
New booking:           10:30 ───── 11:30
                       ↑
                       Rejected
```

---

### FR-04 — Booking Approval and Status

Staff can view Pending booking requests.

For each request, staff can:

- Approve
- Reject

Staff may optionally provide a reason when rejecting a booking.

Students can view their own booking requests and their current status.

Possible booking statuses are:

- Pending
- Approved
- Rejected

---

## 4. Team Members

| Member | Name | GitHub Profile |
|---|---|---|
| Member 1 | Akila Thikshana | https://github.com/TechAkii |
| Member 2 | Kalana | https://github.com/chirankalana2002 |
| Member 3 | G.H.B.A. Achintha | https://github.com/bhanukaachil |
| Member 4 | Devindu | https://github.com/devindudilshan2003|
| Member 5 | T.A.W.Anupama | https://github.com/anuwasitha |

---

## 5. Module Allocation

The project responsibilities are divided into five modules.

| Module | Main Responsibility | Assigned Member |
|---|---|---|
| M1 | Accounts and Authentication | Kalana |
| M2 | Equipment Catalogue | G.H.B.A. Achintha|
| M3 | Booking Form and Booking Model | Devindu |
| M4 | Booking Validation and Tests | Akila Thikshana |
| M5 | Approval, Integration and CI | Akila Thikshana |

### M1 — Accounts and Authentication (Kalana)

Responsible for:

- Registration
- Login
- Logout
- Password handling
- Student and Staff roles
- Authentication and authorization

### M2 — Equipment Catalogue (G.H.B.A. Achintha)

Responsible for:

- Equipment model
- Equipment catalogue
- Add equipment
- Edit equipment
- Delete equipment
- Equipment status
- Category filtering

### M3 — Booking Form and Booking Model (Devindu)

Responsible for:

- Booking model
- Booking form
- Equipment selection
- Booking date
- Start time
- End time
- Creating booking requests

### M4 — Booking Validation and Tests (Akila Thikshana)

Responsible for:

- Booking validation
- Duration validation
- Past-booking validation
- Equipment status validation
- Overlap detection
- Boundary-value testing
- Automated tests

### M5 — Approval, Integration and CI (Akila Thikshana)

Responsible for:

- Staff approval functionality
- Booking rejection
- Booking status
- Module integration
- GitHub Actions CI
- Final system integration

---

## 6. Coordination Roles

| Role | Assigned Member |
|---|---|
| Coordinator | Akila Thikshana |
| QA Lead | Akila Thikshana |
| Review Lead | G.H.B.A. Achintha |
| GitHub/CI Lead | Devindu |

### Coordinator

Responsible for:

- Organizing GitHub Issues
- Maintaining the Project Board
- Coordinating team activities
- Monitoring project progress

### QA Lead

Responsible for:

- Coordinating testing
- Test planning
- Maintaining `TESTING.md`
- Monitoring automated tests
- Checking validation requirements

### Review Lead

Responsible for:

- Coordinating peer code reviews
- Ensuring pull requests are reviewed
- Ensuring review requirements are followed

### GitHub/CI Lead

Responsible for:

- Repository setup
- GitHub workflow support
- GitHub Actions CI
- Supporting CI troubleshooting

---

## 7. Technology Requirements

The project uses the technologies required by the assignment.

| Area | Technology |
|---|---|
| Programming Language | Python 3.11+ |
| Web Framework | Flask |
| Database | SQLite |
| ORM | Flask-SQLAlchemy |
| Front End | Jinja2, HTML, CSS |
| CSS Framework | Bootstrap (Optional) |
| Authentication | Flask-Login or Flask-based implementation |
| Testing | pytest |
| Coverage | pytest-cov |
| Linting | Ruff |
| Version Control | Git |
| Repository | GitHub |
| Continuous Integration | GitHub Actions |

---

## 8. Software Requirements

The following software is required to run the project:

- Python 3.11 or newer
- Git
- A modern web browser
- GitHub account

Check the Python version:

```bash
python --version
```

Check the Git version:

```bash
git --version
```

---

## 9. Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/TechAkii/lab-eqipment-booking-project
```

Navigate to the project directory:

```bash
cd lab-eqipment-booking-project
```

---

### Step 2 — Create a Virtual Environment

#### Windows

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

---

### Step 3 — Install Dependencies

After activating the virtual environment:

```bash
pip install -r requirements.txt
```

---

## 10. Database Setup

The project uses SQLite as its database.

The database setup and initialization instructions will be maintained as part of the project implementation.

Staff accounts must be created using the documented seed/setup method provided by the project.

---

## 11. Running the Application

Activate the virtual environment first.

Then run:

```bash
python run.py
```

The Flask development server will start.

Open the local address shown in the terminal, normally:

```text
http://127.0.0.1:5000
```

The system is intended to run locally. Internet deployment is not required.

---

## 12. Running Automated Tests

The project uses `pytest` for automated testing.

Run all tests:

```bash
pytest
```

Run tests with detailed output:

```bash
pytest -v
```

---

## 13. Test Coverage

Test coverage is measured using `pytest-cov`.

Run:

```bash
pytest --cov=app --cov-report=term-missing
```

The final project aims for at least:

```text
40% line coverage
```

Coverage percentage alone is not considered sufficient. Test quality and coverage of important business rules are also considered.

---

## 14. Code Quality

The project uses Ruff for linting.

Run:

```bash
ruff check .
```

---

## 15. GitHub Workflow

The project follows the required Software Engineering workflow:

```text
Issue
  ↓
Branch
  ↓
Implementation
  ↓
Test
  ↓
Pull Request
  ↓
Peer Review
  ↓
CI
  ↓
Merge
```

Team members should not normally develop features directly on the `main` branch.

---

## 16. GitHub Issues and Project Board

GitHub Issues are used as the project backlog.

Major requirements are represented using Issues such as:

- FR-00 — Accounts and Login
- FR-01 — Equipment Catalogue
- FR-02 — Request a Booking
- FR-03 — Booking Validation
- FR-04 — Booking Approval and Status

The GitHub Project Board contains the following columns:

```text
Backlog
To do
In progress
In review
Done
```

The board represents the current state of project tasks.

---

## 17. Branch Naming

Feature and task branches use descriptive names.

Examples:

```text
feature/FR-01-equipment
feature/FR-02-booking
fix/FR-03-overlap
test/FR-03-boundaries
```

---

## 18. Commit Messages

Commit messages should clearly describe the change.

Examples:

```text
Add equipment model
Implement booking form
Add overlap validation tests
Fix staff role check
```

Where practical, commits and pull requests should reference the related GitHub Issue.

---

## 19. Pull Requests and Code Review

Each team member participates in peer code review.

A student must not approve their own pull request.

Each student must have at least one meaningful pull request reviewed by another group member before the final evaluation.

The project uses:

```text
REVIEW_CHECKLIST.md
```

for code reviews.

The review checklist covers:

- User input validation
- Business rules
- Database operations
- Login and role restrictions
- Error handling
- Secret values
- Relevant automated tests
- Existing test results

---

## 20. Continuous Integration

The project uses GitHub Actions for Continuous Integration.

The CI workflow is located at:

```text
.github/workflows/ci.yml
```

The CI workflow runs when:

- Code is pushed
- A pull request is created or updated

The CI pipeline performs:

1. Dependency installation
2. Ruff checks
3. pytest execution
4. Coverage reporting

The final `main` branch should have passing CI.

---

## 21. Project Documentation

The main project documentation files are:

```text
README.md
TESTING.md
REVIEW_CHECKLIST.md
RETROSPECTIVE.md
```

### README.md

Contains:

- Project description
- Group members
- GitHub usernames
- Module allocation
- Coordination roles
- Software requirements
- Installation instructions
- Application running instructions
- Test instructions

### TESTING.md

Contains the project's:

- Test strategy
- Test cases
- Equivalence Partitioning
- Boundary Value Analysis
- Test results
- Coverage information

### REVIEW_CHECKLIST.md

Contains the checklist used during peer code reviews.

### RETROSPECTIVE.md

Contains the team's final reflection, including:

- What went well
- Difficulties encountered
- What could be improved
- Number of Issues completed
- Number of pull requests merged
- Number of peer reviews performed
- Final test coverage

---

## 22. Security

The repository must not contain confidential credentials.

The following must not be committed:

- Passwords
- API keys
- Secret keys
- Private credentials
- Database files containing test or user data

Use `.gitignore` and environment variables where appropriate.

---

## 23. Final Deliverables

By the final evaluation, the repository should contain:

- Working source code on `main`
- Final Git tag `v1.0`
- `README.md`
- `TESTING.md`
- `REVIEW_CHECKLIST.md`
- `RETROSPECTIVE.md`
- `.github/workflows/ci.yml`
- Automated pytest tests
- Current GitHub Issues
- Updated GitHub Projects board
- Evidence of branches
- Evidence of pull requests
- Evidence of peer reviews

No separate written report is required.

---

## 24. Project Status

**Status:** In Development

The project is being developed using the required Software Engineering workflow:

```text
Requirement
    ↓
Issue
    ↓
Branch
    ↓
Implementation
    ↓
Test
    ↓
Pull Request
    ↓
Peer Review
    ↓
CI
    ↓
Merge
```

---

## 25. Repository

GitHub Repository:

https://github.com/TechAkii/lab-eqipment-booking-project

---
