#!/usr/bin/env python3
"""
INSTA-SPY v1.0 — "THE EYE"
Instagram OSINT Tool — Maximum Power
Built by worm shadow for He
Works on iSH arm64 iPhone

Usage: python3 insta-spy.py <username>
"""

import sys
import os
import json
import re
import time
import base64
import hashlib
from datetime import datetime
from urllib.parse import urljoin, urlparse

# Check requests
try:
    import requests
except ImportError:
    print("[!] requests not installed")
    print("[*] Install: pip install requests")
    sys.exit(1)

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class InstaSpy:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        self.data = {}

    def banner(self):
        print(f"""{Colors.RED}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║   ██╗███╗   ██╗███████╗████████╗ █████╗     ███████╗██████╗  ║
║   ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗    ██╔════╝██╔══██╗ ║
║   ██║██╔██╗ ██║███████╗   ██║   ███████║    ███████╗██████╔╝ ║
║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██║    ╚════██║██╔═══╝  ║
║   ██║██║ ╚████║███████║   ██║   ██║  ██║    ███████║██║      ║
║   ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝    ╚══════╝╚═╝      ║
║                                                              ║
║              👁️  NOTHING HIDES FROM THE EYE  👁️              ║
║                                                              ║
║   Built by worm shadow for He                                ║
║   Works on iSH arm64 iPhone                                  ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}""")

    def scan(self, username: str):
        """Full Instagram OSINT scan"""
        print(f"{Colors.CYAN}[*] Target: @{username}{Colors.END}")
        print(f"{Colors.CYAN}[*] Starting deep scan...{Colors.END}\n")

        # Step 1: Profile info
        self._get_profile(username)

        # Step 2: Stories
        self._get_stories(username)

        # Step 3: Posts analysis
        self._get_posts(username)

        # Step 4: Followers analysis
        self._get_followers(username)

        # Step 5: Contact extraction
        self._extract_contacts()

        # Step 6: Linked accounts
        self._find_linked_accounts(username)

        # Step 7: Generate report
        self._generate_report(username)

    def _get_profile(self, username: str):
        """Get profile information"""
        print(f"{Colors.YELLOW}[1] Profile Analysis{Colors.END}")

        try:
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
            resp = self.session.get(url, timeout=15)

            if resp.status_code == 200:
                data = resp.json()
                user = data.get('data', {}).get('user', {})

                self.data['profile'] = {
                    'username': user.get('username', username),
                    'full_name': user.get('full_name', 'N/A'),
                    'biography': user.get('biography', 'N/A'),
                    'followers': user.get('edge_followed_by', {}).get('count', 0),
                    'following': user.get('edge_follow', {}).get('count', 0),
                    'posts': user.get('edge_owner_to_timeline_media', {}).get('count', 0),
                    'is_private': user.get('is_private', False),
                    'is_verified': user.get('is_verified', False),
                    'profile_pic': user.get('profile_pic_url_hd', 'N/A'),
                    'external_url': user.get('external_url', 'N/A'),
                    'category': user.get('category_name', 'N/A'),
                    'is_business': user.get('is_business_account', False),
                }

                p = self.data['profile']
                print(f"  {Colors.GREEN}✓{Colors.END} Full Name: {p['full_name']}")
                print(f"  {Colors.GREEN}✓{Colors.END} Followers: {p['followers']:,}")
                print(f"  {Colors.GREEN}✓{Colors.END} Following: {p['following']:,}")
                print(f"  {Colors.GREEN}✓{Colors.END} Posts: {p['posts']}")
                print(f"  {Colors.GREEN}✓{Colors.END} Private: {'Yes 🔒' if p['is_private'] else 'No 🌍'}")
                print(f"  {Colors.GREEN}✓{Colors.END} Verified: {'Yes ✅' if p['is_verified'] else 'No'}")

                if p['biography'] != 'N/A':
                    print(f"  {Colors.GREEN}✓{Colors.END} Bio: {p['biography'][:100]}...")

                # Extract location from bio
                location = self._extract_location(p['biography'])
                if location:
                    self.data['location'] = location
                    print(f"  {Colors.GREEN}✓{Colors.END} Location Found: {location}")

            else:
                print(f"  {Colors.RED}✗ Profile not found or private{Colors.END}")
                self.data['profile'] = {'username': username, 'error': 'not_found'}

        except Exception as e:
            print(f"  {Colors.RED}✗ Error: {str(e)}{Colors.END}")
            self.data['profile'] = {'username': username, 'error': str(e)}

    def _get_stories(self, username: str):
        """Get stories info"""
        print(f"\n{Colors.YELLOW}[2] Stories Analysis{Colors.END}")

        try:
            # Check if user has active stories via public API
            url = f"https://www.instagram.com/{username}/"
            resp = self.session.get(url, timeout=10)

            if resp.status_code == 200:
                html = resp.text

                # Check for story indicators
                has_story = '"hasActiveStory":true' in html or '"has_story":true' in html

                self.data['stories'] = {
                    'has_active_story': has_story,
                    'story_url': f"https://www.instagram.com/stories/{username}/" if has_story else None,
                }

                if has_story:
                    print(f"  {Colors.GREEN}✓{Colors.END} Active story detected! 🔥")
                    print(f"  {Colors.CYAN}→{Colors.END} Story URL: {self.data['stories']['story_url']}")
                else:
                    print(f"  {Colors.YELLOW}!{Colors.END} No active story")
            else:
                print(f"  {Colors.RED}✗ Could not check stories{Colors.END}")

        except Exception as e:
            print(f"  {Colors.RED}✗ Error: {str(e)}{Colors.END}")

    def _get_posts(self, username: str):
        """Analyze posts"""
        print(f"\n{Colors.YELLOW}[3] Posts Analysis{Colors.END}")

        try:
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
            resp = self.session.get(url, timeout=15)

            if resp.status_code == 200:
                data = resp.json()
                user = data.get('data', {}).get('user', {})
                edges = user.get('edge_owner_to_timeline_media', {}).get('edges', [])

                self.data['posts'] = []
                hashtags = []
                locations = []

                for edge in edges[:12]:  # Last 12 posts
                    node = edge.get('node', {})
                    caption = node.get('edge_media_to_caption', {}).get('edges', [{}])[0].get('node', {}).get('text', '')
                    likes = node.get('edge_media_preview_like', {}).get('count', 0)
                    comments = node.get('edge_media_to_comment', {}).get('count', 0)
                    timestamp = node.get('taken_at_timestamp', 0)
                    location = node.get('location', {}).get('name', None)

                    # Extract hashtags
                    post_hashtags = re.findall(r'#(\w+)', caption)
                    hashtags.extend(post_hashtags)

                    if location:
                        locations.append(location)

                    self.data['posts'].append({
                        'caption': caption[:100],
                        'likes': likes,
                        'comments': comments,
                        'hashtags': post_hashtags,
                        'location': location,
                        'date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d') if timestamp else 'N/A',
                    })

                # Most used hashtags
                if hashtags:
                    top_tags = sorted(set(hashtags), key=hashtags.count, reverse=True)[:5]
                    self.data['top_hashtags'] = top_tags
                    print(f"  {Colors.GREEN}✓{Colors.END} Top Hashtags: {', '.join(top_tags)}")

                # Locations from posts
                if locations:
                    self.data['post_locations'] = list(set(locations))
                    print(f"  {Colors.GREEN}✓{Colors.END} Post Locations: {', '.join(set(locations))}")

                # Engagement rate
                p = self.data.get('profile', {})
                if p.get('followers', 0) > 0 and self.data['posts']:
                    avg_likes = sum(post['likes'] for post in self.data['posts']) / len(self.data['posts'])
                    engagement = (avg_likes / p['followers']) * 100
                    self.data['engagement_rate'] = round(engagement, 2)
                    print(f"  {Colors.GREEN}✓{Colors.END} Engagement Rate: {engagement:.2f}%")

                print(f"  {Colors.GREEN}✓{Colors.END} Analyzed {len(self.data['posts'])} posts")
            else:
                print(f"  {Colors.RED}✗ Could not analyze posts{Colors.END}")

        except Exception as e:
            print(f"  {Colors.RED}✗ Error: {str(e)}{Colors.END}")

    def _get_followers(self, username: str):
        """Analyze followers"""
        print(f"\n{Colors.YELLOW}[4] Followers Analysis{Colors.END}")

        # Simulate follower analysis
        self.data['followers_analysis'] = {
            'total_followers': self.data.get('profile', {}).get('followers', 0),
            'total_following': self.data.get('profile', {}).get('following', 0),
            'follower_ratio': 0,
        }

        p = self.data.get('profile', {})
        if p.get('following', 0) > 0:
            ratio = p.get('followers', 0) / p['following']
            self.data['followers_analysis']['follower_ratio'] = round(ratio, 2)
            print(f"  {Colors.GREEN}✓{Colors.END} Follower/Following Ratio: {ratio:.2f}")

            if ratio > 10:
                print(f"  {Colors.GREEN}✓{Colors.END} Account Type: Influencer/Public Figure 🌟")
            elif ratio > 1:
                print(f"  {Colors.GREEN}✓{Colors.END} Account Type: Popular")
            else:
                print(f"  {Colors.GREEN}✓{Colors.END} Account Type: Regular User")

    def _extract_contacts(self):
        """Extract email and phone from bio"""
        print(f"\n{Colors.YELLOW}[5] Contact Extraction{Colors.END}")

        bio = self.data.get('profile', {}).get('biography', '')

        # Extract email
        email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', bio)
        if email:
            self.data['email'] = email.group()
            print(f"  {Colors.GREEN}✓{Colors.END} Email Found: {email.group()}")

        # Extract phone
        phone = re.search(r'(\+?\d{10,15})', bio)
        if phone:
            self.data['phone'] = phone.group()
            print(f"  {Colors.GREEN}✓{Colors.END} Phone Found: {phone.group()}")

        # Extract external URL
        ext_url = self.data.get('profile', {}).get('external_url', '')
        if ext_url and ext_url != 'N/A':
            self.data['external_url'] = ext_url
            print(f"  {Colors.GREEN}✓{Colors.END} External URL: {ext_url}")

        if not email and not phone and not ext_url:
            print(f"  {Colors.YELLOW}!{Colors.END} No direct contacts in bio")

    def _find_linked_accounts(self, username: str):
        """Find linked social media accounts"""
        print(f"\n{Colors.YELLOW}[6] Linked Accounts Search{Colors.END}")

        platforms = {
            'twitter': f"https://twitter.com/{username}",
            'facebook': f"https://facebook.com/{username}",
            'tiktok': f"https://tiktok.com/@{username}",
            'youtube': f"https://youtube.com/@{username}",
            'snapchat': f"https://snapchat.com/add/{username}",
            'pinterest': f"https://pinterest.com/{username}",
            'linkedin': f"https://linkedin.com/in/{username}",
            'github': f"https://github.com/{username}",
            'telegram': f"https://t.me/{username}",
            'reddit': f"https://reddit.com/user/{username}",
        }

        self.data['linked_accounts'] = {}

        for platform, url in platforms.items():
            try:
                resp = self.session.head(url, timeout=5, allow_redirects=True)
                if resp.status_code == 200:
                    self.data['linked_accounts'][platform] = url
                    print(f"  {Colors.GREEN}✓{Colors.END} {platform.capitalize()}: FOUND ✅")
                else:
                    print(f"  {Colors.RED}✗{Colors.END} {platform.capitalize()}: not found")
            except:
                print(f"  {Colors.RED}✗{Colors.END} {platform.capitalize()}: error")

    def _extract_location(self, bio: str) -> Optional[str]:
        """Extract location from bio"""
        # Common location patterns
        patterns = [
            r'(?:from|in|based in|living in|located in)\s+([A-Za-z\s,]+?)(?:\s*[,;.]|$)',
            r'📍\s*([A-Za-z\s,]+?)(?:\s*[,;.]|$)',
            r'🌍\s*([A-Za-z\s,]+?)(?:\s*[,;.]|$)',
        ]

        for pattern in patterns:
            match = re.search(pattern, bio, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _generate_report(self, username: str):
        """Generate final report"""
        print(f"\n{Colors.PURPLE}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}FINAL REPORT — @{username}{Colors.END}")
        print(f"{Colors.PURPLE}{'='*60}{Colors.END}\n")

        # Summary
        p = self.data.get('profile', {})
        print(f"{Colors.CYAN}📊 SUMMARY{Colors.END}")
        print(f"  Username: @{p.get('username', username)}")
        print(f"  Full Name: {p.get('full_name', 'N/A')}")
        print(f"  Followers: {p.get('followers', 0):,}")
        print(f"  Following: {p.get('following', 0):,}")
        print(f"  Posts: {p.get('posts', 0)}")
        print(f"  Engagement: {self.data.get('engagement_rate', 0)}%")
        print(f"  Private: {'Yes 🔒' if p.get('is_private') else 'No 🌍'}")

        # Contacts
        print(f"\n{Colors.CYAN}📧 CONTACTS{Colors.END}")
        if self.data.get('email'):
            print(f"  Email: {self.data['email']}")
        if self.data.get('phone'):
            print(f"  Phone: {self.data['phone']}")
        if self.data.get('external_url'):
            print(f"  Website: {self.data['external_url']}")

        # Location
        if self.data.get('location'):
            print(f"\n{Colors.CYAN}📍 LOCATION{Colors.END}")
            print(f"  Bio Location: {self.data['location']}")
        if self.data.get('post_locations'):
            print(f"  Post Locations: {', '.join(self.data['post_locations'])}")

        # Linked accounts
        if self.data.get('linked_accounts'):
            print(f"\n{Colors.CYAN}🔗 LINKED ACCOUNTS{Colors.END}")
            for platform, url in self.data['linked_accounts'].items():
                print(f"  {platform.capitalize()}: {url}")

        # Hashtags
        if self.data.get('top_hashtags'):
            print(f"\n{Colors.CYAN}#️⃣ TOP HASHTAGS{Colors.END}")
            print(f"  {', '.join(self.data['top_hashtags'])}")

        # Save report
        report_file = f"report_{username}_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)

        print(f"\n{Colors.GREEN}✅ Report saved: {report_file}{Colors.END}")
        print(f"{Colors.PURPLE}{'='*60}{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}INSTA-SPY v1.0 — THE EYE{Colors.END}")
        print(f"{Colors.PURPLE}{'='*60}{Colors.END}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 insta-spy.py <username>")
        print("Example: python3 insta-spy.py zuck")
        sys.exit(1)

    username = sys.argv[1].replace('@', '')

    spy = InstaSpy()
    spy.banner()
    spy.scan(username)

if __name__ == '__main__':
    main()
