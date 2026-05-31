FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt numba

# Copy miner files
COPY gpu_miner.py /app/gpu_miner.py
COPY satoshi_miner.py /app/satoshi_miner.py
COPY config.yaml /app/config.yaml
COPY keccak_pow.c /app/keccak_pow.c
COPY setup.py /app/setup.py

# Try to build C extension (optional, fallback to Python)
WORKDIR /app
RUN python3 setup.py build_ext --inplace 2>/dev/null || true

# Run the GPU miner in standalone mode (headless, no GUI)
CMD ["python3", "/app/gpu_miner.py"]
