#!/usr/bin/env python3
"""
Shell 语法高亮工具
为 index.html 中的 Shell 代码块添加 GitHub Light+ 配色的语法高亮标签
"""

import re
import sys

def highlight_shell(code):
    """
    为 Shell 代码添加语法高亮标签
    """
    # 定义 Shell 命令
    commands = [
        'sudo', 'apt', 'apt-get', 'dnf', 'yum', 'brew', 'docker', 'docker-compose',
        'mysql', 'mysql_secure_installation', 'systemctl', 'service', 'cd', 'ls',
        'pwd', 'mkdir', 'rm', 'cp', 'mv', 'cat', 'echo', 'grep', 'find', 'sed',
        'awk', 'tar', 'gzip', 'gunzip', 'chmod', 'chown', 'chgrp', 'ln', 'mv',
        'ps', 'kill', 'top', 'df', 'du', 'free', 'uptime', 'uname', 'whoami',
        'hostname', 'date', 'cal', 'ping', 'wget', 'curl', 'git', 'vim', 'nano',
        'less', 'more', 'head', 'tail', 'sort', 'uniq', 'wc', 'tr', 'cut',
        'paste', 'split', 'tee', 'xargs', 'ssh', 'scp', 'rsync', 'nc', 'netstat',
        'ifconfig', 'ip', 'route', 'ping', 'traceroute', 'nslookup', 'dig',
        'mount', 'umount', 'fdisk', 'mkfs', 'df', 'du', 'free', 'top', 'ps',
        'kill', 'killall', 'pkill', 'nice', 'renice', 'nohup', 'bg', 'fg', 'jobs',
        'export', 'unset', 'env', 'set', 'alias', 'unalias', 'source', '.',
        'history', 'type', 'which', 'whereis', 'man', 'info', 'help', 'exit',
        'logout', 'clear', 'reset', 'stty', 'tput', 'echo', 'printf', 'read',
        'exec', 'eval', 'shift', 'getopts', 'trap', 'wait', 'sleep', 'true',
        'false', 'test', '[', ']', 'let', 'declare', 'typeset', 'local', 'readonly',
        'export', 'unset', 'shift', 'source', 'exec'
    ]

    result = code

    # 高亮注释（从 # 到行尾）
    result = re.sub(r'(#.*$)', r'<span class="com">\1</span>', result, flags=re.MULTILINE)

    # 高亮字符串（双引号和单引号）
    result = re.sub(r'"([^"]*)"', r'<span class="str">"\1"</span>', result)
    result = re.sub(r"'([^']*)'", r"<span class='str'>\1</span>", result)

    # 高亮数字
    result = re.sub(r'\b(\d+)\b', r'<span class="num">\1</span>', result)

    # 高亮命令（在行首或空格后面）
    for cmd in sorted(commands, key=len, reverse=True):
        escaped_cmd = re.escape(cmd)
        # 只匹配在行首、空格或操作符后面的命令
        result = re.sub(r'(?:^|\s|\||;|&&|\|\|)\b(' + escaped_cmd + r')(?=\s|$)', r'<span class="cmd">\1</span>', result, flags=re.MULTILINE)

    # 高亮变量（$VAR 或 ${VAR}）
    result = re.sub(r'(\$\{?\w+\}?)', r'<span class="var">\1</span>', result)

    return result

def process_file(input_file, output_file=None):
    """
    处理 HTML 文件，为 Shell 代码添加高亮
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 统计代码块数量
    code_blocks = re.findall(r'<pre><code class="sh">(.*?)</code></pre>', content, re.DOTALL)
    print(f"找到 {len(code_blocks)} 个 Shell 代码块")

    # 处理代码块
    def replace_shell_code(match):
        code = match.group(1)
        highlighted = highlight_shell(code)
        return f'<pre><code class="sh">{highlighted}</code></pre>'

    # 只处理未添加高亮的代码块（通过检查是否包含 span 标签）
    def should_replace(match):
        code = match.group(1)
        return '<span' not in code

    processed = 0
    skipped = 0

    def replace_if_needed(match):
        nonlocal processed, skipped
        code = match.group(1)
        if '<span' not in code:
            highlighted = highlight_shell(code)
            processed += 1
            print(f"  处理代码块 {processed}: {code[:30]}...")
            return f'<pre><code class="sh">{highlighted}</code></pre>'
        else:
            skipped += 1
            print(f"  跳过已处理的代码块 {skipped}")
            return match.group(0)

    content = re.sub(r'<pre><code class="sh">(.*?)</code></pre>', replace_if_needed, content, flags=re.DOTALL)

    # 保存结果
    if output_file is None:
        output_file = input_file

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n处理完成！")
    print(f"  处理的代码块: {processed}")
    print(f"  跳过的代码块: {skipped}")
    print(f"  输出文件: {output_file}")

if __name__ == '__main__':
    input_file = 'index.html'
    output_file = 'index.html'

    # 检查命令行参数
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    print("Shell 语法高亮工具")
    print("=" * 50)
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print()

    try:
        process_file(input_file, output_file)
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{input_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
