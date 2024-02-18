# Budget Tracker

## Purpose
A simple and easy Monthly Budget tracker for any users who wishes to save some money! Users can use this code to input and track their expenses, and limit their monthly expenditure to an amount that they are satisfied with!

## Description:

1) Head to budget.db and create SQL tables by copy and pasting code inside budget.db using sqlite3.
2) Type in "flask run" in terminal to open the HTML webpage
3) Start by registering an account for the Budget tracker by clicking the top right scroller button.
4) Log into your registered account afterwards.
5) Once logged in, set your monthly budget value!
6) Afterwards, any expense by you can be recorded in the expense webpage. (Enter the cause of expense and expense amount)
7) Lastly, you can observe your previous expenses and your remaining budget for the month in the history webpage!

### Things to take note
- If you wish to change your monthly budget amount, just head to the budget webpage to do so! The previous expenses will reflect directly on the newly set budget value.

### Things to add to improve this Final Project
- A delete button for wrongly inputed expenses
- A prediction on if the user will exceed his budget value based on current expenditure amount

## Details on this Final Project

#### Static Folder
- Contains **styles.css**
- Some CSS code to decorate this webpage. EG: Setting the webpage to a darker colour scheme

#### Templates Folder
- **apology.html** is the error page when a user mis-inputs something such as a username in the login page
- **budget.html** contains the page where user can set their monthly budget value. User is able to change their monthly budget value by entering another budget value. Brings user to index.html after submitting monthly budget value
- **expense.html** is the page where the user records down previous expenditure. Cause of expenditure and cost of expenditure is required. After submitting, brings user to history.html
- **history.html** is a page with a table with user's previous recorded expenditure, together with the date of expenditure recorded. It always shows the user's current budget left for the month
- **index.html** is the homepage after user logs in
- **layout.html** is a layout webpage used in all HTMLS. It contains the design such as the blue colour scheme of the webpages and many more
- **login.html** and **register.html** is the login and register page where users will have to create an account to use their budget tracker

#### SQL databases
- SQL file **budget.db** should contain tables called **users** and **expenses**.
- The users table contains a id, a username (Prevent duplicates of usernames), a hashed password as well as user's monthly budget amount, which is submitted through budget.html.
- The expenses table contains a id too, user_id, expense column (Cost of expenditure) and reason column (Cause of expenditure). A row of information is added to this SQL table when user inputs expenditure details in expense.html. Expense table is used in history.html to showcase user's past expenditures through a table.
- id for both tables is important to identify which user is currently logged in, thus returning that user's necessary details like monthly budget value and etc...
- User has to use sqlite3 and create the tables users and expenses himself (SQL code is inside budget.db)

#### Python files
- **app.py** contains most of the code and the logic. Such as bringing the user to apology.html when user inputs something wrong. It contains all the function and logic behind each HTML webpage.
- Most routes support GET and POST, where GET route is simply reached by clicking on the specific link, while POST route reached by submitting/entering some infomation.


- **helpers.py** are several functions (EG: apology function) imported into app.py.
- It has a login_required function (Credits to CS50 finance) which allows only some webpages to be accessible only when user is logged in. This decorator ensures any user who tries to visit any of those routes to be redirected to login so as to log in.
- It also contains an apology function which renders **apology.html** when user mis-inputs something.

![Savings](images/Savings.jpeg)
