# Quantum Med DX

Quantum Med DX is a comprehensive application designed to assist in medical diagnosis and data management. This project is structured into three main components: backend, data, and frontend.

## Project Structure

- **backend/**: Contains the server-side application, including all necessary scripts and configurations.
- **data/**: Holds data storage directories for runtime-generated data and source notes.
- **frontend/**: Comprises the client-side application built with React, providing a user-friendly interface.

## Setup Instructions

### Backend

1. Navigate to the `backend` directory.
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Configure your environment variables by copying `.env.example` to `.env` and filling in the necessary values.
4. Run the application:
   ```
   python app.py
   ```

### Frontend

1. Navigate to the `frontend` directory.
2. Install the required npm packages:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```

## Usage

Once both the backend and frontend are running, you can access the application through your web browser. The frontend will communicate with the backend to provide a seamless user experience for medical diagnosis and data management.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.