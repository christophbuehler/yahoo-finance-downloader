import yfinance as yf
from pydantic import BaseModel
from typing import List
import yaml
import os
from tqdm import tqdm
from termcolor import colored
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")

config_file = "config.yaml"


class ConfigSchema(BaseModel):
    DateFrom: str
    DateUntil: str
    Interval: str
    Output: str
    DecimalSeparator: str
    Symbols: List[str]
    Columns: List[str]
    Prepost: bool
    Actions: bool
    AutoAdjust: bool
    BackAdjust: bool
    Repair: bool
    Keepna: bool
    Rounding: bool
    Timeout: int
    RaiseErrors: bool


try:
    print(
        colored(
            f"🚀 Launched Yahoo Finance Downloader.",
            "blue",
        )
    )

    with open(config_file, "r") as file:
        content = yaml.safe_load(file)
        config = ConfigSchema(**content)

        print(
            colored(
                f"✅ Your {config_file} is valid. Downloading data for {len(config.Symbols)} symbols from {config.DateFrom} to {config.DateUntil}.",
                "green",
            )
        )

        print(".")

        for index, symbol in enumerate(config.Symbols):
            print(
                "├── "
                + f"[{index + 1}/{len(config.Symbols)}] Fetching data for: {symbol}"
            )

            ticker = yf.Ticker(symbol)
            metadata = {
                "Symbol": symbol,
                "DateFrom": config.DateFrom,
                "DateUntil": config.DateUntil,
            }

            output_file = config.Output.format(**metadata)
            history = ticker.history(
                start=config.DateFrom,
                end=config.DateUntil,
                interval=config.Interval,
                prepost=config.Prepost,
                actions=config.Actions,
                auto_adjust=config.AutoAdjust,
                back_adjust=config.BackAdjust,
                repair=config.Repair,
                keepna=config.Keepna,
                rounding=config.Rounding,
                timeout=config.Timeout,
                raise_errors=config.RaiseErrors,
            )

            output_fns = {
                "csv": lambda: history.to_csv(
                    output_file, decimal=config.DecimalSeparator, columns=config.Columns
                ),
                "json": lambda: history.to_json(
                    output_file, decimal=config.DecimalSeparator, columns=config.Columns
                ),
                "xls": lambda: history.to_excel(
                    output_file, decimal=config.DecimalSeparator, columns=config.Columns
                ),
                "xlsx": lambda: history.to_excel(
                    output_file, decimal=config.DecimalSeparator, columns=config.Columns
                ),
            }

            extension = os.path.splitext(output_file)[1][1:]

            dir_name = os.path.dirname(output_file)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
                print("│   ├── " + f"📁 Created directory: {dir_name}")

            output_fns[extension]()
            print(
                ("    └── " if (index == len(config.Symbols) - 1) else "│   └── ")
                + colored(f"✅ Saved data to: {output_file}", "green")
            )

        print(colored("🎉 All done!", "magenta"))

except Exception as e:
    print(f"Error: {e}")


input("Press Enter to close...")
