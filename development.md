# Purpose of the development branch
This is the core development branch. All modules should be put in subbranches of this branch. When ever you create a new module or a component to the project create a new branch under development and name it suhch a way it can be recognised as subbranch. For example `dev-mainwindow` when you create a GUI for the main window.

## Merging
Sub branches will be merged to the development branch after successfull review of the module or component. After this merge the development branch can be merged to sub brances when needed. Development will be merged to the main branch for releasing a new version of the application.

## Subbranching
When you create a new subbranch you must create a markdown file for describing you module or component to other developpers. Name your file accordingly for example `mainwindow.md`.

## Editing environment
All coding is made in the virtual environment. You can create it in the terminal by typing `python -m venv venv`.
After creating the virtual envirnonmet you should activate it. Go to the `venv\Scripts` folder and run Activat.ps1 script by typing `.\Activate`. Check that you are using python interpretter from virtual environment.
