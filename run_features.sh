#!/bin/bash

for i in {1..6}
do
    # echo "Running feature_script_${i}.py..."
    python3 feature_script_${i}.py
    # echo "Completed feature_script_${i}.py"
    # echo "-------------------"
done

echo "All scripts completed"