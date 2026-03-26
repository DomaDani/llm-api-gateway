FROM python:3.14
WORKDIR /app

RUN useradd -m mupstream
ENV PATH="/home/mupstream/.local/bin:${PATH}"

COPY tests/requirements.txt ./
USER mupstream

RUN python -m pip install --no-cache-dir --user -r requirements.txt

COPY --chown=mupstream:mupstream tests/fixtures ./tests/fixtures
COPY --chown=mupstream:mupstream tests/tools/ ./tests/tools

EXPOSE 8081

CMD ["python", "-m", "tests.tools.mock_upstream"]