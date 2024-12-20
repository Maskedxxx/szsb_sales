FROM continuumio/miniconda3

COPY environment.yml .

RUN conda env create -p /env --file environment.yml && conda clean -afy

WORKDIR /app

COPY . .

ENTRYPOINT [ "conda", "run", "--no-capture-output", "-p", "/env",  "python", "-u", "app/main.py"]
