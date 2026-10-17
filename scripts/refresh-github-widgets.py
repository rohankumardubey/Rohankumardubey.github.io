#!/usr/bin/env python3
"""Refresh committed profile cards; failed requests never replace good SVGs.

Run with an authenticated GitHub CLI (gh auth login locally, GH_TOKEN in Actions).
Only the activity graph needs authentication; no credentials go to widget hosts.
"""

import json
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

OUTPUT = Path(__file__).resolve().parents[1] / 'assets' / 'github'
USER = 'rohankumardubey'
COLORS = dict(bg_color='151A1E', title_color='D0BA91', text_color='B5BEC1',
              icon_color='D0BA91', border_color='3A4143', border_radius=12,
              disable_animations='true')
SVG_NS = '{http://www.w3.org/2000/svg}'


def card_sources():
    hosts = ['https://github-stats-extended.vercel.app',
             'https://github-readme-stats-one-bice.vercel.app']
    stats = dict(COLORS, username=USER, show_icons='true',
                 include_all_commits='true', card_width=495)
    langs = dict(COLORS, username=USER, layout='compact', langs_count=8,
                 hide='html,perl', card_width=495)
    streak = dict(user=USER, background='151A1E', border='3A4143',
                  border_radius=12, stroke='3A4143', ring='D0BA91',
                  fire='D0BA91', currStreakLabel='D0BA91',
                  sideLabels='B5BEC1', currStreakNum='F2F0E9',
                  sideNums='F2F0E9', dates='9CA7AC', disable_animations='true')
    return {
        'stats.svg': ([h + '/api?' + urlencode(stats) for h in hosts],
                      ['total stars', 'total prs']),
        'languages.svg': ([h + '/api/top-langs/?' + urlencode(langs) for h in hosts],
                          ['most used languages']),
        'streak.svg': (['https://streak-stats.demolab.com/?' + urlencode(streak)],
                       ['total contributions', 'current streak', 'longest streak']),
    }


def validate_svg(content, expected=()):
    root = ET.fromstring(content)
    if root.tag != SVG_NS + 'svg':
        raise ValueError('Response is not an SVG')
    if any(e.tag in {SVG_NS + 'script', SVG_NS + 'foreignObject'} for e in root.iter()):
        raise ValueError('SVG contains unsupported active content')
    text = ' '.join(' '.join(root.itertext()).lower().split())
    errors = ('something went wrong', 'rate limit', 'could not fetch',
              'failed to fetch', 'try again later', 'deployment has been disabled')
    if any(error in text for error in errors) or not all(label in text for label in expected):
        raise ValueError('Response is an error card or is missing expected statistics')


def fetch_card(url, expected):
    request = Request(url, headers={'User-Agent': 'rohan-profile-widgets/1.0',
                                    'Accept': 'image/svg+xml'})
    with urlopen(request, timeout=40) as response:
        if response.headers.get_content_type() != 'image/svg+xml':
            raise ValueError('Response has an unexpected content type')
        content = response.read(512_001)
    if len(content) > 512_000:
        raise ValueError('SVG exceeds the expected size')
    validate_svg(content, expected)
    return content


def save_card(name, content):
    validate_svg(content)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    target = OUTPUT / name
    temporary = target.with_suffix('.svg.tmp')
    temporary.write_bytes(content)
    temporary.replace(target)


def activity_days():
    # A repository's built-in GITHUB_TOKEN can query public contribution data.
    query = '''query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }'''
    result = subprocess.run(['gh', 'api', 'graphql', '-f', 'query=' + query,
                             '-f', 'login=' + USER], capture_output=True,
                            text=True, check=True, timeout=60)
    payload = json.loads(result.stdout)
    if payload.get('errors'):
        raise ValueError('GitHub returned a GraphQL error')
    weeks = payload['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    days = [day for week in weeks for day in week['contributionDays']]
    # The calendar sometimes includes padding days in its final week.
    today = datetime.now(timezone.utc).date()
    days = [d for d in days if date.fromisoformat(d['date']) <= today][-31:]
    if len(days) != 31:
        raise ValueError('GitHub returned an incomplete contribution window')
    for index, day in enumerate(days):
        if type(day['contributionCount']) is not int or day['contributionCount'] < 0:
            raise ValueError('Invalid contribution count')
        if index and date.fromisoformat(day['date']) - date.fromisoformat(days[index - 1]['date']) != timedelta(days=1):
            raise ValueError('Contribution dates are not consecutive')
    if date.fromisoformat(days[-1]['date']) != today:
        raise ValueError('GitHub returned stale contribution data')
    return days


def activity_svg(days):
    counts = [d['contributionCount'] for d in days]
    ceiling = max(4, ((max(counts) + 3) // 4) * 4)
    # Fixed zero baseline: daily counts are not a cumulative series.
    points = [(60 + i * 960 / 30, 246 - count * 144 / ceiling)
              for i, count in enumerate(counts)]
    polyline = ' '.join(f'{x:.1f},{y:.1f}' for x, y in points)
    area = '60,246 ' + polyline + ' 1020,246'
    total = sum(counts)
    title = 'Contribution signal'
    desc = f'{total} GitHub contributions from {days[0]["date"]} to {days[-1]["date"]}. Daily contributions, with a zero baseline.'
    fragments = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="330" viewBox="0 0 1080 330" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title><desc id="desc">{escape(desc)}</desc>
  <rect x="0.5" y="0.5" width="1079" height="329" rx="12" fill="#151A1E" stroke="#3A4143"/>
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <text x="30" y="39" fill="#D0BA91" font-size="20" font-weight="600">{title}</text>
    <text x="30" y="66" fill="#9CA7AC" font-size="13">Daily contributions · last 31 days · GitHub contribution calendar</text>
    <text x="1050" y="39" text-anchor="end" fill="#F2F0E9" font-size="22" font-weight="600">{total:,}</text>
    <text x="1050" y="63" text-anchor="end" fill="#9CA7AC" font-size="12">contributions in this window</text>''']
    for fraction in (0, 0.5, 1):
        y = 246 - fraction * 144
        fragments.append(f'<path d="M60 {y}H1020" stroke="#333A3E"/><text x="47" y="{y+4}" text-anchor="end" fill="#9CA7AC" font-size="11">{ceiling*fraction:g}</text>')
    fragments += [f'<polygon points="{area}" fill="#D0BA91" fill-opacity="0.08"/>',
                  f'<polyline points="{polyline}" fill="none" stroke="#D0BA91" stroke-width="2" stroke-linejoin="round"/>']
    for day, (x, y) in zip(days, points):
        fragments.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#D0BA91"><title>{day["date"]}: {day["contributionCount"]} contributions</title></circle>')
    for index in (0, 10, 20, 30):
        x = points[index][0]
        label = date.fromisoformat(days[index]['date']).strftime('%b %d')
        fragments.append(f'<text x="{x}" y="273" text-anchor="middle" fill="#9CA7AC" font-size="12">{label}</text>')
    fragments.append(f'<text x="30" y="310" fill="#9CA7AC" font-size="11">Updated {days[-1]["date"]} UTC · most recent day may be incomplete</text></g></svg>')
    return '\n'.join(fragments).encode()


def main():
    failures = []
    for name, (sources, expected) in card_sources().items():
        for url in sources:
            try:
                save_card(name, fetch_card(url, expected))
                print(f'Updated {name}')
                break
            except Exception as error:
                print(f'{name}: {error}', file=sys.stderr)
        else:
            failures.append(name)
    try:
        save_card('activity.svg', activity_svg(activity_days()))
        print('Updated activity.svg from GitHub')
    except Exception as error:
        print(f'activity.svg: {error}', file=sys.stderr)
        failures.append('activity.svg')
    if failures:
        print('Preserved existing cards after refresh failures: ' + ', '.join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
