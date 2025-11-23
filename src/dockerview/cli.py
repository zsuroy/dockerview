import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
from .monitor import DockerMonitor

console = Console()


def generate_table(monitor):
    """Create a table containing the latest data."""
    table = Table(title="DockerView Monitor (Press Ctrl+C to exit)")

    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("CPU %", justify="right")
    table.add_column("Memory Usage", justify="right")

    stats_list = monitor.get_all_stats()

    for stat in stats_list:
        table.add_row(
            stat["id"],
            stat["name"],
            stat["status"],
            stat["cpu"],
            stat["memory"]
        )

    return table


def main():
    try:
        monitor = DockerMonitor()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return

    console.print("[yellow]Initializing monitor...[/yellow]")

    # Use Rich's Live component to implement auto-refresh
    try:
        with Live(generate_table(monitor), refresh_per_second=1) as live:
            while True:
                time.sleep(1)
                live.update(generate_table(monitor))
    except KeyboardInterrupt:
        console.print("\n[bold blue]Stopped.[/bold blue]")
