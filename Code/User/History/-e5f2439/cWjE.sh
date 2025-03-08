#!/bin/bash

# Navigate to the root project directory to run pytest
cd "$(dirname "$0")"

# Watch for changes in any Python files in the app and test directories, including subdirectories
find ./app ./test -type f -name "*.py" | entr -r pytest
