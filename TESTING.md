# Testing Guide — Lab Equipment Booking System

## 1. Purpose

This document explains how to set up the Lab Equipment Booking System, run the application locally, execute automated tests, verify booking validation rules, and check code quality.

It also documents the initial FR-03 test design, manual testing procedures, Continuous Integration (CI), and the process for reporting defects.

## 2. Prerequisites

Ensure the following software is installed:

- Python 3
- Git
- Visual Studio Code or another code editor

The project uses Flask, SQLite, Flask-SQLAlchemy, Flask-Login, pytest, pytest-cov, and Ruff.

## 3. Set Up the Project

Open PowerShell in the project root directory.

### Step 1: Create a virtual environment

If a virtual environment does not already exist, run:

```powershell
python -m venv venv
```

### Step 2: Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use an activation method permitted by your system's execution policy, or run commands using the virtual environment's Python executable directly.

### Step 3: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## 4. Run the Application

Start the application using:

```powershell
python run.py
```

Open the local URL displayed in the terminal, typically:

http://127.0.0.1:5000/

Check that the application starts successfully and that its main navigation works.

Verify that the relevant pages load correctly, including the equipment catalogue, authentication pages, booking pages, and staff or admin pages.

## 5. Run Automated Tests

### 5.1 Run the complete test suite

Execute:

```powershell
python -m pytest -v
```

This command runs the automated tests and displays individual test results.

### 5.2 Run authentication tests

```powershell
python -m pytest tests/test_auth.py -v
```

### 5.3 Run smoke tests

```powershell
python -m pytest tests/test_smoke.py -v
```

### 5.4 Run tests with coverage

```powershell
python -m pytest --cov=app --cov-report=term-missing
```

Coverage results identify which application code was exercised by the tests. Coverage percentage alone does not guarantee that all requirements are tested.

### 5.5 Test result recording

After running the tests, record the actual results:

- Test command: `python -m pytest -v`
- Date tested: [Enter the actual test date]
- Total tests: [Enter actual count]
- Passed: [Enter actual count]
- Failed: [Enter actual count]
- Skipped: [Enter actual count, if applicable]

Record any failures and their resolutions. Do not record a successful result unless the tests have completed successfully.

## 6. Check Code Quality with Ruff

Run the following command to check for linting issues:

```powershell
ruff check .
```

Review any reported issues and correct them where appropriate.

Run the command again to verify the result.

Record the actual result:

- Command: `ruff check .`
- Result: [Enter actual result]
- Issues found: [Enter actual result]
- Issues resolved: [Enter actual result]

## 7. Test Authentication and User Management (FR-00)

The purpose of these tests is to verify account creation, login, logout, password handling, and role-based access.

Perform the following manual checks where applicable:

| Test ID | Scenario | Expected Result |
|---|---|---|
| FR00-T01 | Register a Student using valid details | Account is created successfully |
| FR00-T02 | Submit registration with missing required fields | Registration is rejected |
| FR00-T03 | Submit mismatched password confirmation | Registration is rejected |
| FR00-T04 | Submit a password shorter than the minimum length | Registration is rejected |
| FR00-T05 | Register using an existing username or email | Duplicate registration is rejected |
| FR00-T06 | Log in using valid credentials | User is authenticated |
| FR00-T07 | Log in using an incorrect password | Login is rejected |
| FR00-T08 | Log out of an authenticated session | User is logged out |
| FR00-T09 | Attempt to access a restricted page without the required role | Access is denied or redirected |
| FR00-T10 | Inspect stored password values | Passwords are stored as hashes, not plain text |

Admin and Staff account creation should also be checked using the account-management process implemented in the application.

Record the actual result of each scenario during testing.

## 8. Test Equipment Catalogue (FR-01)

The purpose of these tests is to verify equipment browsing, category filtering, equipment availability, and management functionality.

| Test ID | Scenario | Expected Result |
|---|---|---|
| FR01-T01 | Open the equipment catalogue | Equipment entries are displayed |
| FR01-T02 | Filter equipment by category | Matching equipment is displayed |
| FR01-T03 | Search or browse equipment, where supported | Relevant equipment is displayed |
| FR01-T04 | Staff adds equipment | Equipment is saved and displayed |
| FR01-T05 | Staff edits equipment | Updated information is displayed |
| FR01-T06 | Staff deletes equipment, where permitted | Equipment is removed according to the application's rules |
| FR01-T07 | Mark equipment as unavailable | The equipment status is updated and unavailable equipment cannot be booked |

For each test, record the actual result and any issues encountered.

## 9. Test Booking Requests (FR-02)

The purpose of these tests is to verify that Students can submit booking requests and view their booking records.

| Test ID | Scenario | Expected Result |
|---|---|---|
| FR02-T01 | Submit a booking request with valid details | Booking request is created |
| FR02-T02 | Open the My Bookings page | The authenticated Student's bookings are displayed |
| FR02-T03 | View the status of a booking | The correct booking status is displayed |
| FR02-T04 | Submit a request with missing or invalid details | The request is rejected with appropriate feedback |
| FR02-T05 | Attempt to access another user's booking data | Access is restricted according to the application's authorization rules |

Record the actual result of each scenario.

## 10. Initial FR-03 Test Design — Booking Validation

### 10.1 Objective

FR-03 focuses on validating equipment booking requests to prevent invalid durations, past booking times, overlapping bookings, and bookings for unavailable equipment.

The following test cases define the initial test design. Each case should be checked against the project requirements and the implemented validation rules.

### 10.2 Test cases

| Test ID | Test Scenario | Test Input / Condition | Expected Result |
|---|---|---|---|
| FR03-T01 | Minimum permitted duration | Booking duration is exactly 30 minutes | Booking is accepted if all other rules pass |
| FR03-T02 | Maximum permitted duration | Booking duration is exactly 4 hours | Booking is accepted if all other rules pass |
| FR03-T03 | Duration below minimum | Booking duration is less than 30 minutes | Booking is rejected |
| FR03-T04 | Duration above maximum | Booking duration exceeds 4 hours | Booking is rejected |
| FR03-T05 | Booking starts in the past | Start date or time is earlier than the permitted current time | Booking is rejected |
| FR03-T06 | Overlapping booking | Requested interval overlaps an existing Pending or Approved booking for the same equipment | Booking is rejected |
| FR03-T07 | Unavailable equipment | Requested equipment is marked unavailable or out of service | Booking is rejected |
| FR03-T08 | Valid non-overlapping booking | Requested interval does not conflict with a blocking booking | Booking may be accepted if all other rules pass |

### 10.3 Test design and execution status

The initial test design defines the scenarios and expected results before or during implementation.

For each test case, record:

- Whether the validation rule has been implemented.
- Whether an automated test exists.
- The actual execution result.
- Any defect identified.
- The corrective action and retest result, if applicable.

Use the following table to track progress:

| Test ID | Automated Test Implemented? | Execution Result |
|---|---|---|
| FR03-T01 | [Yes/No] | [Pass/Fail/Not run] |
| FR03-T02 | [Yes/No] | [Pass/Fail/Not run] |
| FR03-T03 | [Yes/No] | [Pass/Fail/Not run] |
| FR03-T04 | [Yes/No] | [Pass/Fail/Not run] |
| FR03-T05 | [Yes/No] | [Pass/Fail/Not run] |
| FR03-T06 | [Yes/No] | [Pass/Fail/Not run] |
| FR03-T07 | [Yes/No] | [Pass/Fail/Not run] |
| FR03-T08 | [Yes/No] | [Pass/Fail/Not run] |

These status fields must be completed using the actual test implementation and execution results.

## 11. Test Staff Booking Approval (FR-04)

The purpose of these tests is to verify that Staff can review booking requests and that booking statuses are updated correctly.

| Test ID | Scenario | Expected Result |
|---|---|---|
| FR04-T01 | Staff views pending booking requests | Pending requests are displayed |
| FR04-T02 | Staff approves a pending booking | Booking status changes to Approved |
| FR04-T03 | Staff rejects a pending booking | Booking status changes to Rejected |
| FR04-T04 | Student views an updated booking | The latest status is displayed |
| FR04-T05 | Unauthorized user attempts to approve or reject a booking | The operation is denied |
| FR04-T06 | Attempt to approve or reject an already processed booking | The operation is rejected according to the application's rules |

Record the actual result of each scenario.

## 12. Continuous Integration (CI)

The project uses GitHub Actions to automate configured quality checks.

To verify CI:

1. Open the project's GitHub repository.
2. Select the **Actions** tab.
3. Open the relevant workflow run.
4. Check the status of the pytest and Ruff steps, where configured.
5. Open the associated pull request, if applicable.
6. Record the result and retain a screenshot as assessment evidence.

Local test results and GitHub Actions results should be checked separately.

Record:

- Workflow name: [Enter actual workflow name]
- Branch or pull request: [Enter branch or PR]
- Run date: [Enter actual date]
- Result: [Passed/Failed/Cancelled]
- Failed steps and corrective actions: [If applicable]

## 13. Pull Request and Code Review Testing Evidence

Code changes should be reviewed through the project's pull request workflow.

For assessment evidence, verify and record:

- Pull request title and linked issue.
- Source branch and target branch.
- Files changed.
- Reviewer comments and review status.
- CI check results.
- Any corrections made in response to review feedback.

Only describe a pull request as peer-reviewed or approved when the GitHub review record confirms that status.

## 14. GitHub Issues and Project Board

Use GitHub Issues and the project board to track testing and implementation work.

Verify that:

- Issues accurately describe the work to be completed.
- Issue statuses reflect actual progress.
- Testing tasks are linked to relevant code changes or pull requests where possible.
- Completed tasks have supporting evidence.
- Outstanding tasks remain marked as incomplete or in progress.

## 15. Reporting Problems

For each failure or defect, record:

- Test ID or affected feature.
- Steps required to reproduce the problem.
- Expected behaviour.
- Actual behaviour.
- Error message, if available.
- Corrective action taken.
- Retest result.

Retest affected functionality after applying a fix.

## 16. Testing Summary

Complete this summary using verified results.

| Check | Actual Result |
|---|---|
| Application starts successfully | [Enter result] |
| Automated pytest suite | [Enter actual counts and result] |
| Coverage report | [Enter actual percentage, if measured] |
| Ruff code-quality check | [Enter actual result] |
| Authentication tests | [Enter actual result] |
| Equipment catalogue tests | [Enter actual result] |
| Booking request tests | [Enter actual result] |
| FR-03 booking validation tests | [Enter actual result] |
| Staff approval tests | [Enter actual result] |
| GitHub Actions CI workflow | [Enter actual result] |
| Pull request review evidence | [Enter actual status] |

The testing summary should reflect the latest verified results rather than assumed outcomes.

## 17. Limitations and Future Testing

Record any scenarios that are not yet automated, any known defects, and any test cases that require additional verification.

Future testing activities should prioritize untested validation rules, regression testing after code changes, access-control checks, and maintaining reliable separation between the test database and the application's local database.

---

**End of Testing Guide**