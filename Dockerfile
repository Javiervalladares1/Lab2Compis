# Imagen base con Python 3 (necesario para el runtime de ANTLR y los drivers)
FROM python:3.11-slim

# Java es necesario para ejecutar la herramienta ANTLR,
# que es la que genera el lexer, el parser, el visitor y el listener
# a partir de la gramática .g4
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jre-headless curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Descarga del JAR oficial de ANTLR 4.13.2
RUN curl -fsSL -o /usr/local/lib/antlr-4.13.2-complete.jar \
    https://www.antlr.org/download/antlr-4.13.2-complete.jar

# Runtime de ANTLR para Python 3.
# IMPORTANTE: la versión del runtime debe coincidir con la versión del JAR.
RUN pip install --no-cache-dir antlr4-python3-runtime==4.13.2

# Se crea el comando `antlr` para poder escribir:
#   antlr -Dlanguage=Python3 -visitor SimpleLang.g4
# en lugar de invocar el JAR de Java manualmente.
RUN printf '#!/bin/sh\nexec java -jar /usr/local/lib/antlr-4.13.2-complete.jar "$@"\n' \
    > /usr/local/bin/antlr && chmod +x /usr/local/bin/antlr

# Directorio de trabajo: aquí se monta la carpeta ./program del host
WORKDIR /program

# Al entrar al contenedor se abre una terminal bash
CMD ["/bin/bash"]
