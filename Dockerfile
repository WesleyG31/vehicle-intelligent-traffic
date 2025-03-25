FROM python:3.10

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY . /app


COPY --chown=user ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN python -c "import easyocr; easyocr.Reader(['en'], gpu=False)"

COPY --chown=user . /app
CMD ["streamlit", "run", "streamlit_app.py", \
    "--server.port=7860", \
    "--server.address=0.0.0.0", \
    "--server.enableCORS=false", \
    "--server.enableXsrfProtection=false"]


