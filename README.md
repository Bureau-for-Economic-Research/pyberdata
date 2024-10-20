
# pyberdata <img src="man/figures/logo.png" align="right" alt="" width="120" />

[<img
src="https://img.shields.io/badge/lifecycle-experimental-orange.svg"
class="quarto-discovered-preview-image" alt="Lifecycle: experimental" />](https://www.tidyverse.org/lifecycle/#experimental)
[![](https://img.shields.io/github/last-commit/Bureau-for-Economic-Research/berdata.svg)](https://github.com/Bureau-for-Economic-Research/pyberdata/commits/develop)

The
[pyberdata](https://github.com/Bureau-for-Economic-Research/pyberdata)
library is a *basic* wrapper around the [Data Playground
Portal](https://dataplayground.beranalytics.co.za/) API from BER
maintained by the [Bureau for Economic
Research](https://www.ber.ac.za/home/).

This is the homepage for the {pyberdata} python package
<https://github.com/Bureau-for-Economic-Research/pyberdata>. If you are
looking for the R version, it can be found here: {berdata} R package
<https://github.com/Bureau-for-Economic-Research/berdata>.

**NOTE:** The API is currently in *BETA* testing.

## Disclaimer

This package was developed at the [Bureau for Economic
Research](https://www.ber.ac.za/home/) in order to streamline research
processes and allow automation for its internal research.

## About BER

The Bureau for Economic Research (BER) is one of the oldest economic
research institutes in South Africa. It was established in 1944 and is
part of the Faculty of Economic and Management Sciences (EMS) at
Stellenbosch University. Over the years, the BER has built a local and
international reputation for independent, objective and authoritative
economic research and forecasting.

## Create an environment

``` bash
mkdir ~/venv && cd ~/venv
python3 -m venv pyberdata
source ~/venv/pyberdata/bin/activate
```

## Installation from Github

Clone the repo from Github:

``` bash
pip install git+https://github.com/Bureau-for-Economic-Research/pyberdata
```

## Usage

### Set API Key

To access the API you’ll need to first specify an API key in your `.env`
key as provided to you by [BER](https://www.ber.ac.za).

- `.env`

``` txt
BERDATA_API=place_your_key_here
```

After setting the API key in `.env`

- In python

``` python
from decouple import config

print(config("BERDATA_API"))
```

### The API interface

The package currently provides an interface to the [Data Playground
Portal](https://dataplayground.beranalytics.co.za/) API. The package is
designed around the `BERClient` class. The attributes are:

- `apikey`
  - Specify the API provided to you by the BER

The main method `get_data` has the following options:

- `time_series_code` time series code to return: `KBP7096B`

- `output_format`

  - Should output be a nested `{polars}` data frame, `{dict}` or
    `{json}`

``` python
import logging
from decouple import config
from pyberdata import BERClient
from pkg_resources import get_distribution


def setup_logger():
    # create logger
    logger = logging.getLogger("pyberdata")
    logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.INFO)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)


def main():
    setup_logger()
    print(get_distribution("pyberdata").version)
    client = BERClient(apikey = config("BERDATA_API"))
    time_series_code = ["KBP7096B", "KBP7008Q", "KBP7203M"]
    out = client.get_data(time_series_code, output_format = "codes")
    out = client.get_data(time_series_code, output_format = "names")

    # Experimental
    out = client.get_data(time_series_code, output_format = "nested")

    return out


if __name__ == "__main__" and __package__ is None:
    print(f"Main name is {__name__}")
    main()
```
