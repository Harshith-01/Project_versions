# Medical Diagnosis AI

This project is a medical diagnosis application that leverages advanced techniques, including quantum computing and language models, to assist in diagnosing medical conditions. The application is structured into a backend and a frontend, each serving distinct purposes.

## Project Structure

```
medical-diagnosis-ai
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── models
│   │   │   └── pydantic_models.py
│   │   └── services
│   │       ├── diagnosis_service.py
│   │       ├── ingestion_service.py
│   │       ├── llm_service.py
│   │       ├── quantum_service.py
│   │       └── retrieval_service.py
│   ├── scripts
│   │   └── ingest_data.py
│   ├── data
│   │   └── knowledge_base.json
│   ├── .env
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend
│   ├── public
│   ├── src
│   │   ├── App.css
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## Backend

The backend is responsible for processing requests, managing data, and implementing the core logic of the application. It is built using Python and includes the following components:

- **app**: Contains the main application logic, including routes and services.
- **services**: Implements various functionalities such as diagnosis, data ingestion, and quantum computing.
- **scripts**: Contains scripts for data ingestion.
- **data**: Holds the knowledge base in JSON format.
- **.env**: Stores environment variables.
- **config.py**: Configuration settings for the application.
- **requirements.txt**: Lists the required Python packages.
- **run.py**: Entry point to start the backend server.

## Frontend

The frontend is built using React and provides a user interface for interacting with the backend. It includes:

- **public**: Contains static assets.
- **src**: Contains the main application code, including styles and components.
- **package.json**: Configuration file for npm.
- **tailwind.config.js**: Configuration for Tailwind CSS.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/medical-diagnosis-ai.git
   cd medical-diagnosis-ai
   ```

2. Set up the backend:
   - Navigate to the `backend` directory.
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Create a `.env` file with the necessary environment variables.

3. Run the backend:
   ```
   python run.py
   ```

4. Set up the frontend:
   - Navigate to the `frontend` directory.
   - Install dependencies:
     ```
     npm install
     ```
   - Start the frontend:
     ```
     npm start
     ```

## Usage

Once both the backend and frontend are running, you can access the application through your web browser. The frontend will communicate with the backend to provide diagnosis assistance based on the input data.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.