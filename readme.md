1. Install the required packages using conda
    ```
    conda env create --file timesheet_project/conda.yml
    ```


2. Setup the env file based on timesheet_project/copy.env
    - For the secret key
    ```
    django-admin shell
    from django.core.management.utils import get_random_secret_key  
    get_random_secret_key()
    ```

    - Setup the postgres database accordingly
    - For email and password, please follow this [link](https://support.google.com/accounts/answer/185833?hl=en) to setup the app password

3. Create a service account following the step [here](https://support.google.com/a/answer/7378726?hl=en)
    - Please enable Google Sheets and Google Drive API
    - Paste the service account json by creating a google_auth.json within the same directory as google_auth_copy.json

4. Run the following commands
```
cd timesheet_project

python manage.py migrate
python manage.py runserver
```