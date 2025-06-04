import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(project_root, ".."))

print(f"export PYTHONPATH={project_root}")
