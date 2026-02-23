from .state import State
from .logger import log
from .config import CONFIG
from rich.console import Console

console = Console()
state = State()

def bootstrap():
    log(f"Bootstrapping {CONFIG['project_name']} v{CONFIG['version']}")
    log("Modules loaded: analytics, bundle_generator, niche_research, picker")
    log("Bootstrap complete!")

def interactive():
    log("Entering interactive mode. Type 'help' for commands.")
    while True:
        try:
            cmd = console.input("[bold blue]> [/bold blue]").strip()
            if cmd.lower() in ("quit", "exit"):
                log("Exiting OperatorOS.")
                break
            elif cmd.lower() == "list":
                console.print("Tasks:", state.list_tasks())
            elif cmd.lower().startswith("add "):
                task = cmd[4:]
                state.add_task(task)
                log(f"Added task: {task}")
            elif cmd.lower() == "help":
                console.print("Commands: add [task], list, help, exit")
            else:
                console.print(f"Unknown command: {cmd}")
        except KeyboardInterrupt:
            log("Exiting OperatorOS via Ctrl+C.")
            break
