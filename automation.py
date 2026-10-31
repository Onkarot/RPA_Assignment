import csv
import logging
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)
url = "https://opensource-demo.orangehrmlive.com"

def run_automation(form_data):
    driver = None
    wait = None
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    try:
        logger.info("Starting automation process...")

        # Launch the browser
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 15)

        # 1. Open website
        driver.get(url)
        logger.info(f"Navigated to {url}")

        # 2. Login
        username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password = wait.until(EC.presence_of_element_located((By.NAME, "password")))

        username.send_keys(form_data["username"])
        password.send_keys(form_data["password"])

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        logger.info("Login submitted")

        # Verify login success
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))
        logger.info("Login successful, navigating to PIM section")


        # 3. Navigate to PIM
        pim=wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']")))
        pim.click()
        logger.info("Navigated to PIM section")

        # 4. Click on Add Employee
        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']")))
        add_button.click()
        logger.info("Clicked on Add Employee button")

        # 5. Fill in employee details
        first_name_input = wait.until(EC.visibility_of_element_located((By.NAME, "firstName")))
        last_name_input = wait.until(EC.visibility_of_element_located((By.NAME, "lastName")))
        employee_id_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='Employee Id']/../following-sibling::div//input")))

        first_name_input.send_keys(form_data["first_name"])
        last_name_input.send_keys(form_data["last_name"])

        employee_id_input.click()
        employee_id_input.send_keys(Keys.CONTROL, "a")
        employee_id_input.send_keys(Keys.BACKSPACE)
        employee_id_input.send_keys(form_data["employee_id"])

        actual_employee_id = employee_id_input.get_attribute("value")

        logger.info(f"Employee ID entered: {actual_employee_id}")

        if actual_employee_id != form_data["employee_id"]:
            raise Exception(
                f"Employee ID mismatch. Expected: {form_data['employee_id']}, "
                f"Got: {actual_employee_id}"
            )

        logger.info(f"Filled employee details: {form_data['first_name']} {form_data['last_name']} (ID: {form_data['employee_id']})")

        # Take screenshot before saving
        driver.save_screenshot(f"screenshots/{form_data['employee_id']}_before_save.png")
        logger.info("Captured screenshot before saving")

        # 6. Save the employee details
        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
        save_button.click()
        logger.info("Clicked on Save button")

        # 7. Verify employee added successfully
        # Wait until the Personal Details page is loaded
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[text()='Personal Details']")))

        # Wait until employee details are displayed
        wait.until(EC.visibility_of_element_located((By.NAME, "firstName")))
        wait.until(lambda d: d.find_element(By.NAME, "firstName").get_attribute("value") == form_data["first_name"])
        wait.until(lambda d: d.find_element(By.NAME, "lastName").get_attribute("value") == form_data["last_name"])
        logger.info("Employee details page fully loaded")

        # Capture screenshot after details are visible
        driver.save_screenshot(f"screenshots/{form_data['employee_id']}_employee_created.png")

        logger.info("Captured employee created screenshot")

        # Take screenshot After saving
        driver.save_screenshot(f"screenshots/{form_data['employee_id']}_employee_created.png")
        logger.info("Captured employee created screenshot")

        # 8. Navigate back to PIM employee list
        pim = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']")))
        pim.click()
        logger.info("Navigated back to PIM section")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h5[text()='Employee Information']")))
        logger.info("Employee Information page loaded")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "oxd-table")))
        logger.info("Employee table loaded")
        table_rows = driver.find_elements(By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
        logger.info(f"Found {len(table_rows)} employee rows")

        # 9. Export employee table data
        employee_id_search = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='Employee Id']/following::input[1]")))

        employee_id_search.clear()
        employee_id_search.send_keys(form_data["employee_id"])
        logger.info(f"Searching employee ID: {form_data['employee_id']}")
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Search']")))
        search_button.click()

        # Wait until either employee rows appear or no records are found
        def search_completed(driver):
            try:
                table_body = driver.find_element(By.CLASS_NAME, "oxd-table-body")
                if "No Records Found" in table_body.text:
                    return "NO_RECORDS"

                rows = table_body.find_elements(By.CSS_SELECTOR, ".oxd-table-row")

                for row in rows:
                    cells = row.find_elements(By.CSS_SELECTOR, ".oxd-table-cell")
                    values = [cell.text.strip() for cell in cells]

                    if len(cells) >= 4:
                        if values[1] == form_data["employee_id"]:
                            return {
                                "employee_id": values[1],
                                "first_name": values[2],
                                "last_name": values[3]
                            }
                no_records = driver.find_elements(By.XPATH, "//*[normalize-space()='No Records Found']")
                if no_records:
                    return "NO_RECORDS"

                return False
            except StaleElementReferenceException:
                return False

        search_result = wait.until(search_completed)

        if search_result == "NO_RECORDS":
            raise Exception(f"No employee found with ID {form_data['employee_id']}")

        employees = [search_result]

        logger.info(f"Retrieved {len(employees)} employees")
        logger.info(f"Verified employee: {search_result}")

        # Store the currently displayed rows before clearing the filter
        old_rows = driver.find_elements(By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")

        old_first_row = old_rows[0] if old_rows else None

        # Clear Employee ID filter properly
        employee_id_locator = (By.XPATH, "//label[text()='Employee Id']/following::input[1]")

        employee_id_search = wait.until(EC.visibility_of_element_located(employee_id_locator))

        employee_id_search.click()
        employee_id_search.send_keys(Keys.CONTROL, "a")
        employee_id_search.send_keys(Keys.BACKSPACE)

        # Verify that the filter is empty
        wait.until(lambda d: d.find_element(*employee_id_locator).get_attribute("value") == "")

        logger.info("Employee ID filter is empty now")

        # Click Search to fetch all employees
        search_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Search']")
            )
        )
        search_button.click()

        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "oxd-table-body"))
        )

        # Verify that the filter is still empty
        current_value = driver.find_element(*employee_id_locator).get_attribute("value")
        logger.info(f"Employee ID filter after search: '{current_value}'")

        if current_value != "":
            raise Exception("Employee ID filter is still active.")

        # Read displayed table rows
        table_rows = driver.find_elements(
            By.CSS_SELECTOR,
            ".oxd-table-body .oxd-table-row"
        )

        logger.info(f"Actual rows displayed: {len(table_rows)}")

        wait.until(
            lambda d: (
                len(d.find_elements(
                    By.CSS_SELECTOR,
                    ".oxd-table-body .oxd-table-row"
                )) > 0
                or "No Records Found" in d.find_element(
                    By.CLASS_NAME, "oxd-table-body"
                ).text
            )
        )

        logger.info("All employee table results loaded")
        # DEBUG: Check what OrangeHRM displays after clearing the filter
        search_value = employee_id_search.get_attribute("value")

        table_body = driver.find_element(By.CLASS_NAME, "oxd-table-body")

        logger.info(f"Employee ID search field value: '{search_value}'")
        logger.info(f"Employee table content: {table_body.text}")

        rows = driver.find_elements(
            By.CSS_SELECTOR,
            ".oxd-table-body .oxd-table-row"
        )

        logger.info(f"Actual rows displayed: {len(rows)}")

        # Check pagination information
        pagination = driver.find_elements(
            By.CSS_SELECTOR,
            ".oxd-pagination"
        )

        if pagination:
            logger.info(f"Pagination information: {pagination[0].text}")
        else:
            logger.info("Pagination element not found")

        # Check all buttons inside pagination
        pagination_buttons = driver.find_elements(
            By.CSS_SELECTOR,
            ".oxd-pagination button"
        )

        for button in pagination_buttons:
            logger.info(
                f"Pagination button: text='{button.text}', "
                f"class='{button.get_attribute('class')}', "
                f"disabled='{button.get_attribute('disabled')}'"
            )

        employees = []
        seen_ids = set()

        while True:

            table_rows = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
                )
            )

            
            for row in table_rows:
                cells = row.find_elements(By.CSS_SELECTOR, ".oxd-table-cell")
                values = [cell.text.strip() for cell in cells]

                if len(values) < 4:
                    logger.warning(f"Skipping row: Only {len(values)} cells - {values}")
                    continue

                if not values[1]:
                    logger.warning(f"Skipping row: Employee ID is empty - {values}")
                    continue

                employee_id = values[1]
                if not employee_id.isdigit():
                    logger.warning(f"Invalid Employee ID skipped: {employee_id}")
                    continue

                if employee_id in seen_ids:
                    logger.warning(f"Duplicate Employee ID skipped: {employee_id}")
                    continue

                employees.append({
                    "employee_id": employee_id,
                    "first_name": values[2],
                    "last_name": values[3]
                })

                seen_ids.add(employee_id)
            logger.info(f"Total employees extracted so far: {len(employees)}")

            # Find the Next Page button
            next_buttons = driver.find_elements(By.CSS_SELECTOR, "button.oxd-pagination-page-item--next")

            if not next_buttons:
                logger.info("Next page button not found. Extraction completed.")
                break

            next_button = next_buttons[0]

            # Stop when Next Page is disabled
            if (not next_button.is_enabled() or next_button.get_attribute("disabled") is not None):
                logger.info("Last page reached.")
                break

            # Remember the first employee ID on the current page
            first_row = table_rows[0]
            first_cells = first_row.find_elements(
                By.CSS_SELECTOR, ".oxd-table-cell"
            )
            previous_first_id = first_cells[1].text.strip()

            next_button.click()

            # Wait for the next page to load
            wait.until(
                lambda d: (
                    len(d.find_elements(
                        By.CSS_SELECTOR,
                        ".oxd-table-body .oxd-table-row"
                    )) > 0
                    and
                    d.find_elements(
                        By.CSS_SELECTOR,
                        ".oxd-table-body .oxd-table-row"
                    )[0].find_elements(
                        By.CSS_SELECTOR, ".oxd-table-cell"
                    )[1].text.strip() != previous_first_id
                )
            )

        # Ensure newly created employee is included
        if not any(
            emp["employee_id"] == form_data["employee_id"]
            for emp in employees
        ):
            employees.append({
                "employee_id": form_data["employee_id"],
                "first_name": form_data["first_name"],
                "last_name": form_data["last_name"]
            })
            logger.info("Newly created employee added to extracted records.")
        logger.info(f"Completed extraction. Total employees: {len(employees)}")

        # Screenshot after employee list extraction
        driver.save_screenshot(
            f"screenshots/{form_data['employee_id']}_employee_list.png"
        )

        logger.info("Captured employee list screenshot")

        # 10. Export to CSV
        with open("output/employees.csv", mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["employee_id", "first_name", "last_name"])
            writer.writeheader()
            writer.writerows(employees)
            logger.info(f"CSV created: {os.path.abspath('output/employees.csv')}")
            logger.info(f"Total records exported: {len(employees)}")

        # 11. Logout
        profile = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-tab")))
        profile.click()
        logger.info("Clicked on profile dropdown")

        logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']")))
        logout_button.click()
        logger.info("Clicked on Logout button")

        wait.until(EC.visibility_of_element_located((By.NAME, "username")))

        driver.save_screenshot(f"screenshots/{form_data['employee_id']}_after_logout.png")
        logger.info("Captured after logout screenshot")

        return{
            "success": True,
            "message": "Employee added successfully and data exported to employees.csv",
            "employee": {
                "employee_id": form_data["employee_id"],
                "first_name": form_data["first_name"],
                "last_name": form_data["last_name"]
            },
            "employees": employees
        }

    except Exception as e:
        logger.exception("An error occurred during automation")
        error_message = f"{type(e).__name__}: {str(e)}"

        if driver:
            try:
                driver.save_screenshot(f"screenshots/error_{form_data['employee_id']}.png")
                logger.info(f"Saved screenshot of error for employee ID {form_data['employee_id']}")
            except Exception as e:
                logger.error(f"An error occurred while saving screenshot: {e}")

        return {
            "success": False,
            "message": f"An error occurred during automation: {error_message}",
            "employee": None,
            "employees": []
        }

    finally:
        if driver:
            driver.quit()
            logger.info("Closed the browser and ended the automation process")