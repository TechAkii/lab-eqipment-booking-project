# Code Review Checklist — Lab Equipment Booking System

## Purpose

This checklist provides a consistent method for reviewing proposed code changes before they are merged into the main branch.

## 1. General Review

- [ ] The change addresses the intended issue or requirement.
- [ ] The implementation is consistent with the existing project structure.
- [ ] Variable, function, class, and file names are clear and meaningful.
- [ ] The code is readable and avoids unnecessary duplication.
- [ ] No unrelated files or changes are included.

## 2. Functional Correctness

- [ ] The implementation meets the expected requirements.
- [ ] Normal user scenarios have been considered.
- [ ] Invalid inputs and error cases are handled appropriately.
- [ ] Relevant database operations behave as expected.
- [ ] Existing functionality has not been unintentionally broken.

## 3. Security and Access Control

- [ ] User passwords are hashed before storage.
- [ ] Authentication is required for protected pages.
- [ ] Student and staff permissions are checked where applicable.
- [ ] Users cannot access or modify other users' restricted information without authorization.
- [ ] Sensitive information and credentials are not committed to the repository.

## 4. Database and Booking Validation

- [ ] Database models and relationships are used correctly.
- [ ] Required booking fields are validated.
- [ ] Invalid booking dates and times are rejected.
- [ ] Booking conflicts are checked where applicable.
- [ ] Database changes are handled consistently.

## 5. Testing and Code Quality

- [ ] Relevant automated tests have been added or updated.
- [ ] The relevant tests pass locally.
- [ ] `python -m pytest -v` has been executed.
- [ ] `ruff check .` has been executed.
- [ ] New failures and warnings have been investigated.
- [ ] Manual testing has been performed where automated tests are insufficient.

## 6. User Interface

- [ ] Templates render without errors.
- [ ] Navigation and links work as expected.
- [ ] Forms provide understandable validation or feedback.
- [ ] Success and failure messages are appropriate.
- [ ] Pages remain usable at the intended screen sizes.

## 7. Git and Pull Request Review

- [ ] The change is on the appropriate feature or fix branch.
- [ ] The commit messages describe the changes clearly.
- [ ] The pull request explains the purpose of the change.
- [ ] The pull request is linked to the relevant issue when applicable.
- [ ] CI checks have been reviewed.
- [ ] Review feedback has been addressed.
- [ ] The change is merged only after the required checks and review are complete.

## 8. Review Record and Follow-up Actions

### Pull Request #13 — Feature/authentication tests

- **Pull Request:** #13
- **Purpose:** Introduce automated authentication tests.
- **Status:** Merged
- **Review comments:** To be verified in the pull request conversation.
- **CI results:** To be verified in the pull request checks.

### Additional Pull Requests

| Pull Request | Purpose | Status |
|---|---|---|
| #11 | Project architecture and testing foundation | Merged |
| #12 | Configure GitHub Actions CI triggers | Merged |

### Outstanding Review Actions

- [ ] Review the pull request conversation and record any feedback.
- [ ] Verify that the required CI checks completed successfully.
- [ ] Confirm that the relevant automated tests passed.
- [ ] Record any changes requested and how they were addressed.
- [ ] Complete the review record for future pull requests.

### Review Sign-off

- **Reviewer:** To be recorded when the review is completed.
- **Review date:** To be recorded.
- **Final review decision:** Pending verification.
- **Additional comments:** To be recorded if applicable.
