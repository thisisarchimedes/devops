

# Initialize variables
PR_NUMBER=""
PAGE=1
PER_PAGE=1  # Adjust if you expect to check more PRs

# Prepare the API endpoint for fetching closed PRs targeting the main branch
PRS_URL="https://api.github.com/repos/${{ github.repository }}/pulls?state=closed&base=main&sort=updated&direction=desc&per_page=$PER_PAGE&page=$PAGE"

# Fetch the PR data using GitHub API
RESPONSE=$(curl -s -H "Authorization: token ${{ secrets.PAT_TOKEN }}" -H "Accept: application/vnd.github.v3+json" "$PRS_URL")
    
# Check if the API response is valid and contains an array
if ! jq empty <<< "$RESPONSE"; then
    echo "Failed to parse JSON, or got empty response"
    exit 1
fi

# Extract PR number from the response
PR_NUMBER=$(echo "$RESPONSE" | jq -r '.[0].number')
if [ -z "$PR_NUMBER" ]; then
    echo "Could not find a recently merged PR targeting the main branch."
    exit 0  # Exit gracefully, not an error, just no recently merged PR found
fi

echo "PR Number: $PR_NUMBER"
