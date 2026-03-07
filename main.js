/**
 * MySQL 教程网站 - 通用 JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // 移动端导航切换
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.menu-overlay');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            sidebar.classList.toggle('active');
            if (overlay) {
                overlay.classList.toggle('active');
            }
        });
        
        // 点击遮罩关闭侧边栏
        if (overlay) {
            overlay.addEventListener('click', function() {
                sidebar.classList.remove('active');
                this.classList.remove('active');
            });
        }
        
        // 点击侧边栏外部关闭
        document.addEventListener('click', function(e) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('active');
                if (overlay) {
                    overlay.classList.remove('active');
                }
            }
        });
    }
    
    // 代码块复制功能
    const codeBlocks = document.querySelectorAll('.code-block');
    codeBlocks.forEach(function(block) {
        // 创建复制按钮
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.textContent = '复制';
        copyBtn.style.cssText = 'position:absolute;top:0.5rem;right:0.5rem;z-index:10;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:4px;padding:0.3rem 0.6rem;font-size:0.8rem;cursor:pointer;color:#fff;transition:all 0.2s;';
        
        copyBtn.addEventListener('mouseenter', function() {
            this.style.background = 'rgba(255,255,255,0.2)';
        });
        
        copyBtn.addEventListener('mouseleave', function() {
            this.style.background = 'rgba(255,255,255,0.1)';
        });
        
        copyBtn.addEventListener('click', function() {
            const code = block.querySelector('code');
            if (code) {
                const text = code.textContent;
                navigator.clipboard.writeText(text).then(function() {
                    copyBtn.textContent = '已复制!';
                    copyBtn.style.background = 'rgba(16, 185, 129, 0.3)';
                    setTimeout(function() {
                        copyBtn.textContent = '复制';
                        copyBtn.style.background = 'rgba(255,255,255,0.1)';
                    }, 2000);
                }).catch(function() {
                    copyBtn.textContent = '复制失败';
                    setTimeout(function() {
                        copyBtn.textContent = '复制';
                    }, 2000);
                });
            }
        });
        
        block.style.position = 'relative';
        block.appendChild(copyBtn);
    });
    
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href.length > 1) {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // 表格包装（响应式）
    document.querySelectorAll('.comparison-table table').forEach(function(table) {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-wrapper';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });
    
    // 为 mermaid 图表添加容器
    document.querySelectorAll('.mermaid').forEach(function(mermaid) {
        mermaid.setAttribute('data-processed', 'false');
    });
    
    // 重新初始化 mermaid
    if (typeof mermaid !== 'undefined' && mermaid.init) {
        mermaid.init();
    }
});
