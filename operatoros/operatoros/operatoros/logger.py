from rich.console import Console

console = Console()

def log(info):
    console.print(f"[bold green][LOG][/bold green] {info}")
