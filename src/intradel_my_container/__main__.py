""" Allow to test the package from command line"""

from datetime import datetime
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from intradel_my_container import Informations, IntradelMyContainer, Organic, Residual

console = Console()


def main(
    login: Annotated[
        str,
        typer.Option("--login", "-l", envvar="INTRADEL_LOGIN", prompt="Intradel login"),
    ],
    password: Annotated[
        str,
        typer.Option(
            "--password", "-p", envvar="INTRADEL_PASSWORD", prompt="Intradel password"
        ),
    ],
    municipality_id: Annotated[
        str,
        typer.Option(
            "--municipality-id",
            "-m",
            envvar="INTRADEL_MUNICIPALITY",
            prompt="Intradel municipality ID",
        ),
    ],
    start_date: Annotated[
        Optional[datetime],
        typer.Option("--start-date", "-s", formats=["%Y-%m-%d"]),
    ] = None,
    end_date: Annotated[
        Optional[datetime],
        typer.Option("--end-date", "-e", formats=["%Y-%m-%d"]),
    ] = None,
):
    """
    Retrieve the Intradel data from command line.
    """
    data: IntradelMyContainer = IntradelMyContainer(
        login=login,
        password=password,
        municipality_id=municipality_id,
        start_date=start_date,
        end_date=end_date,
    )

    informations: Informations = data.my_informations
    table_info: Table = Table(title="Informations", show_header=False)
    table_info.add_row("Name", informations.name)
    table_info.add_row("Address", informations.address)
    table_info.add_row("Category", informations.category)
    table_info.add_row("Actif", informations.actif.strftime("%Y-%m-%d"))
    console.print(table_info)

    organic: Organic = data.organic
    table_organic: Table = Table(title="Organic", show_header=False)
    table_organic.add_row("Chip number", organic.chip_number)
    table_organic.add_row("Volume", str(organic.volume))
    table_organic.add_row("Collects", str(organic.total_collects()))
    table_organic.add_row("Weight", str(organic.total_kilograms()))
    table_organic.add_row("Since", organic.since.strftime("%Y-%m-%d"))
    table_organic.add_row("Status", organic.status)
    console.print(table_organic)

    residual: Residual = data.residual
    table_residual: Table = Table(title="Residual", show_header=False)
    table_residual.add_row("Chip number", residual.chip_number)
    table_residual.add_row("Volume", str(residual.volume))
    table_residual.add_row("Collects", str(residual.total_collects()))
    table_residual.add_row("Weight", str(residual.total_kilograms()))
    table_residual.add_row("Since", residual.since.strftime("%Y-%m-%d"))
    table_residual.add_row("Status", residual.status)
    console.print(table_residual)


if __name__ == "__main__":
    typer.run(main)
