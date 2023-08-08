# fortigate-vpn-login

Uses `openconnect` to connect to Fortinet VPNs, with extra features. This was created because sometimes we don't want
to use the Forticlient program, or just want a background daemon working for us.

So why not use only `openconnect`? Because there's no proper SAML / OAuth2 support on it, so I decided to do a python
wrapper to extract the `SVPNCOOKIE` from the browser workflow and use it on `openconnect`.

## Usage

To configure this utility on an interactive mode, run:

```bash
fortigate-vpn-login --configure
```

To initiate the SAML workflow on a fortigate ssl vpn server:

```bash
fortigate-vpn-login -s https://vpn-server.example.com
```

To get help and more options:

```bash
fortigate-vpn-login -h
```

## Contents

- [ChangeLog](CHANGELOG.md)

## Setup and usage for local development

Make a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Note that this will also install the local dependencies, which might change after
some time. If needed, you can run `pip install -e .` again to reinstall the
updated dependencies anytime.
