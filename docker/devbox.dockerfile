FROM python:3.14-bookworm

ARG _USER="columbo"
ARG _UID="1000"
ARG _GID="100"
ARG _SHELL="/bin/bash"

# Install uv system-wide for hatch to use as installer
ENV UV_NO_CACHE="true"
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    cp /root/.local/bin/uv /usr/local/bin/uv && \
    cp /root/.local/bin/uvx /usr/local/bin/uvx

RUN useradd -m -s "${_SHELL}" -N -u "${_UID}" "${_USER}"

ENV USER=${_USER}
ENV UID=${_UID}
ENV GID=${_GID}
ENV HOME=/home/${_USER}
ENV PATH="${HOME}/.local/bin/:${PATH}"
ENV PIP_NO_CACHE_DIR="true"


RUN mkdir /app && chown ${UID}:${GID} /app

USER ${_USER}

COPY --chown=${UID}:${GID} ./requirements-bootstrap.txt ./pyproject.toml /app/
WORKDIR /app

RUN pip install -r requirements-bootstrap.txt

COPY --chown=${UID}:${GID} . /app/
RUN hatch --verbose env create && \
    hatch --verbose env create bump && \
    hatch --verbose env create docs

CMD bash
