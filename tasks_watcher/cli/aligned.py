import typer

from typing import List

Table = List[List[str]]

def print_aligned(table: Table) -> None:
    max_lens = [len(cell) for row in table for cell in row]

    for row in table:
        for i, (new_cell, cell_len) in enumerate(zip(row, max_lens)):
            if (new_len := len(new_cell)) > cell_len:
                max_lens[i] = new_len
    
    for row in table:
        line = " ".join(cell.ljust(l + 1) for cell, l in zip(row, max_lens))
        typer.echo(line)
