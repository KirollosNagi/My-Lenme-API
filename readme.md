# My Lenme API

The My Lenme API is a RESTful API built with Django and Django REST framework that provides loan management functionality for borrowers and investors on the Lenme platform.

## Features
* Borrowers can submit loan requests with loan amount and loan period.
* Investors can submit loan offers with annual interest rate for loan requests.
* Borrowers can accept loan offers.
* The API automatically checks if the investor has sufficient balance to fund the loan.
* Loans are funded and scheduled for payments once accepted by the borrower.
* Payments are automatically scheduled based on the loan period.
* Loans are marked as completed once all payments are successfully paid back.

## Installation
* Clone the repository to your local machine:

        git clone https://github.com/KirollosNagi/My-Lenme-API

* Change to the project directory:

        cd My-Lenme-API

* Create and activate a virtual environment:

        python -m venv env
        source env/bin/activate  # for Linux/Mac
        .\env\Scripts\activate  # for Windows

* make database migrations:

        python manage.py makemigrations

* Run database migrations:

        python manage.py migrate

* Start the development server:
        
        python manage.py runserver

* Access the API at http://127.0.0.1:8000/ in your web browser or via a REST client.

## API Endpoints
### Borrower

- `GET /borrower/list/`: Retrieve a list of borrowers (admin view).
- `POST /borrower/register/`: Register a new borrower.
- `GET /borrower/profile/`: Retrieve/update borrower's profile.
- `POST /borrower/deactivate/`: Deactivate borrower's profile.

### Investor

- `GET /investor/list/`: Retrieve a list of investors (admin view).
- `POST /investor/register/`: Register a new investor.
- `GET /investor/profile/`: Retrieve/update investor's profile.
- `POST /investor/deactivate/`: Deactivate investor's profile.

### Loan Requests

- `GET /loan/requests/`: Retrieve a list of loan requests.
- `POST /loan/requests/new/`: Submit a new loan request.
- `GET /loan/requests/<int:pk>/`: Retrieve a loan request by ID.

### Loan Offers

- `GET /loan/offers/`: Retrieve a list of loan offers.
- `POST /loan/offers/new/`: Submit a new loan offer.
- `GET /loan/offers/<int:pk>/`: Retrieve a loan offer by ID.
- `POST /loan/offers/<int:pk>/accept/`: Accept a loan offer.

### Loans

- `GET /loan/loans/`: Retrieve a list of loans.
- `GET /loan/loans/<int:pk>/`: Retrieve a loan by ID.

### Payments

- `GET /loan/payments/`: Retrieve a list of payments.
- `GET /loan/payments/<int:pk>/`: Retrieve a payment by ID.

### Users

- `GET /user/users/`: Retrieve a list of users (admin view).
- `POST /user/signup/`: Register a new user.
- `POST /user/login/`: Login a user and obtain an access token.
- `POST /user/logout/`: Logout a user.


### Authentication
The API uses token-based authentication for authorized access to protected endpoints. To use the API, you need to obtain an authentication token by registering and logging in as a user.

* Register a new user: POST /api/register/
* Login and obtain token: POST /api/login/
* Include the token in the Authorization header of API requests in the format Token <token>.

## Testing
To run tests for the API, use the following command:


python manage.py test

## Built With
* Django - Python web framework
* Django REST framework - Toolkit for building APIs
* SQLite - Database for development

## License
This project is licensed under the MIT License - see the LICENSE file for details.

