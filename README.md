# PagerDuty API

[![Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/91nunocosta/python-package-cookiecutter/releases/tag/v0.10.1)

PagerDuty client API for the interview.

## Installation

```bash
pip install pagerduty
```

## Usage

```python
>>> from pagerduty import PagerDutyClient
>>> import os
>>> client = PagerDutyClient(auth_token=os.environ["PAGERDUTY_TOKEN"])
>>> client.test_ability("teams")
True

```

For more details, read the
[documentation](https://91nunocosta.github.io/pagerduty/pagerduty.html).

## Contributing

Please read the [contributing guidelines](./CONTRIBUTING.md).
