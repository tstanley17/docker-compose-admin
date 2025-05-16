# docker-compose-admin

Docker Compose Manager Overview

Introduction

Docker Compose Manager is a user-friendly, web-based application designed to simplify the management of Docker Compose files and stacks. Built with Flask and styled with Tailwind CSS, this tool provides an intuitive interface for developers and system administrators to organize, edit, and control Docker Compose environments efficiently. Whether you're managing a single project or multiple stacks across complex directory structures, Docker Compose Manager streamlines your workflow with powerful features and a modern design.

Key Features

Recursive Compose File Discovery





Effortless File Detection: Specify a root directory, and Docker Compose Manager will recursively search for docker-compose.yml and docker-compose.yaml files, ensuring no stack is overlooked.



Organized Display: View all discovered compose files in a clean, tabular format, complete with their relative directory paths and associated stack names for easy identification.

Comprehensive Stack Management





Start, Stop, and Pull: Control your Docker Compose stacks with one-click actions to start (up), stop (down), or pull the latest images (pull), directly from the web interface.



Real-Time Status: Monitor the status of containers within each stack, with color-coded indicators (running, exited, or other states) for quick insights.

In-Browser File Editing





Inline Editing: Modify docker-compose.yml files directly within the app using a responsive, auto-resizing textarea with a monospace font for code clarity.



Seamless Saving: Save changes instantly and return to the editor or navigate back to the main dashboard with ease.

Flexible Directory Navigation





Directory Selection: Set a working directory manually via a text input or use the integrated file browser to navigate and select a compose file interactively.



File Browser: Explore directories, view available docker-compose.yml or docker-compose.yaml files, and select a file to set its parent directory as the working context.

Modern and Responsive UI





Tailwind CSS Styling: Enjoy a sleek, responsive interface with card-based layouts, hover effects, and consistent typography, optimized for both desktop and mobile devices.



User-Friendly Design: Intuitive controls, clear feedback messages, and a polished look enhance the user experience, making stack management accessible to all skill levels.

Benefits





Time-Saving: Automate the discovery and management of compose files, reducing manual effort and minimizing errors.



Centralized Control: Manage all your Docker Compose stacks from a single interface, regardless of their location in the directory structure.



Accessibility: Edit and control stacks without leaving the browser, eliminating the need for command-line access or external editors.



Scalability: Handle small projects or large, nested directory structures with equal ease, thanks to recursive search and robust path handling.

Technical Details





Backend: Built with Flask, a lightweight Python web framework, ensuring fast performance and easy deployment.



Docker Integration: Leverages the python-docker library to interact with the Docker daemon, enabling seamless container and stack management.



Frontend: Uses Tailwind CSS (via CDN) for a modern, responsive UI without additional build steps.



Deployment: Packaged with a Dockerfile for easy containerization, running on port 5802 with Docker socket access for full functionality.

Use Cases





Developers: Quickly edit and test Docker Compose configurations during development workflows.



DevOps Teams: Centralize stack management across multiple projects or environments.



System Administrators: Monitor and control Docker Compose stacks without needing direct server access.



Learning Environments: Provide a beginner-friendly interface for students or new Docker users to explore compose files and stack operations.

Getting Started





Clone the Repository: Download the project files, including app.py, the templates directory, and the Dockerfile.



Build the Docker Image: Run docker build -t docker-compose-manager . to create the container image.



Run the Container: Launch the app with docker run -d -p 5802:5802 -v /var/run/docker.sock:/var/run/docker.sock docker-compose-manager.



Access the App: Open http://localhost:5802 in your browser, set a directory, and start managing your Docker Compose stacks.

Security Considerations





Docker Socket Access: The app requires access to /var/run/docker.sock for Docker operations. Use in trusted environments or implement socket proxies for production.



File Permissions: Ensure the specified directories are accessible to the container user to avoid file access errors.

Docker Compose Manager empowers you to take control of your Docker Compose workflows with a powerful, intuitive, and modern tool. Simplify your stack management today!
