#!/usr/bin/env python3
"""
移除 index.html 中 shell 代码块的所有 span 标签
"""

import re

def remove_shell_highlighting():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 移除 shell 代码块中的所有 span 标签
    def remove_spans(match):
        code = match.group(1)
        # 移除所有 span 标签（包括嵌套的）
        code = re.sub(r'<span[^>]*>', '', code)
        code = re.sub(r'</span>', '', code)
        return f'<pre><code class="sh">{code}</code></pre>'

    content = re.sub(r'<pre><code class="sh">(.*?)</code></pre>', remove_spans, content, flags=re.DOTALL)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("已移除 shell 代码块中的所有 span 标签")
    print("请运行以下命令重新添加语法高亮：")
    print("  python3 add_shell_highlighting.py")

if __name__ == '__main__':
    remove_shell_highlighting()
