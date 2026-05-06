# Expo Push Test Target

[![Docker Publish (GHCR)](https://github.com/expopush/test-target/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/expopush/test-target/actions/workflows/docker-publish.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python)](https://www.python.org/downloads/)
[![Multi-Arch](https://img.shields.io/badge/Platform-linux/amd64%20%7C%20linux/arm64-lightgrey)](https://github.com/expopush/test-target/pkgs/container/test-target)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen.svg?logo=dependabot)](https://github.com/expopush/test-target/network/updates)

A Python-based testing utility and Docker container used to simulate client interactions and verify the end-to-end flow of the Expo Push system.

## Getting Started

### Run with Docker

The easiest way to use the test target is via the official Docker image:

```bash
docker pull ghcr.io/expopush/test-target:latest
docker run -p 8080:8080 ghcr.io/expopush/test-target:latest
```

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```

## Integration

The test target interacts with the [Expo Push Test Harnesses](https://github.com/expopush/test-harnesses) to trigger notifications and validate that they arrive at the intended destination with the correct payload.

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

---

**Disclaimer**: This project is an independent, open-source work and is not affiliated with, endorsed by, or sponsored by 650 Industries, Inc. or the official Expo project. "Expo" is a trademark of 650 Industries, Inc.
