# Hands-On 3 – Test Automation Process, Lifecycle & Framework Types

# Task 1: Automation Decision and Test Case Selection

## 1. Criteria for Deciding Whether a Test Case Should Be Automated

### 1. Repetitive Execution
Tests that are executed frequently are ideal for automation because they save time and effort.

**Application to Scenario:**
The POST /api/courses endpoint is tested after every code change, making it a good automation candidate.

---

### 2. Stable Functionality
Features that do not change often are easier to automate and require less maintenance.

**Application to Scenario:**
The API endpoint remains consistent, so automation is suitable.

---

### 3. Regression Testing
Regression tests ensure existing functionality continues to work after updates.

**Application to Scenario:**
The POST endpoint should be included in every regression suite.

---

### 4. Data-Driven Testing
Tests requiring multiple combinations of inputs benefit greatly from automation.

**Application to Scenario:**
Different course names, codes, and departments can be tested automatically.

---

### 5. High Business Impact
Critical functionalities should always be automated to reduce business risk.

**Application to Scenario:**
Creating courses is a core business feature, making it a high-priority automation candidate.

---

# 2. Automate or Manual?

| Test Case | Decision | Justification |
|-----------|----------|---------------|
| a) Regression test for all CRUD endpoints | **Automate** | Executed frequently after every code change. |
| b) Exploratory testing of a new search feature | **Manual** | Requires human observation and creativity. |
| c) Performance test with 100 concurrent users | **Automate** | Performance testing is best performed using automation tools. |
| d) UI test for the login form | **Automate** | Login is a stable and frequently tested feature. |
| e) Verify Swagger documentation | **Manual** | Documentation changes infrequently and needs human review. |
| f) Smoke test after deployment | **Automate** | Smoke tests are executed after every deployment. |

---

# 3. Test Automation ROI

**Definition**

Return on Investment (ROI) measures whether the time and effort spent creating automated tests are recovered through repeated execution.

---

### Given

Automation Development Time = **4 hours**

Manual Execution Time = **30 minutes (0.5 hour)**

Maintenance Overhead = **20% after the 10th run**

---

### ROI Calculation

Initial automation effort:

4 hours

Each manual execution saved:

0.5 hour

Runs required before automation pays off:

4 ÷ 0.5 = **8 runs**

Since maintenance starts only after the 10th run, automation reaches ROI before maintenance costs begin.

**Answer: Automation becomes beneficial after approximately 8 executions.**

---

# 4. Flaky Tests

## Definition

A flaky test is a test that sometimes passes and sometimes fails even though the application has not changed.

---

## Example

A Selenium test clicks a button before it becomes clickable, causing random failures depending on page loading speed.

---

## Prevention Strategies

1. Replace `time.sleep()` with Explicit Waits.

2. Use stable locators such as ID or CSS selectors.

3. Keep test cases independent so they do not rely on previous tests.

---

# Task 2 – Compare Automation Framework Types

## 5. Framework Comparison

### Linear Framework

**Description**

Tests are written sequentially in a single script with little or no modularization.

**Advantage**

Simple to create.

**Disadvantage**

Poor reusability and difficult maintenance.

**Example**

Testing a single login page for a small application.

---

### Modular Framework

**Description**

Application functions are divided into reusable modules.

**Advantage**

Easy maintenance and code reuse.

**Disadvantage**

Requires initial planning.

**Example**

Separate modules for Login, Course Management, and Student Management.

---

### Data-Driven Framework

**Description**

Test data is stored separately from test scripts.

**Advantage**

One script can execute many test cases.

**Disadvantage**

Requires external data files.

**Example**

Testing login using multiple username-password combinations.

---

### Keyword-Driven Framework

**Description**

Tests are driven by predefined keywords such as Click, Enter Text, Verify, etc.

**Advantage**

Non-technical users can create test cases.

**Disadvantage**

Framework implementation is more complex.

**Example**

Business analysts create test cases using keywords.

---

### Hybrid Framework

**Description**

Combines Modular, Data-Driven, and Keyword-Driven approaches.

**Advantage**

Highly flexible, reusable, and scalable.

**Disadvantage**

Higher initial development effort.

**Example**

Large enterprise Course Management System.

---

# 6. Recommended Framework

### Recommendation

A **Hybrid Framework** combining:

- Modular Framework
- Data-Driven Framework
- Keyword-Driven Framework

### Justification

- Supports testing 50 different login combinations.
- Allows login functionality to be reused across multiple test cases.
- Enables both technical and non-technical team members to contribute.
- Easier to maintain and scale as the application grows.

---

# 7. Hybrid Framework Folder Structure

```
CourseManagementAutomation/

│
├── config/
│   └── config.py
│
├── test_data/
│   ├── login_data.xlsx
│   └── course_data.xlsx
│
├── pages/
│   ├── login_page.py
│   ├── course_page.py
│   └── student_page.py
│
├── tests/
│   ├── test_login.py
│   ├── test_course.py
│   └── test_student.py
│
├── utilities/
│   ├── browser_setup.py
│   ├── logger.py
│   └── helpers.py
│
├── reports/
│
├── screenshots/
│
├── requirements.txt
│
└── README.md
```

---

## Conclusion

The Hybrid Framework is the most suitable choice for the Course Management System because it provides high code reusability, supports data-driven testing, enables collaboration between technical and non-technical team members, and is easy to maintain as the project grows.