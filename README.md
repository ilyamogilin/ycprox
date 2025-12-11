# ycprox

A tool for deploying a forward proxy in your Yandex Cloud infrastructure to change your IP address (almost) each request.

[Ru version of docs](https://github.com/chlzen/ycprox/blob/main/docs/README_RU.md)

## Features
- All HTTP(S) methods supported
- All parameters and URI's are passed through
- Spoof X-Forwarded-For source IP header by requesting with an X-My-X-Forwarded-For header (thanks [fireprox](https://github.com/ustayready/fireprox/) for the feature!)
- Rotates IP address with (almost) every request (needs proper testing actually)

## How it works

ycprox similar to [fireprox](https://github.com/ustayready/fireprox/) creates API Gateway in cloud, but also spins up a Cloud Function to control output headers of the request.

```
Client → API Gateway → Cloud Function → Your destination service IP
```

The proxy preserves headers, query parameters, and request bodies while filtering out internal Yandex Cloud headers.

## Requirements

- Python >= 3.11
- (optional) [uv](https://docs.astral.sh/uv/) package manager or generate separate virtualenv
- Yandex Cloud account with created cloud and folder (you can use default ones)

## Quick start

```bash
# Clone the repo
git clone https://github.com/chlzen/ycprox.git
cd ycprox

# Optional creating of venv
# python -m venv ycproxenv
# source ycproxenv/bin/activate

# Install via pip
pip install .

# Authenticate with Yandex OAuth token
ycprox auth init

# Deploy proxy to your service in folder be4dfadewdlksjedde 
# Copy folder id from Yandex Cloud console, default is ok
ycprox proxy up --url https://example-service.com --folder-id be4dfadewdlksjedde

# View proxy info
ycprox proxy info

# Make your requests to proxy
curl "https://kekkekkekkek.lmao.apigw.yandexcloud.net/"

# Tear down when done
ycprox proxy down
```

## Commands

### Authentication

| Command | Description |
|---------|-------------|
| `ycprox auth init` | Get Yandex OAuth token and save it to keyring |
| `ycprox auth reset` | Remove saved OAuth token from keyring |

### Proxy management

`ycprox proxy up`

Deploy proxy gateway setup to Yandex Cloud.

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--url` | Yes | — | URL of the destination service to proxy requests to |
| `--folder-id` | Yes | — | Yandex Cloud folder ID to deploy resources |
| `--gw-name` | No | `ycprox-gateway` | Name of the API Gateway |
| `--cf-name` | No | `ycprox-function` | Name of the Cloud Function |

`ycprox proxy info`

Shows info about your current proxy.

`ycprox proxy down`

Deletes your proxy installation from cloud.

## Optional environment variables

All environment variables use the `YCPROX_` prefix. You can also use a `.env` file in your working directory.

| Variable | Description | Default |
|----------|-------------|---------|
| `YCPROX_UA_STRING` | Custom User-Agent string for API requests | `ycprox/{version}` |

## Disclamer
- Currently ycprox supports **only one proxy deployment at a time**
- Use of this tool on systems other than those that you own are likely to violate the [Terms of Use for Yandex.Cloud Platform Services](https://yandex.ru/legal/cloud_termsofuse/) and could potentially lead to termination or suspension of your Yandex Cloud account. Further, even use of this tool on systems that you do own, or have explicit permission to perform penetration testing on, is subject to the [Acceptable Use Policy for the Yandex.Cloud Platform Services](https://yandex.ru/legal/cloud_aup/).
- This software is provided as is, without any guarantees, and you use it at your own risk