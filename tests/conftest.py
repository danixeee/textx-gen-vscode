from pathlib import Path

import pytest

EXAMPLES_PATH = Path(__file__).parent.parent.resolve() / "examples"


@pytest.fixture
def workflow_grammar_path():
    return str(EXAMPLES_PATH / "workflow" / "tx_workflow" / "workflow.tx")
