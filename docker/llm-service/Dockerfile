FROM 0-singularity-base

ARG PROJECT_DIR
ARG CONFIG_DIR
ARG TYPEA_DIR

RUN pip3 install fastapi uvicorn

RUN echo "PROJECT_DIR: ${PROJECT_DIR}"
RUN echo "CONFIG_DIR: ${CONFIG_DIR}"
RUN echo "TYPEA_DIR: ${TYPEA_DIR}"

# Copy your script and static files
COPY ${PROJECT_DIR}/static /app/static
COPY ${CONFIG_DIR} /app/config
COPY ${TYPEA_DIR} /type_a

RUN pip3 install /type_a

# Expose port
EXPOSE 8000

# Run the application
ENTRYPOINT ["llm-service"]
