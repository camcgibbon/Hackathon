# LeanTaaS Hackathon

## Overview

This repository contains code for a Flask application developed during a LeanTaaS Hackathon. The application was designed to parse and analyze code, extracting function blocks and dynaically generating a PDF report with descriptions by interacting with the OpenAI GPT API.

## Structure

- **[app.py]** The main application file where the Flask app is defined and routes are set up.
- **[parser.py]** Contains logic to parse and analyze code, extracting function blocks.
- **[requirements.txt]** Lists the dependencies required to run the application.
- **[static/styles.css]** CSS file to style the application.
- **[templates/index.html]** HTML template for the application’s interface.

## Setup and Running

1. **Install Dependencies:**
   ```bash
   pip install -r hack-a-thon/requirements.txt
   ```
2. **Run the Application:**

```bash
python3 flask run
```
Access the application at locally at http://127.0.0.1:5000/ (or whichever port your computer defaults to)

## Functionality

The application takes code from any source as a input, parses the code to extract function blocks, and generates a pre-formatted PDF document with descriptions and analysis for the code, providing easy and efficient code documentation

