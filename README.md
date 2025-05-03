# Paths - an interactive path editor
## Features
The user can create an account on the webiste. Having the account created, the user can create, edit, view and delete
paths on backgrounds provided by the administration. The paths can also be managed through an API which is accessible
only for people with an account (an authorization token must be passed in each request).

All the main functionalities are accessible through the main webiste's URL.
The admin panel is accessible through `/admin`. It is necessary to add backgrounds through this panel,
otherwise no path can be created.
The documentation for the API is accessible through `/api/doc`.

## Deployment steps
1. Clone the repository,
2. Create a virtual enviroment: `python3 -m venv <venv_folder_name>`,
3. Activate it: `source <venv_folder_name>/bin/activate`,
4. Install dependencies: `pip install -r requirements.txt`,
5. Apply database migrations: `python manage.py migrate`,
6. (Optional) Run tests: `python manage.py test`,
8. Create a superuser: `python manage.py createsuperuser` and follow prompts,
9. Run the server: `python manage.py runserver`,
10. Add at least 1 background through the admin panel (`/admin` site, login with the created superuser's credentials).

Now the site is ready to be used. Note that for now only debug backend configuration is enabled.
