from operatoros.niche_research import get_scored_niches, save_top_niches
from operatoros.gui import launch_gui

def run(mock=False):
    print("Running OperatorOS...")

    # 1. Get scored niches
    scored_niches = get_scored_niches(mock=mock)
    save_top_niches(scored_niches)

    # 2. Launch GUI and pass scored niches
    # GUI should let user pick one
    launch_gui(scored_niches)

if __name__ == "__main__":
    run()
