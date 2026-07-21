"""
REQUEST-RESPONSE CYCLE

1. Browser sends an HTTP GET request to /api/courses/.

2. Django receives the request and creates an HttpRequest object.

3. The request first passes through Middleware, where tasks such as authentication,
session handling, security checks, and logging can occur.

4. The URL Router (urls.py) matches the requested URL to the appropriate view.

5. The View processes the request and performs business logic.

6. If data is required, the View communicates with the Model.

7. The Model interacts with the database and retrieves or updates data.

8. The View prepares an HTTP response (HTML, JSON, or plain text).

9. The response again passes through middleware before being sent back to the browser.
"""

"""
MIDDLEWARE IN THE REQUEST-RESPONSE CYCLE

Middleware sits between the browser and the view. Every incoming request passes
through middleware before reaching the URL router and view. Likewise, every
outgoing response also passes through middleware before being sent back to the browser.

Request Flow: Browser -> Middleware -> URL Router-> View -> Model -> Database

Response Flow: Database->Model->View->Middleware->Browser

Two built-in Django middleware classes:

1. SecurityMiddleware
   - Adds security-related HTTP headers.
   - Helps enforce HTTPS.
   - Protects against common web vulnerabilities.

2. SessionMiddleware
   - Manages user sessions.
   - Stores session data so users remain logged in across multiple requests.
   - Allows the server to remember information about a user between requests.
"""

"""
WSGI vs ASGI

WSGI (Web Server Gateway Interface)
- Traditional Python web application interface.
- Handles requests synchronously (one request at a time per worker).
- Suitable for most standard web applications.
- Django uses WSGI by default through the wsgi.py file.

ASGI (Asynchronous Server Gateway Interface)
- Modern interface that supports asynchronous programming.
- Can handle multiple requests concurrently while waiting for I/O operations.
- Required for features such as WebSockets, real-time applications,
  streaming responses, and async database/API calls.

When to use ASGI:
- Real-time chat applications
- Live notifications
- WebSockets
- Streaming responses
- High-concurrency applications
- Applications using async/await extensively
"""

"""
MVC Pattern and Django's MVT

MVC (Model-View-Controller)

Model:
- Represents the application's data.
- Interacts with the database.
- Handles CRUD (Create, Read, Update, Delete) operations.

View:
- Represents the user interface.
- Displays data to the user.
- Contains the presentation layer.

Controller:
- Receives user requests.
- Processes business logic.
- Communicates with the Model.
- Selects the appropriate View to display.

Django follows the MVT (Model-View-Template) pattern.

Mapping MVC to Django MVT:

MVC Model       → Django Model
MVC Controller  → Django View
MVC View        → Django Template

In Django, the View performs the role of the Controller by handling requests,
interacting with models, and selecting templates to render responses.
"""