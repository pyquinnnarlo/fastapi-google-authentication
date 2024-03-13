

```markdown
# FastAPI Google OAuth Example

This is an example FastAPI application demonstrating how to integrate Google OAuth for user authentication.

## Setup

1. Clone this repository:

git clone https://github.com/yourusername/your-repo.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add the following variables:

```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

Replace `your-google-client-id` and `your-google-client-secret` with your actual Google OAuth credentials.

4. Run the application:

```bash
uvicorn main:app --reload
```

The application will be running at `http://localhost:8000`.

## Usage

- Navigate to `http://localhost:8000/` in your browser to access the homepage.
- If you are not logged in, you will see a "login" link. Click it to initiate the Google OAuth login process.
- After logging in, you will be redirected back to the homepage with your user information displayed.
- To log out, click the "logout" link.

## Endpoints

### GET /

Renders the homepage with user information if the user is logged in; otherwise, provides a login link.

### GET /login

Initiates the login process by redirecting the user to the Google OAuth authorization page.

### GET /auth

Handles the callback from the Google OAuth authorization page after user authentication. 
This endpoint receives the authorization code from Google OAuth and exchanges it for an access token.

### GET /logout

Logs out the user by removing their session information and redirecting them to the root URL.

## Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
```

Make sure to replace placeholders such as `yourusername`, `your-repo`, `your-google-client-id`, and `your-google-client-secret` with your actual information and credentials. Additionally, if your project uses a specific license, make sure to update the license section accordingly.
