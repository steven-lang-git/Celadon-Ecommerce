

# Django Project Setup Guide

This guide will help you set up a Django project on a new machine after cloning a Git repository.


## Setup Instructions

1. **Clone the Git Repository:**
   ```
   git clone <repository_url>
   ```
   Replace `<repository_url>` with the URL of the Git repository you want to clone.

2. **Create and Activate a Virtual Environment:**
   - On Windows:
     ```
     python -m venv env
     env\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     python -m venv env
     source env/bin/activate
     ```

3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure the Database:**
   Update the database settings in the `settings.py` file.

5. **Run Database Migrations:**
   ```
   python manage.py migrate
   ```

6. **Create a Superuser (Optional):**
   ```
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**
   ```
   python manage.py runserver
   ```

The development server will start running locally, and you can access the project in your web browser at `http://localhost:8000` or another specified address.

## Making Changes Using Git

If you want to contribute to the project or make changes to the code, follow these steps:

1. **Add Changes:**
   Use the following command to add the modified files or new files to the staging area:
   ```
   git add .
   ```
   The `.` represents all the changes in the current directory. If you want to add specific files, replace `.` with the file names.

2. **Commit Changes:**
   Commit your changes with a descriptive message using the following command:
   ```
   git commit -m "Your commit message here"
   ```
   Replace `"Your commit message here"` with a meaningful message summarizing your changes.

3. **Pull Changes (Optional):**
   Before pushing your changes, it's a good practice to pull any updates from the remote repository. Use the following command:
   ```
   git pull origin <branch_name>
   ```
   Replace `<branch_name>` with the name of the branch you want to pull updates from.

4. **Push Changes:**
   Push your committed changes to the remote repository using the following command:
   ```
   git push origin <branch_name>
   ```
   Replace `<branch_name>` with the name of the branch you want to push changes to.

Please note that you may need appropriate permissions and access to push changes to the repository.


