# GTmetrix to BigQuery

![repo status: WIP](https://img.shields.io/badge/repo%20status-WIP-yellow)
[![license: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

>A script running browser test of specified urls through GTmetrix and saving metrics in BigQuery.

## Project Status

Alpha, everything is subject to change.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Background

## Install

```bash
$ docker pull t3nde/gtmetrix-bq
```

## Usage

```bash
# copy example config and edit
$ cp example-config.yaml config.yaml; vim config.yaml
$ docker run t3nde/gtmetrix-bq -v ${PWD}/config.yaml:/app/config.yaml --env GTMETRIX_REST_API_EMAIL=<email> --env GTMETRIX_REST_API_KEY=<key> t3nde/gtmetrix-bq
```

## Contributing

PRs accepted.

Small note: If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

[MIT](LICENSE)
