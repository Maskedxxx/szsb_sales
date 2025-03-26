FROM continuumio/miniconda3

COPY environment.yml .

RUN conda env create -p /env --file environment.yml && conda clean -afy

WORKDIR /app

COPY ./app .

ENTRYPOINT [ "conda", "run", "--no-capture-output", "-p", "/env",  "python", "-u", "main.py"]
