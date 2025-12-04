# Technical Infrastructure

This document outlines the technical infrastructure and deployment pipeline for the ChocoBot application.

## Overview

ChocoBot is a Python-based Discord bot containerized using Docker and hosted on Google Cloud Platform (GCP). The deployment process is automated using Google Cloud Build.

## Components

### 1. Docker Containerization
The application is containerized using Docker to ensure consistency across different environments.
- **Dockerfile**: Defines the runtime environment.
    - **Base Image**: `python:3.9-slim`
    - **Working Directory**: `/app`
    - **Dependencies**: Installed from `requirements.txt`
    - **Entrypoint**: Runs `python bot.py`
- **Build Arguments**: The `Dockerfile` accepts `DISCORD_BOT_TOKEN` as a build argument and sets it as an environment variable, allowing the bot to authenticate with Discord.

### 2. Continuous Integration & Deployment (CI/CD)
The CI/CD pipeline is defined in `cloudbuild.yaml` and is managed by Google Cloud Build.
- **Trigger**: The pipeline is typically triggered by a commit to the repository.
- **Steps**:
    1.  **Build**: Builds the Docker image `gcr.io/$PROJECT_ID/my-discord-bot` tagged with the commit short SHA (`$SHORT_SHA`).
    2.  **Tag**: Tags the same image as `latest` to ensure the most recent build is easily identifiable.
    3.  **Push**: Pushes both tags (`$SHORT_SHA` and `latest`) to the Google Container Registry (GCR).
    4.  **Deploy**: Resets the Compute Engine instance `instance-1` in the `us-central1-a` zone.
        - *Mechanism*: This reset triggers the VM to restart. It is assumed that the VM is configured (via a startup script or similar mechanism) to pull the `latest` Docker image from GCR and run the container upon boot.

### 3. Hosting (Google Compute Engine)
The bot runs on a Google Compute Engine (GCE) virtual machine.
- **Instance Name**: `instance-1`
- **Zone**: `us-central1-a`
- **Machine Type**: `e2-micro` (as referenced in `main.tf`)
- **Operating System**: Debian 12 (as referenced in `main.tf`)

### 4. Infrastructure as Code (Terraform)
The repository contains a `main.tf` file intended for managing the GCP infrastructure using Terraform.
- **Status**: The code in `main.tf` is currently commented out (`TODO: Integration with Terraform`).
- **Purpose**: It defines the provider configuration, the `google_compute_instance` resource, and necessary service account scopes. Once enabled, this will allow for reproducible and version-controlled infrastructure management.

## Deployment Workflow

1.  **Development**: Code changes are made and tested locally.
2.  **Commit**: Changes are committed and pushed to the repository.
3.  **Build Trigger**: Google Cloud Build detects the change and triggers the pipeline defined in `cloudbuild.yaml`.
4.  **Artifact Creation**: A new Docker image is built and pushed to GCR.
5.  **Deployment**: The GCE instance `instance-1` is reset.
6.  **Run**: Upon restart, the instance pulls the `latest` image and starts the bot.
