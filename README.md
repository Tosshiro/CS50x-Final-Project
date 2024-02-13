# Budget Tracker

## Description:
A simple and easy Monthly Budget tracker for any users to use!

1) Start by registering an account for the Budget tracker by clicking the top right scroller button.
2) Log into your registered account afterwards.
3) Once logged in, set your monthly budget value!
4) Afterwards, any expense by you can be recorded in the expense webpage. (Enter the cause of expense and expense amount)
5) Lastly, you can observe your previous expenses and your remaining budget for the month in the history webpage!

### Things to take note
- If you wish to change your monthly budget amount, just head to the budget webpage to do so! The previous expenses will reflect directly on the newly set budget value

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
- SQL file **budget.db** contains a table called **users** and **expenses**.
- The users table contains a id, a username (Prevent duplicates of usernames), a hashed password as well as user's monthly budget amount, which is submitted through budget.html.
- The expenses table contains a id too, user_id, expense column (Cost of expenditure) and reason column (Cause of expenditure). A row of information is added to this SQL table when user inputs expenditure details in expense.html. Expense table is used in history.html to showcase user's past expenditures through a table.
- id for both tables is important to identify which user is currently logged in, thus returning that user's necessary details like monthly budget value and etc...

#### Python files
- **app.py** contains most of the code and the logic. Such as bringing the user to apology.html when user inputs something wrong. It contains all the function and logic behind each HTML webpage.
- **helpers.py** are several functions (EG: apology) imported into app.py. It also has a login_required function (Credits to CS50 finance) which allows only some webpages to be accessible only when user is logged in.

![Savings](Savings.jpeg)