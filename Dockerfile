# Stage 1: Builder - Install dependencies and the project into a virtual environment
FROM python:3.13-slim as builder

# Install uv, our package installer
RUN pip install uv

# Set the working directory
WORKDIR /app

# Set the PATH to include the future virtual environment's binaries
ENV PATH="/app/.venv/bin:$PATH"

# Create a virtual environment
RUN uv venv .venv

# Copy project configuration and source code
COPY pyproject.toml ./
COPY src ./src

# Install all dependencies and the project itself into the virtual environment
# This benefits from Docker caching. If pyproject.toml and src don't change,
# this layer won't be rebuilt.
RUN uv pip install .


# Stage 2: Final - Create the final, lean production image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Create a non-root user for security and switch to it
RUN useradd --create-home appuser
USER appuser

# Copy the populated virtual environment from the builder stage.
# This contains our code and all its dependencies.
COPY --from=builder --chown=appuser:appuser /app/.venv ./.venv

# Set the PATH to include the virtual environment's binaries for the new stage
ENV PATH="/app/.venv/bin:$PATH"

# Set default environment variables for the server
# The server will listen on all network interfaces inside the container
ENV HOST=0.0.0.0
ENV PORT=8000
# Define a default path for the git repository inside the container.
# It is recommended to mount a local directory to this path when running.
ENV GIT_REPO_PATH=/repo

# Expose the port the server will run on
EXPOSE 8000

# The command to run the application using the script defined in pyproject.toml
# This is the idiomatic way to run an installed Python application.
CMD ["git-mcp-server"] 