import json
from fastapi import FastAPI
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")

config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)




@app.get('/')
async def homepage(request: Request):
    """
    Renders the homepage with user information if the user is logged in; otherwise, provides a login link.

    This endpoint checks if a user is logged in by checking the session. If a user is found in the session,
    their information is displayed on the homepage. If no user is found, a login link is provided.

    Parameters:
        request (Request): The incoming request object containing information about the HTTP request.

    Returns:
        HTMLResponse: An HTML response containing user information and a logout link if logged in;
                      otherwise, a login link.

    Example:
        Upon accessing the root URL ('/'), the endpoint checks if a user is logged in. If logged in,
        the user's information is displayed along with a logout link. If not logged in, a login link
        is provided to allow the user to log in.
    """
    user = request.session.get('user')
    # If user exists
    if user:
        # Convert user to JSON
        data = json.dumps(user)
        # Create HTML response
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    # If no user, return login link
    return HTMLResponse('<a href="/login">login</a>')




@app.get('/login')
async def login(request: Request):
    """
    Initiates the login process by redirecting the user to the Google OAuth authorization page.

    Parameters:
        request (Request): The incoming request object containing information about the HTTP request.

    Returns:
        Response: A redirect response to the Google OAuth authorization page for user authentication.

    Example:
        After accessing this endpoint, the user will be redirected to the Google OAuth
        authorization page where they can authenticate and authorize access to their
        Google account. Upon successful authentication, the user will be redirected back
        to the provided redirect URI with an authorization code.
    """
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)





@app.get('/auth')
async def auth(request: Request):
    """
    Handles the callback from the Google OAuth authorization page after user authentication.

    This endpoint receives the authorization code from Google OAuth and exchanges it for an access token.
    Upon successful authentication, the user's information is retrieved from Google and stored in the session.

    Parameters:
        request (Request): The incoming request object containing information about the HTTP request.

    Returns:
        RedirectResponse: A redirect response to the root URL ('/') after successful authentication.
        HTMLResponse: An HTML response displaying the error message if authentication fails.

    Example:
        After the user authenticates on the Google OAuth authorization page, Google redirects
        the user back to this endpoint with an authorization code. This code is then exchanged
        for an access token. If successful, the user's information is stored in the session,
        and the user is redirected to the root URL.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')




@app.get('/logout')
async def logout(request: Request):
    """
    Logout the user by removing their session information and redirecting them to the root URL.

    This endpoint clears the user session, effectively logging them out of the system.

    Parameters:
        request (Request): The incoming request object containing information about the HTTP request.

    Returns:
        RedirectResponse: A redirect response to the root URL ('/') after logging out the user.

    Example:
        When the user accesses this endpoint, their session information, including user details,
        is removed. After successful logout, the user is redirected to the root URL.
    """
    request.session.pop('user', None)
    return RedirectResponse(url='/')