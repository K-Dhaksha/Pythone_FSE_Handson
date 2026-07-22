# Hands-On 2 – SDLC vs TDLC, V-Model & Agile QA Integration

# Task 1: V-Model Mapping

## 1. V-Model Diagram

```
                    REQUIREMENTS
                          │
                          │
              Acceptance Test Planning
                          │
                          ▼
                  SYSTEM DESIGN
                          │
                          │
                System Test Planning
                          │
                          ▼
               ARCHITECTURE DESIGN
                          │
                          │
             Integration Test Planning
                          │
                          ▼
                  MODULE DESIGN
                          │
                          │
                 Unit Test Planning
                          │
                          ▼
                       CODING
                          ▲
                          │
                   UNIT TESTING
                          ▲
                          │
              INTEGRATION TESTING
                          ▲
                          │
                 SYSTEM TESTING
                          ▲
                          │
             ACCEPTANCE TESTING
```

---

# 2. SDLC ↔ TDLC Mapping

| SDLC Phase | Corresponding TDLC Phase | Test Artifact Produced |
|------------|--------------------------|------------------------|
| Requirements Analysis | Acceptance Testing | Acceptance Test Plan |
| System Design | System Testing | System Test Cases |
| Architecture Design | Integration Testing | Integration Test Plan |
| Module Design | Unit Testing | Unit Test Cases |
| Coding | Execution of All Tests | Source Code |

---

# 3. Entry and Exit Criteria

## Unit Testing

### Entry Criteria
- Module development completed
- Unit test cases prepared
- Development environment ready

### Exit Criteria
- All unit tests executed
- All critical defects fixed
- Required code coverage achieved

---

## Integration Testing

### Entry Criteria
- Unit testing completed
- Modules integrated
- Integration test cases prepared

### Exit Criteria
- Interfaces verified
- Critical integration defects resolved
- Integration testing completed successfully

---

## System Testing

### Entry Criteria
- Complete application integrated
- System test cases prepared
- Stable testing environment available

### Exit Criteria
- Functional requirements validated
- No open Critical or High severity defects
- Test execution completed

---

## Acceptance Testing

### Entry Criteria
- System testing completed successfully
- Business requirements satisfied
- Customer ready to validate

### Exit Criteria
- Customer approves application
- Acceptance criteria satisfied
- Product ready for release

---

# 4. QA Engagement During Development

QA should participate before testing actually begins.

### Requirements Review

- Verify requirements are complete.
- Identify ambiguities.
- Ensure requirements are testable.

### Design Review

- Review architecture and system design.
- Identify possible risks.
- Prepare test strategy early.

---

# Task 2 – Agile QA & Shift-Left Testing

## 5. Problems with Waterfall Testing

### Problem 1

Defects are found very late, making them expensive and time-consuming to fix.

---

### Problem 2

Requirement misunderstandings remain unnoticed until the testing phase.

---

### Problem 3

Testing time becomes very limited because development consumes most of the project schedule.

---

# 6. QA Role in Agile Ceremonies

## Sprint Planning

- Review user stories.
- Define acceptance criteria.
- Estimate testing effort.

---

## Daily Standup

- Report testing progress.
- Discuss blockers.
- Coordinate with developers.

---

## Sprint Review

- Validate completed features.
- Demonstrate tested functionality.
- Confirm acceptance criteria.

---

## Sprint Retrospective

- Discuss issues faced during testing.
- Suggest process improvements.
- Identify opportunities for automation.

---

# 7. Shift-Left Practices

## a) Requirement Review

QA reviews requirements before development begins to ensure they are complete and testable.

---

## b) Write Test Cases Before Coding (TDD/BDD)

Prepare test cases and acceptance criteria before implementation starts.

---

## c) Static Code Analysis

Analyze source code using automated tools to identify coding issues without executing the program.

---

## d) API Contract Testing

Verify API request and response formats before integrating different services.

---

# 8. Acceptance Criteria (Given-When-Then)

## Scenario 1 – Successful Course Creation

**Given** the administrator is logged in

**When** valid course details are submitted

**Then** the course is created successfully and a confirmation message is displayed.

---

## Scenario 2 – Duplicate Course Code

**Given** a course already exists with the same course code

**When** the administrator submits another course using that code

**Then** the system displays an appropriate duplicate course error and does not create the course.

---

## Scenario 3 – Missing Required Fields

**Given** the administrator opens the Create Course page

**When** required fields such as Course Code or Course Name are left empty

**Then** validation messages are displayed and the course is not created.