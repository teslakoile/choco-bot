# ChocoBot

## Overview
ChocoBot is a Discord bot designed to notify a specific user in a channel about new YouTube comments on a designated channel's videos every 4 hours. If comments are found, it notifies the user and displays a list of comments, specifying the video, the user who made the comment, and the time the comment was made. If no new comments are found, it simply indicates that no new comments were detected.

## Features
- **Notification System**: Notifies a user every 4 hours about new YouTube comments.
- **Comment Tracking**: Lists new comments with details including the video title, commenter's username, and the time of the comment.
- **No Comment Alert**: Informs users when no new comments are found during a check.

## How it Works
### `YouTube API Integration`
- ChocoBot leverages the YouTube Data API to fetch comments from specified channel videos. It periodically polls the YouTube API to retrieve new comments posted on the videos, employing efficient data handling to process and filter comments based on their timestamps.

### `Discord API Integration`
- Utilizing the Discord API, ChocoBot communicates within a Discord channel, sending notifications and messages. It dynamically constructs messages that include new comment details and sends them to the designated channel, ensuring users are promptly informed about new interactions on their YouTube content.

## Infrastructure
- **Continuous Integration/Continuous Deployment (CI/CD)**: Integrated with Cloud Build for CI/CD to automate the deployment process. The integration of CI/CD with Cloud Build facilitates continuous updates and deployment, enhancing the bot's reliability and performance.
- **Hosting**: Hosted on GCP Compute Engine, ChocoBot benefits from a scalable infrastructure that can handle varying loads efficiently.
- **Containerization**: With a Dockerfile included, ChocoBot is containerized, which simplifies deployment and version control. This containerization approach ensures consistent environments across development and production, reducing discrepancies and potential deployment issues.


## Setup and Configuration
To set up and configure ChocoBot, follow these steps:

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/teslakoile/choco-bot.git
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the bot:
    ```bash
    python bot.py
    ```

## Contributing

Thank you for considering contributing to the ChocoBot repository! We welcome any contributions that can help improve the bot and make it even better.

To contribute, please follow these guidelines:

### Submitting Issues
If you encounter any bugs, have questions, or would like to suggest new features, please submit an issue on the [ChocoBot GitHub repository](https://github.com/teslakoile/choco-bot/issues). When submitting an issue, please provide as much detail as possible, including steps to reproduce the problem and any relevant error messages.

### Pull Requests
We also encourage you to submit pull requests for bug fixes, enhancements, or new features. To submit a pull request, follow these steps:

1. Fork the ChocoBot repository to your own GitHub account.
2. Create a new branch for your changes.
3. Make your changes and commit them to your branch.
4. Push your branch to your forked repository.
5. Open a pull request on the [ChocoBot GitHub repository](https://github.com/teslakoile/choco-bot/pulls) and provide a detailed description of your changes.

We will review your pull request and provide feedback. Once your changes are approved, they will be merged into the main repository.

Thank you for your contributions and helping make ChocoBot better!

