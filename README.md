# GitHub Auto Commit Bot 🚀

An automated GitHub Action repository designed to generate daily commits to keep your GitHub contribution graph active with realistic, randomized commit patterns.

## Features
- **Cron Schedule**: Runs automatically throughout the day.
- **Randomized Activity**: Randomly decides how many commits to make (or skip) to emulate natural coding patterns.
- **Manual Trigger**: Can be triggered manually via `workflow_dispatch` in GitHub Actions.

## Setup Instructions
1. Push this code to a public or private repository on GitHub.
2. In your GitHub repository, go to **Settings** > **Actions** > **General**.
3. Under **Workflow permissions**, select **Read and write permissions** and click **Save**.
4. That's it! Your workflow will run automatically according to the schedule in `.github/workflows/auto-commit.yml`.
