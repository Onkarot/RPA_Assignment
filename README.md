# OrangeHRM Employee Management – RPA Automation

## Project Overview

This project implements a dashboard-driven Robotic Process Automation (RPA) system using **Python, Selenium, FastAPI, HTML, CSS, and JavaScript**.

The application allows users to trigger employee management automation on the OrangeHRM demo website through a simple web dashboard.

Users can enter login credentials and employee details from the dashboard. The automation then logs into OrangeHRM, creates a new employee, verifies the employee record, extracts employee information, and exports the extracted data into a CSV file.

## Features

- **Dashboard Interface:** Simple and user-friendly web dashboard.
- **Automated Login:** Logs into OrangeHRM using user-provided credentials.
- **Employee Creation:** Automatically navigates to the PIM section and adds a new employee.
- **Employee Verification:** Verifies that the newly created employee has been saved successfully.
- **Employee Data Extraction:** Extracts employee IDs, first names, and last names from the employee list.
- **CSV Export:** Saves extracted employee records into a CSV file.
- **Screenshot Capture:** Captures screenshots during important automation steps.
- **Logging:** Maintains execution logs for monitoring and debugging.
- **Exception Handling:** Handles automation errors and browser cleanup.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Automation and backend logic |
| Selenium | Browser automation |
| FastAPI | Backend API |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| JavaScript | Frontend interactions |
| CSV | Employee data export |
| Google Chrome | Browser used for automation |

## Application Workflow

1. User opens the dashboard.
2. User enters OrangeHRM login credentials.
3. User enters employee details:
   - First Name
   - Last Name
   - Employee ID
4. User clicks the automation button.
5. FastAPI receives the dashboard data.
6. Selenium launches Chrome and logs into OrangeHRM.
7. Automation navigates to the PIM section.
8. A new employee is created.
9. The application verifies the newly created employee.
10. Automation extracts employee records from the employee list.
11. Extracted employee information is exported to a CSV file.
12. Screenshots and execution logs are saved.
13. Selenium logs out and closes the browser.
14. The dashboard displays the automation result.

## Project Structure


rpa_automation/
│
├── app.py                  # FastAPI backend
├── automation.py           # Selenium automation logic
├── requirements.txt        # Python dependencies
│
├── templates/
│   └── index.html          # Dashboard HTML
│
├── static/
│   ├── style.css           # Dashboard styling
│   └── script.js           # Dashboard JavaScript
│
├── output/
│   └── employees.csv       # Extracted employee records
│
├── screenshots/
│   └── Automation screenshots
│
├── logs/
│   └── Automation execution logs
│
└── README.md


## Installation and Setup

### 1. Clone the Repository


git clone <YOUR_GITHUB_REPOSITORY_URL>


### 2. Navigate to the Project Directory


cd rpa_automation


### 3. Create a Virtual Environment


python -m venv venv


Activate the virtual environment.

**Windows:**


venv\Scripts\activate


**Linux/macOS:**


source venv/bin/activate


### 4. Install Dependencies


pip install -r requirements.txt


### 5. Run the Application


uvicorn app:app --reload


### 6. Open the Dashboard

Open the following URL in your browser:


http://127.0.0.1:8000


Enter your OrangeHRM demo credentials and employee details to start the automation.

## Output Files

The application generates the following outputs:

| Output | Description |
|---|---|
| `employees.csv` | Extracted employee records |
| `screenshots/` | Screenshots captured during automation |
| `logs/` | Automation execution logs |

### CSV Output Format

The exported CSV contains the following columns:

csv
employee_id,first_name,last_name


## Website Used

**OrangeHRM Demo Website**

https://opensource-demo.orangehrmlive.com/

The application uses the OrangeHRM public demo environment for testing and demonstration purposes.

## Important Notes

- Use valid OrangeHRM demo credentials.
- Login credentials are entered through the dashboard.
- Do not commit passwords, API keys, or other sensitive information to GitHub.
- Make sure Google Chrome is installed.
- Keep the browser and Selenium dependencies compatible.
- The demo website may change its UI or data, which can affect automation selectors and results.
- This project is intended for educational and demonstration purposes.

## Future Improvements

- Add employee update and delete automation.
- Add Excel export functionality.
- Add automation execution history to the dashboard.
- Add better reporting and error notifications.
- Support additional employee search and filtering options.

## Author

**Onkar Otari**

Python Developer | RPA Automation | Backend Development

---

*Developed as part of an RPA Practical Assignment – Dashboard-Driven Automation.*