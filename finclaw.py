#!/usr/bin/env python3

import typer
from social.ts import trump as t
from finance.twelvedata import historical_data


app = typer.Typer(help="The Fin Claw")
social = typer.Typer(help="Claw Social Media")
finance = typer.Typer(help="Financial Data")
app.add_typer(social, name="social")
app.add_typer(finance, name="finance")

@social.command()
def trump(
        start_date: str,
        end_date: str
):
    tweets = t.claw(start_date, end_date)
    print(tweets)

@finance.command()
def hd(
        symbol: str,
        start_date: str,
        end_date: str
):
    data = historical_data.claw(symbol, start_date, end_date)
    print(data)

if __name__ == "__main__":
    app()
