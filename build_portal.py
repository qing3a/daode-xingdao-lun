# -*- coding: utf-8 -*-
"""生成总站首页 index.html（作者作品总站门户）"""

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="青山 · 作品总站：以系统与生存的语言重读经典。首部作品《新版-行道论》。">
    <title>青山 · 作品总站</title>
    <style>
        :root {
            --primary: #8c2f1b;
            --secondary: #5c3c10;
            --border: #d4b483;
            --bg: #f9f3e6;
            --card: #fff9e6;
            --highlight: #fff0d9;
            --text: #333;
            --muted: #666;
            --divider: rgba(212,180,131,0.35);
            --shadow: rgba(212,180,131,0.25);
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --primary: #d48c7b;
                --secondary: #b49c70;
                --border: #8c6c43;
                --bg: #1a1406;
                --card: #25200d;
                --highlight: #352d13;
                --text: #e6e6e6;
                --muted: #b3b3b3;
                --divider: rgba(140,108,67,0.35);
                --shadow: rgba(0,0,0,0.4);
            }
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        html { scroll-behavior:smooth; }
        body {
            font-family: "楷体","STKaiti","KaiTi",serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.8;
            -webkit-font-smoothing: antialiased;
        }
        a { color: inherit; text-decoration: none; }

        .nav {
            position: sticky; top:0; z-index:100;
            background: color-mix(in srgb, var(--bg) 88%, transparent);
            backdrop-filter: blur(8px);
            border-bottom: 1px solid var(--divider);
        }
        .nav-inner {
            max-width: 980px; margin: 0 auto; padding: 12px 24px;
            display: flex; align-items: center; gap: 18px;
        }
        .nav-brand { font-weight: bold; color: var(--primary); letter-spacing: 1px; white-space: nowrap; }
        .nav-links { display: flex; gap: 16px; margin-left: auto; }
        .nav-links a { font-size: 0.92rem; color: var(--muted); }
        .nav-links a:hover { color: var(--primary); }
        .nav-read {
            padding: 6px 14px; border-radius: 4px;
            background: var(--primary); color: #fff;
            font-size: 0.9rem; white-space: nowrap;
        }
        .nav-read:hover { filter: brightness(1.1); }

        .hero {
            text-align: center;
            padding: 84px 24px 52px;
            max-width: 820px; margin: 0 auto;
        }
        .eyebrow {
            display: inline-block;
            font-size: 0.85rem; letter-spacing: 4px;
            color: var(--secondary);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 4px 18px;
            background: var(--card);
        }
        .hero h1 {
            font-size: 3.4rem; margin: 26px 0 12px;
            color: var(--primary); letter-spacing: 10px;
        }
        .hero .subtitle { font-size: 1.05rem; color: var(--muted); }
        .hero .divider {
            width: 72px; height: 2px; margin: 26px auto;
            background: linear-gradient(90deg, transparent, var(--border), transparent);
        }
        .hero-quote { font-size: 1.05rem; color: var(--secondary); }

        section { max-width: 980px; margin: 0 auto; padding: 56px 24px; }
        .sec-head { text-align: center; margin-bottom: 36px; }
        .sec-index {
            display: inline-block; font-size: 0.8rem; letter-spacing: 3px;
            color: var(--primary); margin-bottom: 8px;
        }
        .sec-head h2 { font-size: 1.7rem; color: var(--primary); letter-spacing: 4px; }
        .sec-head p { color: var(--muted); font-size: 0.95rem; margin-top: 8px; }

        .work-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 24px;
            max-width: 860px; margin: 0 auto;
        }
        .work-card {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 14px; padding: 30px;
            position: relative;
            transition: transform .25s, box-shadow .25s;
        }
        .work-card:hover { transform: translateY(-3px); box-shadow: 0 10px 24px var(--shadow); }
        .work-badge {
            position: absolute; top: -12px; left: 24px;
            background: var(--primary); color: #fff;
            font-size: 0.75rem; letter-spacing: 2px;
            padding: 3px 14px; border-radius: 12px;
        }
        .work-card h3 { font-size: 1.5rem; color: var(--primary); letter-spacing: 3px; margin: 6px 0 6px; }
        .work-sub { color: var(--secondary); font-size: 0.95rem; margin-bottom: 12px; }
        .work-desc { color: var(--muted); font-size: 0.95rem; }
        .work-tags { margin: 16px 0 20px; display: flex; flex-wrap: wrap; gap: 8px; }
        .work-tags .tag {
            font-size: 0.8rem; color: var(--secondary);
            border: 1px solid var(--border); border-radius: 14px;
            padding: 2px 12px; background: var(--bg);
        }
        .work-actions { display: flex; gap: 12px; flex-wrap: wrap; }
        .btn {
            padding: 10px 26px; border-radius: 6px; font-size: 1rem;
            font-family: inherit; letter-spacing: 2px;
            transition: transform .2s, box-shadow .2s;
        }
        .btn-primary { background: var(--primary); color: #fff; box-shadow: 0 4px 14px var(--shadow); }
        .btn-ghost { border: 1px solid var(--border); color: var(--secondary); background: var(--bg); }
        .btn:hover { transform: translateY(-2px); }

        .work-card.placeholder {
            border-style: dashed;
            display: flex; flex-direction: column; justify-content: center;
            min-height: 280px; text-align: center;
        }
        .work-card.placeholder h3 { color: var(--muted); letter-spacing: 6px; }
        .work-card.placeholder .work-desc { font-size: 0.88rem; }

        .about-text { max-width: 700px; margin: 0 auto; font-size: 1.02rem; text-align: center; }
        .about-text p + p { margin-top: 14px; }

        footer {
            border-top: 1px solid var(--divider);
            padding: 36px 24px 48px; text-align: center;
            color: var(--muted); font-size: 0.88rem;
        }
        footer .flink { color: var(--primary); }
        @media (max-width: 600px) {
            .hero h1 { font-size: 2.4rem; letter-spacing: 6px; }
            .nav-links { display: none; }
        }
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-inner">
            <span class="nav-brand">青山 · 作品总站</span>
            <div class="nav-links">
                <a href="#works">作品</a>
                <a href="#about">关于</a>
            </div>
            <a class="nav-read" href="https://github.com/qing3a" target="_blank" rel="noopener">GitHub</a>
        </div>
    </nav>

    <header class="hero">
        <span class="eyebrow">个人作品总站</span>
        <h1>青山</h1>
        <p class="subtitle">以系统与生存的语言重读经典 · 以本地优先的架构构建工具</p>
        <div class="divider"></div>
        <div class="hero-quote">得与失的过程，就是生存与发展的过程。</div>
    </header>

    <main>
        <section id="works">
            <div class="sec-head">
                <span class="sec-index">一 · 作品</span>
                <h2>著作</h2>
            </div>
            <div class="work-grid">
                <div class="work-card">
                    <div class="work-badge">第一部</div>
                    <h3>新版-行道论</h3>
                    <p class="work-sub">对《道德经》的逐章再阐释 · 八十一章</p>
                    <p class="work-desc">以统一的词汇逐章重写《道德经》，标注每一句的结构角色——现象、建模、策略、评论；让两千年前的文本成为可检验、可实践的系统学说。</p>
                    <div class="work-tags">
                        <span class="tag">生存与发展</span>
                        <span class="tag">得与失</span>
                        <span class="tag">有无相生</span>
                        <span class="tag">81 章</span>
                    </div>
                    <div class="work-actions">
                        <a class="btn btn-primary" href="./行道论.html">书页详情</a>
                        <a class="btn btn-ghost" href="./道德经.html">在线阅读</a>
                    </div>
                </div>
                <div class="work-card">
                    <div class="work-badge">工具</div>
                    <h3>md-agent</h3>
                    <p class="work-sub">本地双层 MD 知识库 Agent · Rust</p>
                    <p class="work-desc">以 Markdown 为原生知识载体的本地 AI 知识 Agent——无向量库、ripgrep 全文检索、SQLite 知识图谱、网页终端交互；知识人写人读，AI 只负责整理、关联、推演、生成。</p>
                    <div class="work-tags">
                        <span class="tag">Rust</span>
                        <span class="tag">知识图谱</span>
                        <span class="tag">本地优先</span>
                        <span class="tag">待审机制</span>
                    </div>
                    <div class="work-actions">
                        <a class="btn btn-primary" href="https://qing3a.github.io/md-agent/" target="_blank" rel="noopener">项目主页</a>
                        <a class="btn btn-ghost" href="https://github.com/qing3a/md-agent" target="_blank" rel="noopener">GitHub 仓库</a>
                    </div>
                </div>
                <div class="work-card placeholder">
                    <h3>新作筹备中</h3>
                    <p class="work-desc">以系统与生存的视角，继续重读经典、整理实践。</p>
                </div>
            </div>
        </section>

        <section id="about">
            <div class="sec-head">
                <span class="sec-index">二 · 关于</span>
                <h2>作者</h2>
            </div>
            <div class="about-text">
                <p>青山，以系统与生存的视角重读经典、构建工具的创作者。文字作品以统一的概念系统贯穿始终，注重可实践、可检验；工具作品以本地优先、可审计为原则。</p>
                <p>个人作品，非学术翻译，不依从市面上的通解。原文仍是权威，作品只是陪伴阅读的一种方式。</p>
            </div>
        </section>
    </main>

    <footer>
        <p>青山 · 作品总站</p>
        <p style="margin-top:10px">
            <a class="flink" href="https://github.com/qing3a" target="_blank" rel="noopener">GitHub 主页</a>
            &nbsp;·&nbsp;
            <a class="flink" href="https://github.com/qing3a/daode-xingdao-lun" target="_blank" rel="noopener">行道论仓库</a>
        </p>
    </footer>
</body>
</html>
'''

open('index.html', 'w', encoding='utf-8').write(html)
print('index.html（作品总站）生成完成')
