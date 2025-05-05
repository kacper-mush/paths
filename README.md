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


## Site presentation examples

### Welcome page
![welcome_page](https://github.com/user-attachments/assets/8936950f-4669-4890-ba33-b97b170f61b7)

### Register page
![register_page](https://github.com/user-attachments/assets/c167716f-5ea4-4859-b052-127e23e3d887)

### User dashboard
![dashboard](https://github.com/user-attachments/assets/0427de89-119e-4b8e-9190-89521f1e17b0)

### Path creation
![path_creation](https://github.com/user-attachments/assets/d1263e80-fa84-4c2f-a8ba-d4df91a61234)

### Path editing
![edit_1](https://github.com/user-attachments/assets/8c5ab5f0-6138-4e05-8e6d-93a767c9ce2d)

### Path editing (hidden UI)
![edit 2](https://github.com/user-attachments/assets/d4de3b2a-7396-4845-bcf0-5c7a682463bc)

### Viewing
![viewing](https://github.com/user-attachments/assets/272500dc-d86a-49ed-8cc3-2c4d92ed793c)

### Documentation site
![doc](https://github.com/user-attachments/assets/d7f6e591-0788-41f8-9c27-373c16b20d2b)



