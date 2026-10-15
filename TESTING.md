# Testing Guide — Lab Equipment Booking System

## 1. Purpose

This document explains how to set up the Lab Equipment Booking System, run the application locally, execute automated tests, and check code quality.

## 2. Prerequisites

Ensure the following software is installed:

- Python 3
- Git
- Visual Studio Code or another code editor

The project uses Flask, SQLite, pytest, pytest-cov, and Ruff.

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

If PowerShell blocks activation, use the activation method permitted by your system's execution policy, or run the commands using the virtual environment's Python executable directly.

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

`http://127.0.0.1:5000/`

Check that the application loads and that its main navigation works.

## 5. Run Automated Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

The command displays each test and whether it passed or failed.

To run the authentication tests only:

```powershell
python -m pytest tests/test_auth.py -v
```

To run the smoke tests only:

```powershell
python -m pytest tests/test_smoke.py -v
```

### Test Result Recording

After executing the tests, record the actual result below:

- Test command: `python -m pytest -v`
- Date tested: [Enter the date]
- Result: [Enter the actual passed/failed summary]
- Notes: [Record any failures and their resolutions]

Do not record a successful result unless the tests have completed successfully.

## 6. Check Code Quality with Ruff

Check the project for linting issues:

```powershell
ruff check .
```

If Ruff reports errors, review and fix them before committing the changes.

Run the command again to verify the fixes.

## 7. Test Authentication

Manually verify the following scenarios:

1. Register a student account with valid details.
2. Confirm that a password mismatch is rejected.
3. Attempt to register with an email address that is already registered.
4. Log in with valid credentials.
5. Attempt to log in with an incorrect password.
6. Log out and verify the expected behaviour.

Also confirm that passwords are stored as password hashes rather than as plain text.

Record the actual outcome of each scenario during testing.

## 8. Test Equipment Booking

Where the relevant functionality is available, verify these scenarios:

1. View the equipment catalogue.
2. Attempt to book available equipment using valid booking details.
3. Attempt to submit invalid booking details, such as an end time before the start time.
4. Check that overlapping bookings are handled according to the application's validation rules.
5. Check that a user's bookings appear on the My Bookings page.
6. If staff approval functionality is enabled, test approving and rejecting a booking.

Record any unavailable or failing functionality rather than marking it as passed.

## 9. Continuous Integration (CI)

The project uses a GitHub Actions workflow to automate quality checks.

To verify CI:

1. Open the project's GitHub repository.
2. Select the **Actions** tab.
3. Open the latest workflow run.
4. Check whether the Ruff and pytest steps completed successfully.
5. Record the workflow result and retain a screenshot for assessment evidence.

The local test results and GitHub Actions results should be checked separately.

## 10. Reporting Problems

For each failure, record:

- The test or feature that failed.
- The steps required to reproduce the problem.
- The expected behaviour.
- The actual behaviour.
- Any error message.
- The fix applied, if resolved.
- The result after retesting.

## 11. Testing Summary

Complete this section after testing:

| Check | Actual result |
|---|---|
| Application starts successfully | [Passed] |
| Automated pytest suite | [7 passed] |
| Ruff code-quality check | [Passed] |
| Authentication scenarios | [Passed] |
| Equipment booking scenarios | [Passed] |
| GitHub Actions CI workflow | [Passed] |

