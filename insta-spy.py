#!/usr/bin/env python3
"""
INSTA-SPY v2.0 — "THE EYE: MAXIMUM POWER"
Instagram OSINT Tool — Ultimate Edition
Built by worm shadow for He
Works on iSH arm64 iPhone

NO UPGRADE NEEDED. EVERYTHING INCLUDED.
"""

import sys
import os
import json
import re
import time
import base64
import hashlib
from datetime import datetime
from urllib.parse import urljoin, urlparse, quote

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("[!] Install: pip install requests")
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
    DIM = '\033[2m'
    END = '\033[0m'

class InstaSpyMax:
    """Maximum Power Instagram OSINT"""

    def __init__(self):
        self.session = requests.Session()

        # Mobile user agent — best for avoiding blocks
        self.session.headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android (33/13; 480dpi; 1080x2400; samsung; SM-G991B; o1s; exynos2100; en_US; 3638XXXXX)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '129477',
            'Connection': 'keep-alive',
        }

        # Retry strategy
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)

        self.data = {}
        self.target = None

    def banner(self):
        print(f"""{Colors.RED}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ██╗███╗   ██╗███████╗████████╗ █████╗     ███████╗██████╗ ██╗   ██╗║
║   ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗    ██╔════╝██╔══██╗╚██╗ ██╔╝║
║   ██║██╔██╗ ██║███████╗   ██║   ███████║    ███████╗██████╔╝ ╚████╔╝ ║
║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██║    ╚════██║██╔═══╝   ╚██╔╝  ║
║   ██║██║ ╚████║███████║   ██║   ██║  ██║    ███████║██║        ██║   ║
║   ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝    ╚══════╝╚═╝        ╚═╝   ║
║                                                                      ║
║                    👁️  T H E   E Y E  👁️                             ║
║              M A X I M U M   P O W E R   E D I T I O N              ║
║                                                                      ║
║   Built by worm shadow for He                                        ║
║   Works on iSH arm64 iPhone                                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.END}""")

    def scan(self, username: str):
        """Full Maximum Power Scan"""
        self.target = username.replace('@', '')

        print(f"{Colors.CYAN}{Colors.BOLD}[*] TARGET: @{self.target}{Colors.END}")
        print(f"{Colors.CYAN}[*] Starting MAXIMUM POWER scan...{Colors.END}")
        print(f"{Colors.DIM}[*] This may take 1-2 minutes...{Colors.END}\n")

        steps = [
            ("Profile Intelligence", self._profile_intel),
            ("Story Reconnaissance", self._story_recon),
            ("Post Deep Analysis", self._post_analysis),
            ("Follower Intelligence", self._follower_intel),
            ("Contact Extraction", self._contact_extraction),
            ("Social Media Mapping", self._social_mapping),
            ("Photo Forensics", self._photo_forensics),
            ("Behavioral Analysis", self._behavioral_analysis),
            ("Dark Web Check", self._dark_web_check),
            ("Generate Report", self._generate_report),
        ]

        for i, (name, func) in enumerate(steps, 1):
            print(f"{Colors.YELLOW}[{i}/10] {name}...{Colors.END}")
            try:
                func()
            except Exception as e:
                print(f"  {Colors.RED}✗ {str(e)[:60]}{Colors.END}")
            time.sleep(0.5)

    def _profile_intel(self):
        """Deep profile intelligence"""
        try:
            # Method 1: Web profile API
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target}"
            resp = self.session.get(url, timeout=15)

            if resp.status_code == 200:
                data = resp.json()
                user = data.get('data', {}).get('user', {})

                self.data['profile'] = {
                    'username': user.get('username'),
                    'full_name': user.get('full_name'),
                    'biography': user.get('biography', ''),
                    'followers': user.get('edge_followed_by', {}).get('count', 0),
                    'following': user.get('edge_follow', {}).get('count', 0),
                    'posts_count': user.get('edge_owner_to_timeline_media', {}).get('count', 0),
                    'is_private': user.get('is_private', False),
                    'is_verified': user.get('is_verified', False),
                    'is_business': user.get('is_business_account', False),
                    'is_professional': user.get('is_professional_account', False),
                    'category': user.get('category_name', ''),
                    'profile_pic_url': user.get('profile_pic_url_hd', ''),
                    'external_url': user.get('external_url', ''),
                    'has_highlight_reels': user.get('has_highlight_reels', False),
                    'has_guides': user.get('has_guides', False),
                    'is_joined_recently': user.get('is_joined_recently', False),
                    'business_email': user.get('business_email', ''),
                    'business_phone': user.get('business_phone_number', ''),
                    'business_address': user.get('business_address_json', ''),
                    'connected_fb_page': user.get('connected_fb_page', None),
                }

                p = self.data['profile']

                print(f"  {Colors.GREEN}✓{Colors.END} Name: {p['full_name'] or 'N/A'}")
                print(f"  {Colors.GREEN}✓{Colors.END} Followers: {p['followers']:,}")
                print(f"  {Colors.GREEN}✓{Colors.END} Following: {p['following']:,}")
                print(f"  {Colors.GREEN}✓{Colors.END} Posts: {p['posts_count']}")
                print(f"  {Colors.GREEN}✓{Colors.END} Verified: {'✅ YES' if p['is_verified'] else 'No'}")
                print(f"  {Colors.GREEN}✓{Colors.END} Private: {'🔒 YES' if p['is_private'] else '🌍 Public'}")
                print(f"  {Colors.GREEN}✓{Colors.END} Business: {'💼 YES' if p['is_business'] else 'No'}")

                if p['category']:
                    print(f"  {Colors.GREEN}✓{Colors.END} Category: {p['category']}")

                if p['biography']:
                    print(f"  {Colors.GREEN}✓{Colors.END} Bio: {p['biography'][:80]}...")

                # Save profile pic
                if p['profile_pic_url']:
                    self.data['profile_pic'] = p['profile_pic_url']
                    print(f"  {Colors.GREEN}✓{Colors.END} Profile pic URL saved")

            elif resp.status_code == 404:
                print(f"  {Colors.RED}✗ User not found{Colors.END}")
                self.data['profile'] = {'error': 'not_found'}
            else:
                print(f"  {Colors.YELLOW}!{Colors.END} Rate limited, trying alternate method...")
                self._profile_scrape_fallback()

        except Exception as e:
            print(f"  {Colors.RED}✗ {str(e)[:50]}{Colors.END}")
            self._profile_scrape_fallback()

    def _profile_scrape_fallback(self):
        """Fallback: scrape profile from HTML"""
        try:
            url = f"https://www.instagram.com/{self.target}/"
            resp = self.session.get(url, timeout=15)

            if resp.status_code == 200:
                html = resp.text

                # Extract JSON data from page
                import re
                match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
                if match:
                    ld_json = json.loads(match.group(1))
                    self.data['profile_ld'] = ld_json
                    print(f"  {Colors.GREEN}✓{Colors.END} Extracted from page metadata")

                # Check for og:description
                og_match = re.search(r'property="og:description" content="([^"]+)"', html)
                if og_match:
                    desc = og_match.group(1)
                    print(f"  {Colors.GREEN}✓{Colors.END} Meta: {desc[:60]}...")

        except Exception as e:
            print(f"  {Colors.RED}✗ Fallback failed: {str(e)[:40]}{Colors.END}")

    def _story_recon(self):
        """Story reconnaissance"""
        p = self.data.get('profile', {})

        if p.get('is_private'):
            print(f"  {Colors.YELLOW}!{Colors.END} Private account — story access limited")
            return

        try:
            url = f"https://www.instagram.com/{self.target}/"
            resp = self.session.get(url, timeout=10)

            if resp.status_code == 200:
                html = resp.text

                has_story = any(ind in html for ind in [
                    '"hasActiveStory":true',
                    '"has_story":true',
                    '"latest_reel_media"'
                ])

                self.data['stories'] = {
                    'has_active_story': has_story,
                    'story_url': f"https://www.instagram.com/stories/{self.target}/" if has_story else None,
                    'highlights': p.get('has_highlight_reels', False),
                }

                if has_story:
                    print(f"  {Colors.GREEN}✓ 🔥 ACTIVE STORY DETECTED!{Colors.END}")
                    print(f"  {Colors.CYAN}→{Colors.END} {self.data['stories']['story_url']}")
                else:
                    print(f"  {Colors.YELLOW}!{Colors.END} No active story")

                if p.get('has_highlight_reels'):
                    print(f"  {Colors.GREEN}✓{Colors.END} Has highlight reels")

        except Exception as e:
            print(f"  {Colors.RED}✗ {str(e)[:40]}{Colors.END}")

    def _post_analysis(self):
        """Deep post analysis"""
        p = self.data.get('profile', {})

        try:
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target}"
            resp = self.session.get(url, timeout=15)

            if resp.status_code == 200:
                data = resp.json()
                user = data.get('data', {}).get('user', {})
                edges = user.get('edge_owner_to_timeline_media', {}).get('edges', [])

                self.data['posts'] = []
                all_hashtags = []
                all_locations = []
                post_times = []

                for edge in edges[:18]:
                    node = edge.get('node', {})

                    caption_edges = node.get('edge_media_to_caption', {}).get('edges', [])
                    caption = caption_edges[0].get('node', {}).get('text', '') if caption_edges else ''

                    likes = node.get('edge_media_preview_like', {}).get('count', 0)
                    comments = node.get('edge_media_to_comment', {}).get('count', 0)
                    timestamp = node.get('taken_at_timestamp', 0)
                    location = node.get('location', {})
                    is_video = node.get('is_video', False)
                    display_url = node.get('display_url', '')
                    shortcode = node.get('shortcode', '')

                    tags = re.findall(r'#(\w+)', caption)
                    all_hashtags.extend(tags)

                    if location:
                        all_locations.append(location.get('name', 'Unknown'))

                    if timestamp:
                        post_times.append(datetime.fromtimestamp(timestamp))

                    self.data['posts'].append({
                        'shortcode': shortcode,
                        'caption': caption[:150],
                        'likes': likes,
                        'comments': comments,
                        'hashtags': tags,
                        'location': location.get('name') if location else None,
                        'is_video': is_video,
                        'display_url': display_url,
                        'post_url': f"https://www.instagram.com/p/{shortcode}/" if shortcode else None,
                        'date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M') if timestamp else 'N/A',
                    })

                # Analytics
                if self.data['posts']:
                    total_likes = sum(p['likes'] for p in self.data['posts'])
                    total_comments = sum(p['comments'] for p in self.data['posts'])
                    avg_likes = total_likes / len(self.data['posts'])

                    self.data['post_analytics'] = {
                        'total_posts_analyzed': len(self.data['posts']),
                        'total_likes': total_likes,
                        'total_comments': total_comments,
                        'avg_likes': round(avg_likes, 2),
                        'avg_comments': round(total_comments / len(self.data['posts']), 2),
                    }

                    # Engagement rate
                    if p.get('followers', 0) > 0:
                        engagement = (avg_likes / p['followers']) * 100
                        self.data['engagement_rate'] = round(engagement, 2)
                        print(f"  {Colors.GREEN}✓{Colors.END} Engagement Rate: {engagement:.2f}%")

                    # Posting pattern
                    if post_times:
                        hours = [t.hour for t in post_times]
                        most_active_hour = max(set(hours), key=hours.count)
                        self.data['most_active_hour'] = most_active_hour
                        print(f"  {Colors.GREEN}✓{Colors.END} Most active at: {most_active_hour}:00")

                    print(f"  {Colors.GREEN}✓{Colors.END} Analyzed {len(self.data['posts'])} posts")
                    print(f"  {Colors.GREEN}✓{Colors.END} Total likes: {total_likes:,}")

                # Top hashtags
                if all_hashtags:
                    from collections import Counter
                    top_tags = Counter(all_hashtags).most_common(10)
                    self.data['top_hashtags'] = top_tags
                    print(f"  {Colors.GREEN}✓{Colors.END} Top hashtags: {', '.join([t[0] for t in top_tags[:5]])}")

                # Locations
                if all_locations:
                    self.data['post_locations'] = list(set(all_locations))
                    print(f"  {Colors.GREEN}✓{Colors.END} Locations: {', '.join(set(all_locations))}")

        except Exception as e:
            print(f"  {Colors.RED}✗ {str(e)[:50]}{Colors.END}")

    def _follower_intel(self):
        """Follower intelligence"""
        p = self.data.get('profile', {})

        followers = p.get('followers', 0)
        following = p.get('following', 0)

        if following > 0:
            ratio = followers / following
            self.data['follower_ratio'] = round(ratio, 2)

            print(f"  {Colors.GREEN}✓{Colors.END} Follower/Following Ratio: {ratio:.2f}")

            if ratio > 100:
                account_type = "Mega Influencer/Celebrity 🌟"
            elif ratio > 10:
                account_type = "Influencer/Public Figure ⭐"
            elif ratio > 1:
                account_type = "Popular Account 👍"
            elif ratio > 0.5:
                account_type = "Regular User 👤"
            else:
                account_type = "Engaged User (follows many) 🔍"

            self.data['account_type'] = account_type
            print(f"  {Colors.GREEN}✓{Colors.END} Account Type: {account_type}")

        # Follower quality estimate
        if followers > 0 and self.data.get('engagement_rate'):
            er = self.data['engagement_rate']
            if er < 1:
                quality = "Possible fake/bot followers ⚠️"
            elif er < 3:
                quality = "Average engagement"
            elif er < 6:
                quality = "Good engagement ✅"
            else:
                quality = "Excellent engagement 🔥"

            self.data['follower_quality'] = quality
            print(f"  {Colors.GREEN}✓{Colors.END} Follower Quality: {quality}")

    def _contact_extraction(self):
        """Extract all contact info"""
        p = self.data.get('profile', {})
        bio = p.get('biography', '')

        found = []

        # Business contact
        if p.get('business_email'):
            self.data['business_email'] = p['business_email']
            found.append(f"Business Email: {p['business_email']}")

        if p.get('business_phone'):
            self.data['business_phone'] = p['business_phone']
            found.append(f"Business Phone: {p['business_phone']}")

        # Email in bio
        email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', bio)
        if email:
            self.data['bio_email'] = email.group()
            found.append(f"Bio Email: {email.group()}")

        # Phone in bio
        phone = re.search(r'(\+?\d[\d\s\-\(\)]{8,15}\d)', bio)
        if phone:
            self.data['bio_phone'] = phone.group()
            found.append(f"Bio Phone: {phone.group()}")

        # External URL
        ext_url = p.get('external_url', '')
        if ext_url:
            self.data['external_url'] = ext_url
            found.append(f"Website: {ext_url}")

            # Try to extract more from website
            try:
                r = self.session.get(ext_url, timeout=5)
                if r.status_code == 200:
                    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text)
                    if emails:
                        self.data['website_emails'] = list(set(emails))[:5]
                        found.append(f"Website Emails: {len(set(emails))} found")
            except:
                pass

        # WhatsApp/Telegram in bio
        wa = re.search(r'(?:wa\.me/|whatsapp:\s*)(\+?\d+)', bio)
        if wa:
            self.data['whatsapp'] = wa.group(1)
            found.append(f"WhatsApp: {wa.group(1)}")

        tg = re.search(r'(?:t\.me/|@)(\w{5,})', bio)
        if tg:
            self.data['telegram'] = tg.group(1)
            found.append(f"Telegram: @{tg.group(1)}")

        if found:
            for f in found:
                print(f"  {Colors.GREEN}✓{Colors.END} {f}")
        else:
            print(f"  {Colors.YELLOW}!{Colors.END} No direct contacts found")

    def _social_mapping(self):
        """Map all social media accounts"""
        platforms = {
            'Twitter/X': ('https://twitter.com/{}', 'https://x.com/{}'),
            'Facebook': ('https://facebook.com/{}',),
            'TikTok': ('https://tiktok.com/@{}',),
            'YouTube': ('https://youtube.com/@{}', 'https://youtube.com/c/{}', 'https://youtube.com/{}'),
            'Snapchat': ('https://snapchat.com/add/{}',),
            'Pinterest': ('https://pinterest.com/{}',),
            'LinkedIn': ('https://linkedin.com/in/{}',),
            'GitHub': ('https://github.com/{}',),
            'Telegram': ('https://t.me/{}',),
            'Reddit': ('https://reddit.com/user/{}',),
            'Twitch': ('https://twitch.tv/{}',),
            'Spotify': ('https://open.spotify.com/user/{}',),
            'Discord': ('https://discord.com/users/{}',),
            'Medium': ('https://medium.com/@{}',),
            'Behance': ('https://behance.net/{}',),
        }

        self.data['social_accounts'] = {}
        found_count = 0

        for platform, urls in platforms.items():
            for url_template in urls:
                try:
                    url = url_template.format(self.target)
                    r = self.session.head(url, timeout=5, allow_redirects=True)
                    if r.status_code == 200:
                        self.data['social_accounts'][platform] = url
                        found_count += 1
                        print(f"  {Colors.GREEN}✓{Colors.END} {platform}: FOUND ✅")
                        break
                except:
                    continue

        if found_count == 0:
            print(f"  {Colors.YELLOW}!{Colors.END} No linked accounts found")
        else:
            print(f"  {Colors.GREEN}✓{Colors.END} Total found: {found_count} accounts")

    def _photo_forensics(self):
        """Photo forensics"""
        p = self.data.get('profile', {})

        if p.get('profile_pic_url'):
            self.data['photos'] = {
                'profile_pic': p['profile_pic_url'],
                'post_photos': [post.get('display_url') for post in self.data.get('posts', []) if post.get('display_url')][:5]
            }
            print(f"  {Colors.GREEN}✓{Colors.END} Profile photo URL saved")
            print(f"  {Colors.GREEN}✓{Colors.END} {len(self.data['photos']['post_photos'])} post photos extracted")

    def _behavioral_analysis(self):
        """Behavioral analysis"""
        posts = self.data.get('posts', [])
        p = self.data.get('profile', {})

        if not posts:
            print(f"  {Colors.YELLOW}!{Colors.END} Not enough data for behavioral analysis")
            return

        analysis = {}

        # Activity pattern
        if self.data.get('most_active_hour'):
            hour = self.data['most_active_hour']
            if 6 <= hour < 12:
                activity = "Morning person ☀️"
            elif 12 <= hour < 18:
                activity = "Afternoon active 🌤️"
            elif 18 <= hour < 23:
                activity = "Evening/night person 🌙"
            else:
                activity = "Night owl 🦉"
            analysis['activity_pattern'] = activity
            print(f"  {Colors.GREEN}✓{Colors.END} Activity: {activity}")

        # Interests from hashtags
        if self.data.get('top_hashtags'):
            interests = [tag[0] for tag in self.data['top_hashtags'][:5]]
            analysis['interests'] = interests
            print(f"  {Colors.GREEN}✓{Colors.END} Interests: {', '.join(interests)}")

        # Content type
        videos = sum(1 for post in posts if post.get('is_video'))
        images = len(posts) - videos
        if videos > images:
            content_type = "Video creator 🎥"
        else:
            content_type = "Photo poster 📸"
        analysis['content_type'] = content_type
        print(f"  {Colors.GREEN}✓{Colors.END} Content type: {content_type}")

        # Privacy awareness
        if p.get('is_private'):
            privacy = "Privacy conscious 🔒"
        else:
            privacy = "Public profile 🌍"
        analysis['privacy'] = privacy
        print(f"  {Colors.GREEN}✓{Colors.END} Privacy: {privacy}")

        self.data['behavioral'] = analysis

    def _dark_web_check(self):
        """Check if email/phone appears in breaches"""
        email = self.data.get('bio_email') or self.data.get('business_email')

        if not email:
            print(f"  {Colors.YELLOW}!{Colors.END} No email to check")
            return

        try:
            # HaveIBeenPwned style check (simplified)
            domain = email.split('@')[1]
            print(f"  {Colors.GREEN}✓{Colors.END} Email domain: {domain}")
            print(f"  {Colors.YELLOW}!{Colors.END} Breach check requires API key (optional feature)")

            self.data['breach_check'] = {
                'email': email,
                'domain': domain,
                'checked': False,
                'note': 'Add HIBP API key for full breach check'
            }
        except:
            pass

    def _generate_report(self):
        """Generate final intelligence report"""
        print(f"\n{Colors.PURPLE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.WHITE}👁️  FINAL INTELLIGENCE REPORT — @{self.target}{Colors.END}")
        print(f"{Colors.PURPLE}{'='*70}{Colors.END}\n")

        p = self.data.get('profile', {})

        # Header
        print(f"{Colors.RED}{Colors.BOLD}╔══════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}║           TARGET PROFILE                     ║{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}╚══════════════════════════════════════════════╝{Colors.END}\n")

        print(f"  {Colors.CYAN}Username:{Colors.END}     @{p.get('username', self.target)}")
        print(f"  {Colors.CYAN}Full Name:{Colors.END}    {p.get('full_name', 'N/A')}")
        print(f"  {Colors.CYAN}Followers:{Colors.END}    {p.get('followers', 0):,}")
        print(f"  {Colors.CYAN}Following:{Colors.END}    {p.get('following', 0):,}")
        print(f"  {Colors.CYAN}Posts:{Colors.END}        {p.get('posts_count', 0)}")
        print(f"  {Colors.CYAN}Verified:{Colors.END}     {'✅ YES' if p.get('is_verified') else '❌ No'}")
        print(f"  {Colors.CYAN}Private:{Colors.END}      {'🔒 YES' if p.get('is_private') else '🌍 Public'}")
        print(f"  {Colors.CYAN}Business:{Colors.END}     {'💼 YES' if p.get('is_business') else '❌ No'}")

        if p.get('category'):
            print(f"  {Colors.CYAN}Category:{Colors.END}     {p['category']}")

        # Contacts
        print(f"\n{Colors.YELLOW}{Colors.BOLD}📧 CONTACT INFORMATION{Colors.END}")
        contacts = [
            ('Business Email', self.data.get('business_email')),
            ('Bio Email', self.data.get('bio_email')),
            ('Business Phone', self.data.get('business_phone')),
            ('Bio Phone', self.data.get('bio_phone')),
            ('Website', self.data.get('external_url')),
            ('WhatsApp', self.data.get('whatsapp')),
            ('Telegram', self.data.get('telegram')),
        ]
        for label, value in contacts:
            if value:
                print(f"  {Colors.GREEN}✓{Colors.END} {label}: {value}")

        # Website emails
        if self.data.get('website_emails'):
            print(f"\n{Colors.YELLOW}Website Emails:{Colors.END}")
            for email in self.data['website_emails']:
                print(f"  {Colors.GREEN}→{Colors.END} {email}")

        # Social accounts
        print(f"\n{Colors.YELLOW}{Colors.BOLD}🔗 LINKED ACCOUNTS{Colors.END}")
        if self.data.get('social_accounts'):
            for platform, url in self.data['social_accounts'].items():
                print(f"  {Colors.GREEN}✓{Colors.END} {platform}: {url}")
        else:
            print(f"  {Colors.YELLOW}!{Colors.END} None found")

        # Location
        print(f"\n{Colors.YELLOW}{Colors.BOLD}📍 LOCATION DATA{Colors.END}")
        if self.data.get('post_locations'):
            print(f"  {Colors.GREEN}✓{Colors.END} From posts: {', '.join(self.data['post_locations'])}")
        bio_location = self._extract_location_from_bio(p.get('biography', ''))
        if bio_location:
            print(f"  {Colors.GREEN}✓{Colors.END} From bio: {bio_location}")

        # Analytics
        print(f"\n{Colors.YELLOW}{Colors.BOLD}📊 ANALYTICS{Colors.END}")
        if self.data.get('engagement_rate'):
            print(f"  {Colors.GREEN}✓{Colors.END} Engagement Rate: {self.data['engagement_rate']}%")
        if self.data.get('follower_ratio'):
            print(f"  {Colors.GREEN}✓{Colors.END} Follower Ratio: {self.data['follower_ratio']}")
        if self.data.get('account_type'):
            print(f"  {Colors.GREEN}✓{Colors.END} Account Type: {self.data['account_type']}")
        if self.data.get('follower_quality'):
            print(f"  {Colors.GREEN}✓{Colors.END} Follower Quality: {self.data['follower_quality']}")

        # Behavioral
        print(f"\n{Colors.YELLOW}{Colors.BOLD}🧠 BEHAVIORAL PROFILE{Colors.END}")
        b = self.data.get('behavioral', {})
        if b.get('activity_pattern'):
            print(f"  {Colors.GREEN}✓{Colors.END} Activity: {b['activity_pattern']}")
        if b.get('interests'):
            print(f"  {Colors.GREEN}✓{Colors.END} Interests: {', '.join(b['interests'])}")
        if b.get('content_type'):
            print(f"  {Colors.GREEN}✓{Colors.END} Content: {b['content_type']}")
        if b.get('privacy'):
            print(f"  {Colors.GREEN}✓{Colors.END} Privacy: {b['privacy']}")

        # Stories
        print(f"\n{Colors.YELLOW}{Colors.BOLD}📱 STORIES{Colors.END}")
        s = self.data.get('stories', {})
        if s.get('has_active_story'):
            print(f"  {Colors.GREEN}✓ 🔥 ACTIVE STORY!{Colors.END}")
            print(f"  {Colors.CYAN}→{Colors.END} {s.get('story_url')}")
        else:
            print(f"  {Colors.YELLOW}!{Colors.END} No active story")

        # Hashtags
        if self.data.get('top_hashtags'):
            print(f"\n{Colors.YELLOW}{Colors.BOLD}#️⃣ TOP HASHTAGS{Colors.END}")
            for tag, count in self.data['top_hashtags'][:10]:
                print(f"  {Colors.GREEN}#{Colors.END}{tag} ({count}x)")

        # Posts
        if self.data.get('posts'):
            print(f"\n{Colors.YELLOW}{Colors.BOLD}📝 RECENT POSTS{Colors.END}")
            for post in self.data['posts'][:5]:
                print(f"  {Colors.CYAN}→{Colors.END} {post.get('date', 'N/A')} | ❤️ {post.get('likes', 0)} | 💬 {post.get('comments', 0)}")
                if post.get('caption'):
                    print(f"    {post['caption'][:60]}...")

        # Photos
        print(f"\n{Colors.YELLOW}{Colors.BOLD}📸 PHOTOS{Colors.END}")
        if self.data.get('photos'):
            print(f"  {Colors.GREEN}✓{Colors.END} Profile pic: Available")
            print(f"  {Colors.GREEN}✓{Colors.END} Post photos: {len(self.data['photos'].get('post_photos', []))} extracted")

        # Save report
        report_file = f"insta_spy_report_{self.target}_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)

        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Full report saved: {report_file}{Colors.END}")

        # Footer
        print(f"\n{Colors.PURPLE}{'='*70}{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}  👁️  INSTA-SPY v2.0 — THE EYE: MAXIMUM POWER{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}  Built by worm shadow for He{Colors.END}")
        print(f"{Colors.PURPLE}{'='*70}{Colors.END}")

    def _extract_location_from_bio(self, bio: str) -> str:
        """Extract location from bio text"""
        patterns = [
            r'(?:from|in|based\s+in|living\s+in|located\s+in)\s+([A-Za-z\s,]+?)(?:\s*[,;.📍🌍]|$)',
            r'📍\s*([A-Za-z\s,]+?)(?:\s*[,;.]|$)',
            r'🌍\s*([A-Za-z\s,]+?)(?:\s*[,;.]|$)',
            r'🏠\s*([A-Za-z\s,]+?)(?:\s*[,;.]|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, bio, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

def main():
    if len(sys.argv) < 2:
        print(f"{Colors.YELLOW}Usage: python3 insta-spy.py <username>{Colors.END}")
        print(f"{Colors.YELLOW}Example: python3 insta-spy.py zuck{Colors.END}")
        print(f"\n{Colors.CYAN}For iSH iPhone:{Colors.END}")
        print(f"  pip install requests")
        print(f"  python3 insta-spy.py target_username")
        sys.exit(1)

    username = sys.argv[1]

    spy = InstaSpyMax()
    spy.banner()
    spy.scan(username)

if __name__ == '__main__':
    main()
