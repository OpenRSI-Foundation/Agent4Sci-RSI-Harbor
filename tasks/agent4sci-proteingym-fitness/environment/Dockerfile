FROM ghcr.io/maszhongming/agent4sci-proteingym@sha256:e26305539be83948826900982227170e75c8cd21385d7242d13dd7d0cac918a6
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
