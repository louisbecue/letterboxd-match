# Letterboxd Comparison Project

This project is a web application that allows users to compare their Letterboxd profiles and receive a compatibility score along with movie recommendations based on their watched movies.

## Features

- Compare two Letterboxd users
- Calculate compatibility score based on watched movies
- Provide movie recommendations based on user preferences
- User-friendly web interface

## Project Structure

```
letterboxd-comparison
├── src
│   ├── app.py                  # Entry point of the application
│   ├── models
│   │   ├── __init__.py         # Initializes the models package
│   │   └── user.py             # Defines the User class
│   ├── services
│   │   ├── __init__.py         # Initializes the services package
│   │   ├── letterboxd_api.py   # Interacts with the Letterboxd API
│   │   ├── compatibility_calculator.py # Calculates compatibility score
│   │   └── recommendation_engine.py    # Generates movie recommendations
│   ├── routes
│   │   ├── __init__.py         # Initializes the routes package
│   │   ├── compare.py           # Route for comparing users
│   │   └── recommendations.py    # Route for fetching recommendations
│   └── utils
│       ├── __init__.py         # Initializes the utils package
│       └── data_processor.py    # Utility functions for data processing
├── static
│   ├── css
│   │   └── style.css            # CSS styles for the web application
│   └── js
│       └── app.js               # JavaScript for client-side functionality
├── templates
│   ├── index.html               # Main landing page
│   ├── compare.html             # User comparison page
│   └── results.html             # Displays comparison results and recommendations
├── requirements.txt             # Python dependencies
├── config.py                    # Configuration settings
└── README.md                    # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/letterboxd-comparison.git
   cd letterboxd-comparison
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your API keys in `config.py`.

## Usage

1. Run the application:
   ```
   python src/app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Use the interface to compare two Letterboxd users and view the compatibility score and recommendations.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.