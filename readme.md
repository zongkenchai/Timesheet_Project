# Timesheet Project

## Overview
The Timesheet Project is a CRM system designed to manage invoicing and timesheets efficiently. This project aims to streamline the process of tracking work hours and generating invoices for clients.

## Features
- **Invoicing**: Create and manage invoices for clients with ease.
- **Timesheet Management**: Track and record work hours for employees.
- **Client Management**: Maintain a database of clients and their details.
- **Reporting**: Generate detailed reports on work hours and invoices.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/timesheet_project.git
    ```
2. Navigate to the project directory:
    ```bash
    cd timesheet_project
    ```
3. Install the required packages using conda
    ```
    conda env create --file conda.yml
    ```
4. Setup the env file based on timesheet_project/copy.env
    - For the secret key
    ```
    django-admin shell
    from django.core.management.utils import get_random_secret_key  
    get_random_secret_key()
    ```

    - Setup the postgres database accordingly
    - For email and password, please follow this [link](https://support.google.com/accounts/answer/185833?hl=en) to setup the app password

5. Create a service account following the step [here](https://support.google.com/a/answer/7378726?hl=en)
    - Please enable Google Sheets and Google Drive API
    - Paste the service account json by creating a google_auth.json within the same directory as google_auth_copy.json

6. Insert a user that can register
    ```
    python manage.py register_email --email user_2:test@gmail.com
    ```
    
7. Run the following commands
    ```
    # Applying the db changes
    python manage.py migrate
    # Starting the server
    python manage.py runserver
    ```


