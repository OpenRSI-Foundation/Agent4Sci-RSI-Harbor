# CPU-only contract test. This is NOT any benchmark's scientific environment.
FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends sudo \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash agent \
    && useradd --create-home --shell /bin/bash a4sci-judge \
    && ln -s /usr/local/bin/python3 /usr/bin/python3
COPY adapter/ /opt/adapter/
COPY catalog.json /fixtures/catalog.json
COPY checks/runtime/ /fixtures/
COPY adapter/candidate_exec.py /usr/local/bin/agent4sci-candidate
RUN chmod 0755 /usr/local/bin/agent4sci-candidate /fixtures/fake_claude.py \
    && printf '%s\n' 'a4sci-judge ALL=(root) NOPASSWD: /usr/local/bin/agent4sci-candidate *' > /etc/sudoers.d/agent4sci-judge \
    && chmod 0440 /etc/sudoers.d/agent4sci-judge \
    && mkdir -p /opt/agent4sci /logs /results \
    && printf '%s\n' /fixtures/fake_claude.py > /opt/agent4sci/claude-path \
    && python3 /fixtures/prepare.py \
    && mv /fixtures/workspace /workspace \
    && mv /fixtures/trajectory /logs/agent \
    && cp /fixtures/huggingface_hub.py /opt/adapter/huggingface_hub.py
ENV PYTHONDONTWRITEBYTECODE=1
CMD ["python3", "/fixtures/smoke.py"]
