# Setup Guide

## 1. Create the special "profile" repo
GitHub shows a README automatically on your profile page **only** if you create
a repo with the *exact same name* as your username.

- New repo → name it `YOUR_USERNAME` (must match exactly, case-insensitive)
- Public
- Initialize with a README (you'll overwrite it)

## 2. Add these files
Copy everything from this package into that repo:

```
YOUR_USERNAME/
├── README.md
├── .github/
│   └── workflows/
│       ├── update-facts.yml
│       ├── snake.yml
│       └── metrics.yml
└── scripts/
    └── update_readme.py
```

## 3. Find-and-replace placeholders
In `README.md`, replace:
- `YOUR_USERNAME` → your actual GitHub username (appears ~10 times)
- `YOUR_NAME` → your display name
- `you@example.com` → your real email (or delete that line)
- The "Currently working on / learning" bullets → your real info

## 4. Turn on write permissions for Actions
The bots need to commit back to your repo:
- Repo → **Settings → Actions → General → Workflow permissions**
- Select **"Read and write permissions"**
- Save

## 5. Run the workflows once manually
- Go to the **Actions** tab
- Run each workflow manually the first time (`Run workflow` button) so you don't
  have to wait for the cron schedule:
  - `Generate Snake Contribution Graph`
  - `Generate Metrics`
  - `Update README Live Section`

The snake workflow pushes to a branch called `output` — that's expected, don't
delete it, the README links directly to files on that branch.

## 6. (Optional) Extra stats services — no code needed, just swap the username
- **Streak stats**: already wired to `github-readme-streak-stats.herokuapp.com`
- **WakaTime coding-time graph**: sign up at wakatime.com, install their editor
  plugin, then add a badge like:
  `![wakatime](https://wakatime.com/badge/user/YOUR_WAKATIME_ID.svg)`
- **Spotify "now playing"**: use `kittinan/spotify-github-profile` — needs a
  Spotify API secret added under repo Settings → Secrets

## 7. Sanity check
Wait a few minutes after the manual runs, then visit
`github.com/YOUR_USERNAME` — you should see:
- Typing animation at the top
- Stats cards populated with real numbers
- Snake animation eating your contribution graph
- The "Live Feed" section showing today's date + a real arXiv paper

If a stats card shows an error image instead of numbers, it's almost always a
typo in the username — double check every `YOUR_USERNAME` was replaced.

## Notes
- Nothing here requires a paid service or secret API key except the optional
  Spotify widget.
- The bots run on GitHub's free Actions minutes — a public repo gets 2,000
  free minutes/month, and these workflows use well under a minute each per run.
