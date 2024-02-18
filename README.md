# MNIST Application

This application is a full-stack project that uses a React frontend and a Python Flask backend. It's designed to work with the MNIST dataset.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python
- Node.js and npm

### Set up separated environment (to avoid any conflict)

- Create new environment using python: `python -m venv <name>`
- Ex: `python -m venv testing_env`

### Installing

1. Clone the repository: `git clone https://github.com/username/mnist_app.git`
2. Navigate to the project directory: `cd mnist_app`

#### Backend

1. Navigate to the backend directory: `cd backend`
2. Install Python dependencies: `pip install -r requirement.txt`

#### Frontend

1. Navigate to the frontend directory: `cd ../frontend`
2. Install Node.js dependencies: `npm --force install `
3. Install package: `frontend\run_dependencies.sh`

### Running the Application

#### Backend

1. Run the Flask application: `python app.py`

#### Frontend

1. Run the React application: `npm start`

## Built With

- [React](https://reactjs.org/) - The web framework used
- [Flask](https://flask.palletsprojects.com/) - The backend framework used
- [Socket.IO](https://socket.io/) - Used for real-time communication between the client and the server

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
