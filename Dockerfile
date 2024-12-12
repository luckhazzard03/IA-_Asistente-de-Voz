FROM python:3.10

# Desactivar la verificación de versión de pip y configurar Python sin búfer
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt .

# Crear un entorno virtual y activar el entorno para instalar las dependencias
RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r requirements.txt

# -----------------------------------------------------------------
# Copy certificates to make use of free open ai usage within the lab
# REMOVE THIS WHEN DEPLOYING TO CODE ENGINE

# Copy the self-signed root CA certificate into the container
COPY certs/rootCA.crt /usr/local/share/ca-certificates/rootCA.crt

# Update the CA trust store to trust the self-signed certificate
RUN chmod 644 /usr/local/share/ca-certificates/rootCA.crt && \
    update-ca-certificates

# Set the environment variable OPENAI_API_KEY to empty string
ENV OPENAI_API_KEY=skills-network
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
# -----------------------------------------------------------------

# Verificar si el archivo de certificados se copió correctamente (opcional)
RUN ls -l /usr/local/share/ca-certificates/

# Exponer el puerto en el que la aplicación estará corriendo
EXPOSE 8000

# Comando para ejecutar la aplicación (asegurarse de que use el entorno virtual)
CMD ["/app/venv/bin/python", "server.py"]
