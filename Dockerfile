FROM continuumio/miniconda3

COPY environment.yml .

RUN conda env create -p /env --file environment.yml && conda clean -afy

WORKDIR /app

COPY . .

ENTRYPOINT [ "conda", "run", "-p", "/env",  "python", "app/main.py"]
