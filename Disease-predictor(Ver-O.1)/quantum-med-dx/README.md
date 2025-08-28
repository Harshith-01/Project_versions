# Quantum Med DX

Quantum Med DX is a project that integrates quantum computing techniques with medical data processing and analysis. This repository contains both backend and frontend components designed to work together to provide a seamless experience for users.

## Project Structure

The project is organized into two main directories: `backend` and `frontend`.

### Backend

The backend is responsible for handling data ingestion, processing, and serving API endpoints. It includes the following files:

- **app.py**: Main entry point for the backend application. Initializes the web server and sets up routes and middleware.
- **ingest.py**: Functions for ingesting data from various sources, processing it, and storing it for further use.
- **quantum.py**: Functions and classes related to quantum computing processes and algorithms relevant to the application.
- **rag.py**: Implements retrieval-augmented generation techniques to enhance model responses with external data.
- **llm.py**: Functions and classes for working with large language models, including loading models and generating text.
- **utils.py**: Utility functions used across the backend application, such as data formatting and logging.
- **schemas.py**: Data schemas for validation and serialization using libraries like Pydantic or Marshmallow.
- **config.py**: Configuration settings for the application, including API keys and database URLs.
- **requirements.txt**: Lists the Python dependencies required for the backend application.
- **.env.example**: Example of environment variables needed for the application.
- **data/sources.yaml**: Configuration for data sources, specifying how to connect and retrieve data.
- **data/docs_raw/**: Directory for storing downloaded pages or raw documents (optional).

### Frontend

The frontend is built using React and is responsible for the user interface. It includes the following files:

- **index.html**: Main HTML file for the frontend application.
- **package.json**: Configuration file for npm, listing dependencies and scripts.
- **postcss.config.cjs**: Configuration settings for PostCSS.
- **tailwind.config.cjs**: Configuration file for Tailwind CSS.
- **vite.config.js**: Configuration settings for Vite, the build tool.
- **src/main.jsx**: Entry point for the React application.
- **src/App.jsx**: Main application component containing the structure and logic of the frontend.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/quantum-med-dx.git
   cd quantum-med-dx
   ```

2. **Backend Setup**:
   - Navigate to the `backend` directory.
   - Create a virtual environment and activate it:
     ```
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
   - Install the required dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Copy `.env.example` to `.env` and fill in the necessary environment variables.

3. **Frontend Setup**:
   - Navigate to the `frontend` directory.
   - Install the frontend dependencies:
     ```
     npm install
     ```

4. **Running the Application**:
   - Start the backend server:
     ```
     python app.py
     ```
   - Start the frontend development server:
     ```
     npm run dev
     ```

## Usage

Once both the backend and frontend servers are running, you can access the application in your web browser at `http://localhost:3000` (or the port specified by your frontend configuration).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.