#!/bin/bash
# Run pytest using real LLM calls.
export USE_REAL_LLM=1
pytest -q "$@"
