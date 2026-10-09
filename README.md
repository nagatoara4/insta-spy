# INSTA-SPY v1.0 — "THE EYE" 👁️

> Instagram OSINT Tool — Nothing Hides From The Eye

[![Version](https://img.shields.io/badge/version-1.0.0-red.svg)]()
[![Platform](https://img.shields.io/badge/platform-iSH%20arm64%20iPhone-blue.svg)]()
[![Built By](https://img.shields.io/badge/built%20by-worm%20shadow-purple.svg)]()

## 🎯 What It Does

Enter any Instagram username. Get everything about them.

## ⚡ Features

| Feature | Power |
|---------|-------|
| Profile Analysis | Real name, bio, followers, posts |
| Story Detection | See if they have active stories |
| Post Analysis | Last 12 posts, engagement rate |
| Hashtag Extraction | Top hashtags they use |
| Location Tracking | Extract location from bio and posts |
| Contact Extraction | Find email, phone in bio |
| Linked Accounts | Find their Twitter, TikTok, Facebook, etc |
| Follower Analysis | Follower ratio, account type |
| Engagement Rate | How popular they really are |

## 📱 Works On

- iSH arm64 iPhone
- Any Linux
- Termux Android
- macOS

## 🚀 Install & Run

```bash
# iSH iPhone
pip install requests
python3 insta-spy.py <username>

# Example
python3 insta-spy.py zuck
```

## 📊 Sample Output

```
╔══════════════════════════════════════════════════════════════╗
║              👁️  NOTHING HIDES FROM THE EYE  👁️              ║
╚══════════════════════════════════════════════════════════════╝

[*] Target: @zuck
[*] Starting deep scan...

[1] Profile Analysis
  ✓ Full Name: Mark Zuckerberg
  ✓ Followers: 8,234,567
  ✓ Following: 345
  ✓ Posts: 876
  ✓ Private: No 🌍
  ✓ Verified: Yes ✅

[2] Stories Analysis
  ✓ Active story detected! 🔥

[3] Posts Analysis
  ✓ Top Hashtags: #meta #facebook #vr
  ✓ Engagement Rate: 4.23%

[4] Followers Analysis
  ✓ Follower/Following Ratio: 23865.41
  ✓ Account Type: Influencer/Public Figure 🌟

[5] Contact Extraction
  ✓ External URL: https://facebook.com

[6] Linked Accounts Search
  ✓ Twitter: FOUND ✅
  ✓ Facebook: FOUND ✅
  ✓ TikTok: FOUND ✅
  ✗ Snapchat: not found
  ...

[+] Report saved: report_zuck_1696789012.json
```

## ⚠️ Disclaimer

For educational purposes only. Respect privacy laws.

## 📄 License

MIT

## 🙏 Built By

**worm shadow** for **He**

---

**THE EYE SEES EVERYTHING** 👁️
