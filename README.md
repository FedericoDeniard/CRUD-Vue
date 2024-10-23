# How to run the project

## Backend

It's built on Python using Flask.

To access the backend, first navigate to the backend directory:

- `cd backend/`

- Next, install the dependencies (it is recommended to create a virtual environment):
  - On **Linux**:
    - Create the virtual environment:
      - `python3 -m venv myenv`
    - Activate the virtual environment:
      - `source myenv/bin/activate`
  - On **Windows**:
    - Create the virtual environment:
      - `python -m venv myenv`
    - Activate the virtual environment:
      - `myenv\Scripts\activate`
  - On **macOS**:
    - Create the virtual environment:
      - `python3 -m venv myenv`
    - Activate the virtual environment:
      - `source myenv/bin/activate`
- After activating the virtual environment, install the project dependencies:

  - `pip install -r requirements.txt`

- Set up environment variables:

  - Create a `.env` file in the backend directory containing the following key:
    - `DATABASE_URI=**(Insert your database URL for connection)**`

- Upload users from a file (optional):
  - On **Linux/macOS**:
    - `python3 parser.py`
  - On **Windows**:
    - If you're in a virtual environment:
      - `python parser.py`
    - If not, you can also use:
      - `py parser.py`
- To run the project, use the following command:
  - `flask run --debug --port=3000`

## Frontend

It's built on JavaScript using Vue3 and Bootstrap.

To access the frontend, first navigate to the directory:

- `cd frontend/` (This command is the same on Windows, macOS, and Linux)

- Next, set up the environment variables:

  - Create a `.env` file in the frontend directory containing the following key:
    - `VITE_API_URL="http://localhost:3000"` (By default, this is the port used by the backend, but you can change it if needed)

- Then, install the dependencies:

  - `npm install`

- Run the project:
  - `npm run dev`
