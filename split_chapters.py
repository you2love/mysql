#!/usr/bin/env python3
"""Split index.html into individual chapter files."""

import re
import os

# Read the main HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract head section (styles, scripts, etc.)
head_match = re.search(r'(<head>.*?</head>)', content, re.DOTALL)
if head_match:
    head_content = head_match.group(1)
else:
    head_content = ''

# Extract body header (sidebar, etc.)
body_start = content.find('<body>')
body_header_end = content.find('<section id="')

# Get the layout structure
layout_start = content.find('<div class="layout">')
layout_header = content[body_start:layout_start + len('<div class="layout">')]

# Also need to get the sidebar structure
sidebar_match = re.search(r'(<aside class="sidebar">.*?</aside>)', content, re.DOTALL)
if sidebar_match:
    sidebar = sidebar_match.group(1)

# Get all sections
section_pattern = r'<section id="([^"]+)" class="section">(.*?)</section>'
sections = re.findall(section_pattern, content, re.DOTALL)

print(f"Found {len(sections)} sections:")
for sid, _ in sections:
    print(f"  - {sid}")

# Chapter files to create (in order)
chapter_order = [
    'introduction', 'installation', 'basics', 'advanced',
    'sql-theory', 'index-theory', 'performance', 'backup',
    'security', 'alternatives', 'history', 'ai', 'practice'
]

# Create a chapter file
def create_chapter_file(section_id, section_content, order):
    """Create a standalone HTML file for a chapter."""

    # Generate navigation for this chapter
    nav_items = []
    for i, cid in enumerate(order):
        if cid == section_id:
            nav_items.append(f'<li class="current"><a href="#">{get_title(cid)}</a></li>')
        else:
            nav_items.append(f'<li><a href="{cid}.html">{get_title(cid)}</a></li>')

    nav_html = '\n'.join(nav_items)

    chapter_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{get_title(section_id)} - MySQL 教程</title>
    <link rel="icon" href="../favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="../styles.css">
    <script src="../mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default'
        }});
    </script>
</head>
<body>
    <div class="layout">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1><a href="../index.html">MySQL 教程</a></h1>
            </div>
            <nav class="tree-nav">
                <ul class="tree">
                    {nav_html}
                </ul>
            </nav>
        </aside>
        <main class="main-content">
            <section id="{section_id}" class="section">
                <h2>{get_title(section_id)}</h2>
                <div class="content">
{section_content}
                </div>
            </section>
        </main>
    </div>
</body>
</html>'''

    filename = f"chapters/{section_id}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(chapter_html)
    print(f"Created: {filename}")

def get_title(section_id):
    """Get chapter title from section id."""
    titles = {
        'introduction': '什么是 MySQL？',
        'installation': '安装与配置',
        'basics': '基础操作',
        'advanced': '高级特性',
        'sql-theory': 'SQL原理',
        'index-theory': '索引原理',
        'performance': '性能优化',
        'backup': '备份与恢复',
        'security': '安全特性',
        'alternatives': 'MySQL 替代品',
        'history': '发展历程',
        'ai': 'AI 增强',
        'practice': '实战练习'
    }
    return titles.get(section_id, section_id)

# Create each chapter file
for section_id, section_content in sections:
    if section_id in chapter_order:
        create_chapter_file(section_id, section_content.strip(), chapter_order)

print("\nDone! All chapter files created.")
print("Now creating main index.html...")

# Create main index.html with links to all chapters
nav_items_index = []
for cid in chapter_order:
    nav_items_index.append(f'<li><a href="chapters/{cid}.html">{get_title(cid)}</a></li>')

nav_html_index = '\n'.join(nav_items_index)

# Read original index content for introduction section
intro_match = re.search(r'<section id="introduction" class="section">(.*?)</section>', content, re.DOTALL)
if intro_match:
    intro_content = intro_match.group(1).strip()

index_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MySQL 学习教程 - 从入门到精通</title>
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="styles.css">
    <script src="mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default'
        }});
    </script>
</head>
<body>
    <div class="layout">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1>MySQL 教程</h1>
            </div>
            <nav class="tree-nav">
                <ul class="tree">
                    {nav_html_index}
                </ul>
            </nav>
        </aside>
        <main class="main-content">
            <section id="introduction" class="section">
                <h2>什么是 MySQL？</h2>
                <div class="content">
{intro_content}
                </div>
            </section>
        </main>
    </div>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("Created: index.html (entry point with navigation)")
print("\nAll files created successfully!")
