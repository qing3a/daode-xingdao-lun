# -*- coding: utf-8 -*-
"""从 道德经-行道论.md 生成阅读器书籍数据 行道论.json

结构：前言、总章（chapter=0 的开篇卡片）+ 81 章正文
每章：行道版正文区块（现象/建模/策略/评论/说明/专题/系统动态图）+ 注释 + 备注
"""
import re
import json

MD = '道德经-行道论.md'
OUT = '行道论.json'

md = open(MD, encoding='utf-8').read()
lines = md.split('\n')

chap_re = re.compile(r'^#{0,3} *\**第([一二三四五六七八九十百]+)章（([^）]*)）\**$')
marker_re = {
    'notes': re.compile(r'^注释[:：](.*)$'),
    'remarks': re.compile(r'^备注[:：](.*)$'),
    'dynamic': re.compile(r'^(?:系统动态图|动态图)[:：](.*)$'),
    'explain': re.compile(r'^说明[:：](.*)$'),
    'topic': re.compile(r'^专题[:：](.*)$'),
    'labeled': re.compile(r'^【([^】]+)】\s*(.*)$'),
}

def new_chapter(num, title):
    return {'chapter': num, 'title': title,
            'sections': {'content': [], 'notes': [], 'remarks': []}}

chapters = []
frontmatter = []          # 开篇段落（前言/总章的正文行，chapter=0）
front_title = None        # 当前开篇块标题（前言 / 总章）
cur = None
mode = None
current_section = None

def flush_frontmatter():
    """把收集到的开篇段落按块输出为卡片（前言 / 总章），随后清空"""
    global front_title, current_section, frontmatter
    for blk_title, paras in frontmatter:
        if not paras:
            continue
        ch = new_chapter(0, blk_title)
        ch['sections']['content'] = [{'label': '正文', 'text': '\n\n'.join(paras)}]
        chapters.append(ch)
    frontmatter = []

for raw in lines:
    line = raw.strip()
    if not line:
        continue

    # 章节标题
    m = chap_re.match(line)
    if m:
        flush_frontmatter()
        cur = new_chapter(m.group(1), m.group(2).replace('*', '').strip())
        chapters.append(cur)
        mode = None
        current_section = None
        continue

    # 开篇块：前言 / 总章（在第一章之前）
    if cur is None:
        if line == '**前言**' or line == '**总章**':
            front_title = line.replace('**', '')
            frontmatter.append([front_title, []])
        elif front_title and line.startswith('**') and line.endswith('**'):
            front_title = line.replace('**', '')
            frontmatter.append([front_title, []])
        elif frontmatter:
            # 开篇正文行
            frontmatter[-1][1].append(line.replace('**', ''))
        continue

    if line.startswith('行道版'):
        continue
    if m := marker_re['notes'].match(line):
        mode, current_section = 'notes', None
        rest = m.group(1).strip()
        if rest:
            cur['sections']['notes'].append(rest.replace('**', ''))
        continue
    if m := marker_re['remarks'].match(line):
        mode, current_section = 'remarks', None
        rest = m.group(1).strip()
        if rest:
            cur['sections']['remarks'].append(rest.replace('**', ''))
        continue
    if m := marker_re['dynamic'].match(line):
        mode = None
        current_section = {'label': '系统动态图', 'text': m.group(1).strip()}
        cur['sections']['content'].append(current_section)
        continue
    if m := marker_re['explain'].match(line):
        mode = None
        current_section = {'label': '说明', 'text': m.group(1).strip()}
        cur['sections']['content'].append(current_section)
        continue
    if m := marker_re['topic'].match(line):
        mode = None
        current_section = {'label': '专题', 'text': m.group(1).strip()}
        cur['sections']['content'].append(current_section)
        continue
    if m := marker_re['labeled'].match(line):
        mode = None
        current_section = {'label': m.group(1), 'text': m.group(2).strip()}
        cur['sections']['content'].append(current_section)
        continue
    if mode == 'notes':
        cur['sections']['notes'].append(line.replace('**', ''))
        continue
    if mode == 'remarks':
        cur['sections']['remarks'].append(line.replace('**', ''))
        continue
    text = line.replace('**', '')
    if current_section is not None:
        current_section['text'] = (current_section['text'] + '\n' + text).strip()
    else:
        current_section = {'label': '正文', 'text': text}
        cur['sections']['content'].append(current_section)

flush_frontmatter()

# 清理空区块
for ch in chapters:
    ch['sections']['content'] = [s for s in ch['sections']['content'] if s['text']]

book = {
    'metadata': {'title': '行道论', 'author': '青山',
                 'description': '新版-行道论：对《道德经》的逐章再阐释'},
    'content': chapters
}

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(book, f, ensure_ascii=False, indent=2)

print(f"生成 {OUT}：共 {len(chapters)} 个条目")
for ch in chapters[:3]:
    n = len(ch['sections']['content'])
    print(f"  [{ch['chapter']}] {ch['title']} —— {n} 个正文区块")
