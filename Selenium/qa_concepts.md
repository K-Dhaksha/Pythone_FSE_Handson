# Hands-On 1 – QA Concepts, Functional Testing & Defect Lifecycle

# Task 1: Map Testing Types to a Real System

## 1. Testing Types

### Unit Testing
**Description:**
Verify that the function responsible for validating course details works correctly.

**Example Test Case:**
Input a valid course object into the validation function and verify it returns success.

**Classification:** Functional Testing

---

### Integration Testing
**Description:**
Verify that the POST /api/courses endpoint correctly stores course information in the database.

**Example Test Case:**
Send a valid POST request and verify that the database contains the new course record.

**Classification:** Functional Testing

---

### System Testing
**Description:**
Test the complete flow from sending an API request until the data is stored and retrieved.

**Example Test Case:**
Create a course using POST /api/courses, retrieve it using GET /api/courses, and verify the details match.

**Classification:** Functional Testing

---

### User Acceptance Testing (UAT)
**Description:**
Verify that a college administrator can successfully create a new course.

**Example Test Case:**
Login as an administrator, create a new course, and confirm it appears in the course list.

**Classification:** Functional Testing

---

## Non-Functional Testing Example

### Performance Testing

Verify that the Course Management API responds within 2 seconds when 500 users access it simultaneously.

Classification: Non-Functional Testing

---

## 2. Black-Box vs White-Box Testing

### Black-Box Testing
Black-box testing verifies the application's functionality without knowing the internal implementation or source code. The tester only checks inputs and outputs.

Typically performed by:
- QA Engineers
- Testers

---

### White-Box Testing

White-box testing verifies the internal code, logic, branches, and algorithms of the application.

Typically performed by:
- Developers

---

## 3. Formal Test Cases

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|--------------|-------------|---------------|------------|-----------------|---------------|-----------|
| TC001 | Create course with valid data | API server is running | Send POST request with valid course details | HTTP 201 Created and course stored successfully | | |
| TC002 | Create course with missing course code | API server is running | Send POST request without course code | HTTP 400 Bad Request with validation message | | |
| TC003 | Create duplicate course | Course already exists | Send POST request using an existing course code | Duplicate course error message displayed | | |

---

# Task 2: Defect Lifecycle & Severity Classification

## 4. Defect Lifecycle

New
↓
Assigned
↓
Open
↓
Fixed
↓
Retest
↓
Verified
↓
Closed

### Rejected
If the reported issue is not a valid defect or cannot be reproduced, it is marked as Rejected.

### Deferred
If fixing the defect is postponed to a future release because of low business impact or time constraints, it is marked as Deferred.

---

## 5. Severity and Priority Classification

### a) POST /api/courses returns 500 Internal Server Error

Severity: Critical

Priority: P1

Justification:
The API cannot perform its primary function, affecting all users immediately.

---

### b) Course names longer than 150 characters are silently truncated

Severity: Medium

Priority: P2

Justification:
The application works but causes data loss.

---

### c) Typo on the Swagger documentation page

Severity: Low

Priority: P4

Justification:
Only affects documentation and does not impact functionality.

---

### d) Login occasionally returns 401 with valid credentials

Severity: High

Priority: P1

Justification:
Intermittent authentication failures seriously affect users and indicate system instability.

---

## 6. Defect Report

**Defect ID:** BUG-001

**Title:**
POST /api/courses returns 500 Internal Server Error

**Environment:**
Windows 11
Python 3.12
Chrome Browser
Course Management API

**Build Version:**
v1.0

**Severity:**
Critical

**Priority:**
P1

**Steps to Reproduce:**

1. Start the Course Management API.
2. Open Postman.
3. Send a POST request to /api/courses with valid course details.
4. Observe the response.

**Expected Result:**

The API should return HTTP 201 Created and store the course successfully.

**Actual Result:**

The API returns HTTP 500 Internal Server Error.

**Attachments:**

Screenshot of 500 error

---

## 7. Difference Between Severity and Priority

### Severity
Severity refers to how much the defect affects the system's functionality.

### Priority
Priority refers to how urgently the defect should be fixed.

### Example

A spelling mistake on the CEO's dashboard has:

Severity: Low

Priority: High

Reason:
The application functions correctly, but because the CEO will see the error during an important presentation, it must be fixed immediately.