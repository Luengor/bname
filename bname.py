#!/usr/bin/env python3
import os
import re
import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def main(
        match_regex: Annotated[str, typer.Argument(help="The regex used to match the files.")],
        rename_regex: Annotated[str, typer.Argument(help="The output names.")],
        dry: Annotated[bool, typer.Option(help="If set, don't change files.")] = True,
        full_match: Annotated[bool, typer.Option(help="If set, regex must match the whole filename.")] = True):
    # Get files in the directory
    files = [file for file in os.listdir() if os.path.isfile(file)]

    # Check names
    match_regex_cmp = re.compile(match_regex)
    new_files: list[str]

    if full_match:
        new_files = [
                match_regex_cmp.sub(rename_regex, file)
                for file in files
                if match_regex_cmp.match(file)
        ]

        print(f"{len(new_files)} files matched the regex.")
    else:
        new_files = [
                match_regex_cmp.sub(rename_regex, file)
                for file in files
        ]

    if len(new_files) != len(set(new_files)): 
        print("Multiple output files with the same name, abort.")
        exit(2)

    # Rename
    for old_name, new_name in zip(files, new_files):
        if not dry:
            os.rename(old_name, new_name)
        print(old_name, "->", new_name)

def main():
    app()

if __name__ == "__main__":
    main()

