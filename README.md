# SparkleWash - Premium Car Wash Booking System

A high-end, responsive web application for booking car wash services, featuring a "Pitch Black" premium theme with Gold accents.

## Features

*   **Premium User Interface**: Glassmorphism design, animated hero slideshow, and cinematic service cards.
*   **Booking System**: Interactive slot selection with real-time availability.
*   **User Management**: Customer registration, login, and dashboard to view booking history.
*   **Admin Panel**: Comprehensive dashboard for administrators to manage bookings and user accounts.
*   **Responsive Design**: Optimized for both desktop and mobile devices.

## Installation & Setup

1.  **Clone the repository** (or download the files).

2.  **Install Dependencies**:
    Make sure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize Database**:
    The application uses SQLite. The database is initialized automatically on first run, or you can manually ensure the schema is applied.
    *Note: A default `carwash.db` is included.*

## Running the Application

1.  **Start the Server**:
    ```bash
    python run.py
    ```

2.  **Access the App**:
    Open your browser and navigate to:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Project Structure

*   `app/`: Core application package.
    *   `routes.py`: URL routes and logic.
    *   `models.py`: Database models (User).
    *   `templates/`: HTML templates (Jinja2).
    *   `static/`: CSS styles, JavaScript, and images.
*   `scripts/`: Utility scripts (e.g., `reset_admin.py`, image generators).
*   `run.py`: Application entry point.
*   `requirements.txt`: Python dependencies.

## Default Credentials

*   **Admin Email**: `admin@sparklewash.com`
*   **Password**: `admin123`
*(You can reset this using `python scripts/reset_admin.py`)*
