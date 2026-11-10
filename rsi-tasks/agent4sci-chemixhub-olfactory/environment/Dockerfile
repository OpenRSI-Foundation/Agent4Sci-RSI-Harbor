FROM ghcr.io/maszhongming/agent4sci-chemixhub@sha256:fe2ce412dfe8831b892fe8d6c916848a657cc4f3693d13385b3fb0a50dd93f55
USER root
COPY spec.json instruction.md bootstrap.py data.py /opt/agent4sci/
COPY candidate_exec.py /usr/local/bin/agent4sci-candidate
RUN npm install --prefix /opt/agent4sci/judge-cli --no-audit --no-fund @anthropic-ai/claude-code@2.1.322 \
    && useradd --create-home --shell /bin/bash a4sci-judge \
    && chmod 0755 /usr/local/bin/agent4sci-candidate \
    && printf '%s\n' 'a4sci-judge ALL=(root) NOPASSWD: /usr/local/bin/agent4sci-candidate *' > /etc/sudoers.d/agent4sci-judge \
    && chmod 0440 /etc/sudoers.d/agent4sci-judge \
    && /usr/bin/python3 -I /opt/agent4sci/bootstrap.py
ENV PYTHONDONTWRITEBYTECODE=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /workspace
USER agent
ENTRYPOINT []
CMD ["sleep", "infinity"]
