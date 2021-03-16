import typing as t
from pathlib import Path

import httpx
import typer

app = typer.Typer()

base_url = typer.Option("http://0x0.st", envvar="OXO_BASE_URL")


@app.command()
def files(
    files: t.List[Path] = typer.Argument(..., min=1, exists=True, file_okay=True, dir_okay=False, resolve_path=True),
    base_url: str = base_url,
):
    """Upload one or more files."""
    urls = []
    with httpx.Client() as client:
        for f in files:
            payload = {"file": f.open("rb")}
            res = client.post(base_url, files=payload)
            if res.status_code == httpx.codes.OK:
                urls.append(res.text.strip())
    typer.echo("\n".join(urls), nl=False)


@app.command()
def repost(urls: t.List[str], base_url=base_url):
    """Repost one or more urls."""
    reposted = []
    with httpx.Client() as client:
        for u in urls:
            data = {"url": u.strip()}
            res = client.post(base_url, data=data)
            if res.status_code == httpx.codes.OK:
                reposted.append(res.text.strip())
    typer.echo("\n".join(reposted), nl=False)


@app.command()
def shorten(urls: t.List[str], base_url=base_url):
    """Shorten one or more urls."""
    shortened = []
    with httpx.Client() as client:
        for u in urls:
            data = {"shorten": u.strip()}
            res = client.post(base_url, data=data)
            if res.status_code == httpx.codes.OK:
                shortened.append(res.text.strip())
    typer.echo("\n".join(shortened), nl=False)
