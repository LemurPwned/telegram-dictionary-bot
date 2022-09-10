"""Console script for telegram_notes."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("telegram-notes")
    click.echo("=" * len("telegram-notes"))
    click.echo("Telegram bot for note ops")


if __name__ == "__main__":
    main()  # pragma: no cover
