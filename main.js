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
    
    // 代码块复制和折叠功能
    const codeBlocks = document.querySelectorAll('.code-block');
    codeBlocks.forEach(function(block) {
        // 创建工具栏容器
        const toolbar = document.createElement('div');
        toolbar.className = 'code-toolbar';
        toolbar.style.cssText = 'position:absolute;top:0;right:0;display:flex;gap:0.5rem;padding:0.5rem;z-index:10;transition:all 0.3s ease;';
        
        // 折叠/展开按钮
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'toggle-btn';
        toggleBtn.textContent = '折叠';
        toggleBtn.style.cssText = 'background:rgba(59, 130, 246, 0.2);border:1px solid rgba(59, 130, 246, 0.3);border-radius:4px;padding:0.3rem 0.6rem;font-size:0.8rem;cursor:pointer;color:#fff;transition:all 0.2s;font-weight:500;min-width:50px;';
        
        toggleBtn.addEventListener('mouseenter', function() {
            this.style.background = 'rgba(59, 130, 246, 0.3)';
            this.style.borderColor = 'rgba(59, 130, 246, 0.5)';
        });
        
        toggleBtn.addEventListener('mouseleave', function() {
            this.style.background = 'rgba(59, 130, 246, 0.2)';
            this.style.borderColor = 'rgba(59, 130, 246, 0.3)';
        });
        
        // 复制按钮
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.textContent = '复制';
        copyBtn.style.cssText = 'background:rgba(16, 185, 129, 0.2);border:1px solid rgba(16, 185, 129, 0.3);border-radius:4px;padding:0.3rem 0.6rem;font-size:0.8rem;cursor:pointer;color:#fff;transition:all 0.2s;font-weight:500;';
        
        copyBtn.addEventListener('mouseenter', function() {
            this.style.background = 'rgba(16, 185, 129, 0.3)';
            this.style.borderColor = 'rgba(16, 185, 129, 0.5)';
        });
        
        copyBtn.addEventListener('mouseleave', function() {
            this.style.background = 'rgba(16, 185, 129, 0.2)';
            this.style.borderColor = 'rgba(16, 185, 129, 0.3)';
        });
        
        // 折叠功能
        let isExpanded = true;
        const pre = block.querySelector('pre');
        const originalMaxHeight = pre.style.maxHeight || '500px';
        
        toggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (isExpanded) {
                // 折叠 - 只隐藏 pre 内容，保留工具栏
                pre.style.maxHeight = '0';
                pre.style.padding = '0';
                pre.style.opacity = '0';
                pre.style.overflow = 'hidden';
                toggleBtn.textContent = '展开';
                block.classList.add('collapsed');
            } else {
                // 展开
                pre.style.maxHeight = originalMaxHeight;
                pre.style.padding = '1.25rem';
                pre.style.opacity = '1';
                pre.style.overflow = 'auto';
                toggleBtn.textContent = '折叠';
                block.classList.remove('collapsed');
            }
            isExpanded = !isExpanded;
        });
        
        // 复制功能
        copyBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const code = block.querySelector('code');
            if (code) {
                const text = code.textContent;
                navigator.clipboard.writeText(text).then(function() {
                    copyBtn.textContent = '已复制!';
                    copyBtn.style.background = 'rgba(16, 185, 129, 0.4)';
                    setTimeout(function() {
                        copyBtn.textContent = '复制';
                        copyBtn.style.background = 'rgba(16, 185, 129, 0.2)';
                    }, 2000);
                }).catch(function() {
                    copyBtn.textContent = '复制失败';
                    setTimeout(function() {
                        copyBtn.textContent = '复制';
                    }, 2000);
                });
            }
        });
        
        toolbar.appendChild(toggleBtn);
        toolbar.appendChild(copyBtn);
        
        block.style.position = 'relative';
        block.insertBefore(toolbar, block.firstChild);
        
        // 如果代码超过 15 行，默认折叠
        const code = block.querySelector('code');
        if (code) {
            const lines = code.textContent.split('\n').length;
            if (lines > 15) {
                pre.style.maxHeight = '0';
                pre.style.padding = '0';
                pre.style.opacity = '0';
                pre.style.overflow = 'hidden';
                toggleBtn.textContent = '展开';
                block.classList.add('collapsed');
                isExpanded = false;
            }
        }
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
});
