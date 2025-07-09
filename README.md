# Instagram Bot

A collection of Instagram automation bots for interacting with users who comment specific numbers on posts. These bots can send direct messages to users based on their follower status.

## Features

### Three Different Implementation Methods

1. **With Browser Profile (instagram bot.py)**
   - Uses your existing Chrome profile for authentication
   - No need to log in manually each time
   - Maintains session cookies and preferences
   - Tracks sent messages using CSV file
   - Sends different messages to followers vs. non-followers

2. **With Login and CSV Tracking (no login with csv.py)**
   - Logs in with username and password
   - Tracks sent messages using CSV file
   - Sends different messages to followers vs. non-followers
   - Handles login and notification popups

3. **Basic Implementation (nologin.py)**
   - Logs in with username and password
   - Tracks sent messages in memory (session only)
   - Sends different messages to followers vs. non-followers
   - Simplest implementation for quick use

### Common Features Across All Implementations

- **Human-like Behavior**: Random sleep intervals between actions to avoid detection
- **Comment Filtering**: Identifies users who commented with a specific number ("4")
- **Follower Detection**: Checks if users are following you before sending messages
- **Customized Messages**: Different message templates for followers and non-followers
- **Error Handling**: Robust error handling to continue operation even if some messages fail
- **Undetected Chrome**: Uses undetected_chromedriver to bypass anti-bot measures

## Requirements

- Python 3.6+
- Selenium
- undetected_chromedriver
- Chrome browser

## Installation

```bash
pip install selenium undetected-chromedriver
```

## Usage

### 1. Using Browser Profile (Recommended)

Edit `instagram bot.py`:
- Set your Chrome profile path in `user_data_dir`
- Update `POST_URL` with your Instagram post URL
- Customize message templates as needed

Run:
```bash
python "instagram bot.py"
```

### 2. Using Login with CSV Tracking

Edit `no login with csv.py`:
- Set your Instagram `USERNAME` and `PASSWORD`
- Update `POST_URL` with your Instagram post URL
- Customize message templates as needed

Run:
```bash
python "no login with csv.py"
```

### 3. Basic Implementation

Edit `nologin.py`:
- Set your Instagram `USERNAME` and `PASSWORD`
- Update `POST_URL` with your Instagram post URL
- Customize message templates as needed

Run:
```bash
python nologin.py
```

## How It Works

1. The bot navigates to a specified Instagram post
2. It loads and scans comments for users who commented with "4"
3. For each qualifying user:
   - Checks if they're already in the sent_users list/file
   - Visits their profile to determine if they're following you
   - Sends an appropriate message based on follower status
   - Records successful message sends

## Customization

- **Target Comment**: Change the `if text == "4":` condition to target different comments
- **Messages**: Modify `DM_MESSAGE_FOLLOWER` and `DM_MESSAGE_NONFOLLOWER` variables
- **Sleep Intervals**: Adjust the `human_sleep` function parameters for faster/slower operation

## Disclaimer

This bot is for educational purposes only. Using automation tools against Instagram's Terms of Service may result in account restrictions. Use at your own risk.

## License

MIT