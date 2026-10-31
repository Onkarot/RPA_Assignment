const form = document.getElementById('automationForm');

form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const button = document.getElementById('submitbtn');
    const status = document.getElementById('status');

    button.disabled = true;
    button.innerText = 'Processing...';

    status.innerText = 'Processing your request...';
    status.className = "";

    const employeeData = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
        first_name: document.getElementById("fname").value,
        last_name: document.getElementById("lname").value,
        employee_id: document.getElementById("employeeId").value
    };

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(employeeData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'An error occurred while processing your request.');
        }

        status.innerText = result.message || 'Automation completed successfully!';
        status.className = "success";

        // Display employee data
        const employeeresult = result.result;
        if (!employeeresult.success) {
            throw new Error(employeeresult.message || "Automation failed.");
        }
        const employee = employeeresult.employee;

        if (employee) {
           document.getElementById('employeeTableBody').innerHTML = `
                <tr>
                    <td>${escapeHTML(employee.employee_id)}</td>
                    <td>${escapeHTML(employee.first_name)}</td>
                    <td>${escapeHTML(employee.last_name)}</td>
                </tr>
            `;
        }

        const employeeList = document.getElementById('extractedDataTableBody');

        employeeList.innerHTML = (employeeresult.employees || []).map(emp => `
            <tr>
                <td>${escapeHTML(emp.employee_id)}</td>
                <td>${escapeHTML(emp.first_name)}</td>
                <td>${escapeHTML(emp.last_name)}</td>
            </tr>
        `).join("");
    }

    catch (error) {
        status.innerText = error.message;
        status.className = "error";
    }

    finally {
        button.disabled = false;
        button.innerText = 'Submit';
    }
});

function escapeHTML(value) {
    const div = document.createElement('div');
    div.textContent = value ?? "";
    return div.innerHTML;
}