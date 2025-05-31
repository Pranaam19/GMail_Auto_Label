# GMail Auto Label - Web Application

This application automatically analyzes and labels your Gmail emails using AI, helping you organize your inbox more efficiently. This README provides instructions for setting up and running the Flask web application.

## Prerequisites

Before you begin, ensure you have the following:

*   **Python 3.8+** and **pip** (Python package installer).
*   Access to a **Google Account** and your Gmail inbox.
*   A **Google Cloud Project** to obtain OAuth 2.0 credentials for the Gmail API.
*   A **Google PaLM API Key** (or an API key for the relevant Google generative language model service) for email processing.

## Setup

Follow these steps to set up the application:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Pranaam19/GMail_Auto_Label.git
    ```

2.  **Navigate to the repository directory:**
    ```bash
    cd GMail_Auto_Label
    ```

3.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4.  **Install dependencies:**
    The web application's specific dependencies are listed in `web_app/requirements.txt`.
    ```bash
    pip install -r web_app/requirements.txt
    ```

5.  **Configure Google OAuth 2.0 Credentials:**
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Create a new project or select an existing one.
    *   In the navigation menu, go to "APIs & Services" > "Enabled APIs & services". Click "+ ENABLE APIS AND SERVICES" and search for "Gmail API". Enable it.
    *   Go back to "APIs & Services" > "Credentials".
    *   Click "+ CREATE CREDENTIALS" and select "OAuth client ID".
    *   For "Application type", choose "Web application".
    *   Give it a name (e.g., "GMail AutoLabel Web App").
    *   Under "Authorized redirect URIs", click "+ ADD URI" and enter:
        `http://localhost:5000/oauth2callback`
        *(This URI must match the `REDIRECT_URI` in `web_app/gmail_auth.py` and how your Flask app is run. If you deploy the app or change the port, update this accordingly.)*
    *   Click "CREATE". You will see a client ID and client secret. **Download the JSON file** provided.
    *   Rename the downloaded JSON file to `credentials.json`.
    *   Place this `credentials.json` file inside the `GMail_Auto_Label/web_app/` directory.

6.  **Configure User Information and Labels:**
    *   Create a new file named `user_info.json` inside the `GMail_Auto_Label/web_app/` directory.
    *   This file helps the AI understand your email preferences and defines the labels it can use. Here's an example structure:
      ```json
      {
          "user_info": "I am a software developer focusing on AI and machine learning projects. I prefer concise summaries of emails, highlighting key points and action items. Emails related to 'Project Gemini' are high priority and should be labeled as such. Newsletters or promotional content, unless directly related to core interests, can be considered for a 'LowPriority' or 'Archive' label.",
          "label_mapping": {
              "Project Gemini": "Critical project updates for Gemini",
              "AI Research": "Interesting papers and articles on AI",
              "Dev Community": "Updates from developer forums and communities",
              "Urgent": "Requires immediate attention",
              "LowPriority": "Can be reviewed later",
              "Archive": "To be archived"
          },
          "max_results": 15
      }
      ```
      *   `user_info`: A general description of your role, interests, and how you'd like emails to be processed.
      *   `label_mapping`: A dictionary where keys are the descriptive names for categories the AI will identify, and values are the actual Gmail label names you want to be applied (or created if they don't exist).
      *   `max_results`: The maximum number of recent emails to fetch and process in one go.

7.  **Set PaLM API Key (or equivalent Google AI Service Key):**
    *   Obtain your API key from [Google AI Studio (e.g., for PaLM models)](https://makersuite.google.com/app/apikey) or the relevant Google service providing access to large language models.
    *   Set this key as an environment variable named `PALM_API_KEY`.
      *   On **Linux/macOS**:
        ```bash
        export PALM_API_KEY="YOUR_API_KEY_HERE"
        ```
      *   On **Windows (Command Prompt)**:
        ```bash
        set PALM_API_KEY=YOUR_API_KEY_HERE
        ```
      *   On **Windows (PowerShell)**:
        ```powershell
        $env:PALM_API_KEY="YOUR_API_KEY_HERE"
        ```
      *(For these environment variable settings to persist, you might need to add them to your shell's profile file (e.g., `.bashrc`, `.zshrc`) or set them via system properties in Windows.)*

## Running the Application

1.  Ensure your virtual environment (e.g., `venv`) is activated.
2.  Make sure you are in the root directory of the project (`GMail_Auto_Label`).
3.  Run the Flask application:
    ```bash
    python -m web_app.app
    ```
    Alternatively, you can run:
    ```bash
    python web_app/app.py
    ```
4.  Open your web browser and navigate to: `http://localhost:5000`

## Usage

1.  On the application's home page, click the "Login with Google" button.
2.  You will be redirected to Google's authentication screen. Sign in with the Google account whose Gmail inbox you want to process. Grant the necessary permissions (to read and modify your emails for labeling).
3.  After successful authentication, you will be redirected back to the application.
4.  Click the "Start Processing Recent Emails" button.
5.  The application will fetch your recent emails, process them using the AI, and apply labels.
6.  You will be taken to a results page showing the outcome for each processed email.

## Security and Configuration Notes

*   The files `web_app/credentials.json` (your OAuth client secrets), `web_app/token.json` (your OAuth access/refresh tokens), and `web_app/user_info.json` (your personal email preferences) are sensitive.
*   These files are listed in the `.gitignore` file to prevent accidental commitment to the repository. Ensure they remain git-ignored if you clone or fork this project.

---

*Information regarding the previous local CLI application or Flutter frontend has been omitted from this README to focus on the current web application.*
