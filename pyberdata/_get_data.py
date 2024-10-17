import requests
import logging
import polars as pl
from typing import Union
import time
import json

log = logging.getLogger(__name__)


def get_data(self, time_series_code: str, output_format: str = "names") -> pl.DataFrame:
    """
    Fetch data from BER's DataPlayground API.

    Parameters
    ----------
    time_series_code : str
        Code representing the time series to be fetched.
    output_format : str
        Should output be a nested `{polars}` data frame, `{dict}`

    Returns
    -------
    polars.DataFrame
        The data fetched is in polars DataFrame format.

    Raises
    ------
    HTTPError
        If there's an HTTP error in the request.
    """

    start_time = time.time()

    url = "https://api.beranalytics.co.za/"

    payload_dict = {
            "data": time_series_code,
            "interface": self.interface,
            "platform": self.platform,
            "apikey": self.apikey,
        }

    payload_dict.popitem()
    payload = json.dumps(payload_dict)
    log.debug(f"Querying with parameters: [{payload}]")

    payload_dict = {
            "data": time_series_code,
            "interface": self.interface,
            "platform": self.platform,
            "apikey": self.apikey,
        }
    payload = json.dumps(payload_dict)

    timeseriescode_response = requests.post(
        f"{url}/timeseriescode",
        headers={"Content-Type": "application/json"},
        data=payload,
    )

    if timeseriescode_response.status_code == 404:
        raise Exception(
            f"Error: Resource not found (404). Response content: {timeseriescode_response.content.decode('utf-8')}"
        )

    timeseriescode = pl.read_csv(timeseriescode_response.content)

    codedescriptions_response = requests.post(
        f"{url}/codedescriptions",
        headers={"Content-Type": "application/json"},
        data=payload,
    )

    if codedescriptions_response.status_code == 404:
        raise Exception(
            f"Error: Resource not found (404). Response content: {codedescriptions_response.content.decode('utf-8')}"
        )

    codedescriptions = pl.read_csv(codedescriptions_response.content, has_header=True)

    # Output formatting
    if output_format == "codes":
        out = timeseriescode

    elif output_format == "names":
        # Extract description for the timeseries code
        description = codedescriptions.select("Description").to_series().to_list()

        out = timeseriescode.rename(
            dict(zip(timeseriescode.columns, ["date"] + description))
        )

    elif output_format == "nested":
        timeseriescode_long = timeseriescode.melt(
            id_vars=["date_col"],
            value_vars=[col for col in timeseriescode.columns if col != "date_col"],
        )

        timeseriescode_grouped = timeseriescode_long.groupby("variable").agg(
            ["date_col", "value"]
        )

        out = codedescriptions.join(
            timeseriescode_grouped,
            left_on="Timeseries code",
            right_on="variable",
            how="left",
        )

    # Calculate total runtime
    total_time = round(time.time() - start_time, 3)
    log.debug(f"Total runtime: [{total_time}s]")

    return out
