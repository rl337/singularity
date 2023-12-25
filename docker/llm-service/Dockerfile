FROM 0-singularity-base

ARG PROJECT_DIR
ARG CONFIG_DIR

RUN pip3 install fastapi uvicorn

RUN echo "PROJECT_DIR: ${PROJECT_DIR}"
RUN echo "CONFIG_DIR: ${CONFIG_DIR}"

# Copy your script and static files
COPY ${PROJECT_DIR}/app.py /app/app.py
COPY ${PROJECT_DIR}/static /app/static
COPY ${PROJECT_DIR}/drivers /app/drivers
COPY ${CONFIG_DIR} /app/config

# Expose port
EXPOSE 8000

# Run the application
ENTRYPOINT ["python3", "/app/app.py"]
