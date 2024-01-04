FROM 0-singularity-base

ARG PROJECT_DIR
ARG CONFIG_DIR

RUN echo "PROJECT_DIR: ${PROJECT_DIR}"
RUN echo "CONFIG_DIR: ${CONFIG_DIR}"

# Copy your script and static files
COPY ${PROJECT_DIR}/app.py /app/app.py
COPY ${CONFIG_DIR} /app/config

# Run the application
ENTRYPOINT ["python3", "/app/app.py"]
