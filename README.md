## Bubble Job Board API

Welcome to the Bubble Job Board API documentation. This API provides endpoints for managing job listings, user authentication, and job applications for a decentralized payment-enabled job platform. The API is built using Django Rest Framework (DRF) with two main apps: users and jobs.

## Authentication
The users app utilizes JWT (JSON Web Tokens) for authentication. This means that to access protected endpoints, clients must include a valid JWT token in the Authorization header of their HTTP requests.

## Endpoints
User Registration

## POST /users/auth/register/
Register a new user. Requires username, email, and password fields in the request body.
User Authentication

## POST /users/auth//login/
Obtain a JWT token by providing username and password in the request body.
User Profile

## GET /users/auth//profile/<str:pk>
Retrieve the authenticated user's profile information.
## UPDATE /api/users/auth/profile/<str:pk>
Update the authenticated user's profile information.
Job Listings
The jobs app manages job listings, allowing users to view, post, edit, and apply for jobs.

## Endpoints
Job Listings

## GET /jobs/
Retrieve a list of all job listings.
## UPDATE /jobs/
Post a new job listing. Requires authentication as an employer.
## Job Details

## GET /jobs/<job_id>/
Retrieve details of a specific job listing.
## UPDATE /jobs/<job_id>/
Update details of a job listing. Requires authentication as the job poster.
## DELETE /jobs/<job_id>/
Delete a job listing. Requires authentication as the job poster.
## Job Applications

## POST /jobs/<job_id>/apply/
Apply for a job listing. Requires authentication as a job seeker.
## Permissions
Only authenticated users can access most endpoints.
Job posting, updating, and deletion can only be performed by the user who created the job listing.
Job applications can only be submitted by authenticated users.
## Error Handling
The API returns appropriate HTTP status codes and error messages in JSON format to indicate the success or failure of requests.

## Decentralized Payment
For decentralized payment integration, additional endpoints and functionalities would need to be implemented, potentially using blockchain technology or other decentralized protocols. This aspect is not covered in the current version of the API.

## Getting Started
Installation

Clone the repository.
Install dependencies: pip install -r requirements.txt.
Set up your database and migrate: python manage.py migrate.
Create a superuser: python manage.py createsuperuser.
Run the development server: python manage.py runserver.
Usage

Obtain JWT tokens by registering and logging in.
Use the obtained tokens in the Authorization header for authenticated requests.