#!/bin/bash

GITHUB_TOKEN=$1

TEST_OUTPUT="This is a test output"
echo "::set-output name=TEST_OUTPUT::$TEST_OUTPUT"
