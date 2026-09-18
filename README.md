# GitHub Activity & Auto Commit Bot 🚀

An automated GitHub Action repository designed to keep your GitHub profile active with realistic randomized commits and automated repository forks.

## Features
- **High Activity Commits**: Runs every 3 hours (`0 */3 * * *`) and generates up to 50 commits per run with natural commit messages.
- **Auto Fork Bot**: Automatically discovers and forks trending repositories twice daily to boost repository and fork counts on your profile.
- **Fully Automated**: Runs completely on GitHub Actions without needing your computer powered on.
- **Manual Trigger**: Can be manually run on-demand via the Actions tab.

## Setup Instructions

### 1. Enable Workflow Permissions (for Auto-Commits)
1. In your GitHub repository, go to **Settings** > **Actions** > **General**.
2. Under **Workflow permissions**, choose **Read and write permissions**.
3. Click **Save**.

### 2. Configure Auto-Forking (Optional, for Fork Activity)
GitHub's built-in token cannot fork repositories into your personal account, so a Personal Access Token is needed:
1. Go to [GitHub Token Settings](https://github.com/settings/tokens?type=beta) or [Classic Tokens](https://github.com/settings/tokens/new).
2. Create a token with `public_repo` (or `repo`) scope.
3. In this repository, go to **Settings** > **Secrets and variables** > **Actions**.
4. Click **New repository secret**, name it `AUTO_FORK_PAT`, paste your token, and click **Add secret**.
