# Vulnerability Management Application

## Overview

This application is designed to manage vulnerabilities and devices associated with different profiles. It allows users to add, search, and manage vulnerabilities and devices through a graphical user interface (GUI) built with Tkinter.

## Features

- **Profile Management**: Add and manage profiles.
- **Device Management**: Add and manage devices associated with profiles.
- **Vulnerability Management**: Add and manage vulnerabilities associated with profiles.
- **Search Functionality**: Search for devices and vulnerabilities within profiles.
- **GUI**: User-friendly interface for managing profiles, devices, and vulnerabilities.

## Requirements

- Python 3.x
- Tkinter
- `ttk` module for themed widgets
- `messagebox` for displaying messages

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. Use the GUI to manage profiles, devices, and vulnerabilities.

## Code Structure

- `main.py`: Entry point of the application.
- `controllers/`: Contains the controller classes for managing profiles, devices, and vulnerabilities.
- `views/`: Contains the view classes for the GUI components.
- `models/`: Contains the model classes for the data structures.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

