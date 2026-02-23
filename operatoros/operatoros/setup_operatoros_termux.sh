#!/bin/bash
set -e

# Step 1: Update packages
pkg update -y
pkg upgrade -y

# Step 2: Install Python and Git if not installed
pkg install -y python git

# Step 3: Create OperatorOS folder if it doesn't exist
OPERATOROS_DIR=$HOME/operatoros/operatoros
mkdir -p "$OPERATOROS_DIR"

cd "$OPERATOROS_DIR"

# Step 4: Create virtual environment
python -m venv venv
source venv/bin/activate

# Step 5: Upgrade pip
pip install --upgrade pip

# Step 6: Install dependencies
pip install rich==14.3.1 pydantic==1.10.12 python-dotenv

# Step 7: Populate OperatorOS skeleton files

mkdir -p operatoros

echo "Creating __init__.py"
cat > operatoros/__init__.py << 'EOF'
# marks this folder as a package
EOF

echo "Creating config.py"
cat > operatoros/config.py << 'EOF'
from dotenv import load_dotenv
import os

load_dotenv()

CONFIG = {
    "project_name": os.getenv("PROJECT_NAME", "OperatorOS"),
    "version": os.getenv("VERSION", "0.1"),
}
EOF

echo "Creating state.py"
cat > operatoros/state.py << 'EOF'
class State:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_name):
        self.tasks.append(task_name)

    def list_tasks(self):
        return self.tasks
EOF

echo "Creating logger.py"
cat > operatoros/logger.py << 'EOF'
from rich.console import Console

console = Console()

def log(info):
    console.print(f"[bold green][LOG][/bold green] {info}")
EOF

echo "Creating main.py"
cat > operatoros/main.py << 'EOF'
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
EOF

# Create placeholder modules
for mod in analytics bundle_generator niche_research picker; do
    echo "Creating placeholder $mod.py"
    cat > operatoros/$mod.py << 'EOF'
# placeholder module
EOF
done

echo "Creating run_operatoros.py"
cat > run_operatoros.py << 'EOF'
from operatoros import main

if __name__ == "__main__":
    main.bootstrap()
    main.interactive()
EOF

# Step 8: Finish
echo "OperatorOS skeleton created successfully!"
echo "To run:"
echo "cd $OPERATOROS_DIR"
echo "source venv/bin/activate"
echo "python run_operatoros.py"
