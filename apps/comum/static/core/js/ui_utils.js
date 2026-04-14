/* ============================================================
   SIGE — Global UI Utilities
   ui_utils.js
============================================================ */

/**
 * Common Input Masks
 */
const masks = {
    cpf: v => v.replace(/\D/g, "").replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d{1,2})$/, "$1-$2"),
    tel: v => v.replace(/\D/g, "").replace(/^(\d{2})(\d)/g, "($1) $2").replace(/(\d{5})(\d)/, "$1-$2"),
    cep: v => v.replace(/\D/g, "").replace(/(\d{5})(\d)/, "$1-$2")
};

/**
 * Initializes global masks on inputs with specific data attributes or IDs
 */
function initGlobalMasks() {
    const cpfInputs = document.querySelectorAll('input[name="cpf"], #id_cpf');
    const telInputs = document.querySelectorAll('input[name="telefone"], #id_telefone');
    const cepInputs = document.querySelectorAll('input[name="cep"], #id_cep');

    cpfInputs.forEach(input => input.addEventListener('input', e => e.target.value = masks.cpf(e.target.value)));
    telInputs.forEach(input => input.addEventListener('input', e => e.target.value = masks.tel(e.target.value)));
    cepInputs.forEach(input => input.addEventListener('input', e => e.target.value = masks.cep(e.target.value)));
}

/**
 * Client-side search filter for grids/lists
 * @param {string} inputId - ID of the search input
 * @param {string} containerId - ID of the container holding the items
 * @param {string} itemSelector - CSS selector for the items to filter
 * @param {string} textSelector - CSS selector for the text to match against
 */
function initSearchFilter(inputId, containerId, itemSelector, textSelector) {
    const input = document.getElementById(inputId);
    const container = document.getElementById(containerId);
    if (!input || !container) return;

    input.addEventListener('input', function() {
        const term = this.value.toLowerCase().trim();
        const items = container.querySelectorAll(itemSelector);
        
        items.forEach(item => {
            const textEl = item.querySelector(textSelector);
            const matches = textEl && textEl.textContent.toLowerCase().includes(term);
            item.style.display = matches ? '' : 'none';
        });
    });
}

/**
 * Client-side pills filter for switching active classes
 * @param {string} selector - CSS selector for the pill elements
 */
function initPillsFilter(selector) {
    const pills = document.querySelectorAll(selector);
    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            pills.forEach(p => p.classList.remove('ativo'));
            pill.classList.add('ativo');
            // Note: Filter logic can be extended here if needed
        });
    });
}

/**
 * Generic Sidebar/Menu Toggle
 */
function initSidebarToggle(toggleId, menuId) {
    const toggle = document.getElementById(toggleId);
    const menu = document.getElementById(menuId);

    if (!toggle || !menu) return;

    toggle.addEventListener('click', (e) => {
        e.stopPropagation();
        menu.classList.toggle('ativo');
    });
}

/**
 * Avatar Dropdown Logic
 */
function initAvatarDropdown(avatarId, dropdownId) {
    const avatar = document.getElementById(avatarId);
    const dropdown = document.getElementById(dropdownId);

    if (!avatar || !dropdown) return;

    avatar.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdown.classList.toggle('ativo');
    });

    document.addEventListener('click', () => {
        dropdown.classList.remove('ativo');
    });
}

// Auto-run common UI features
document.addEventListener('DOMContentLoaded', () => {
    initGlobalMasks();
    
    // Sidebar for base.html
    initSidebarToggle('menu-toggle', 'menu-lateral');

    // Avatar for base.html
    initAvatarDropdown('user-avatar', 'dropdown-menu');

    // Global Notifications Handling
    const messages = document.querySelectorAll('.msg-list li');
    const overlay = document.getElementById('registration-success-overlay');
    
    messages.forEach(msg => {
        const text = msg.textContent.toLowerCase();
        
        // Robust check for "cadastrado", "atualizado", "removido" or "salvo"
        const isRegistration = text.includes('cadastrado') || 
                             text.includes('atualizado') || 
                             text.includes('removido') ||
                             text.includes('sucesso');

        if (msg.classList.contains('success') && isRegistration) {
            if (overlay) {
                const titleEl = document.getElementById('overlay-title');
                const msgEl = document.getElementById('overlay-msg');
                
                // Customize overlay text based on content
                if (text.includes('aluno') || text.includes('discente')) {
                    titleEl.textContent = 'Aluno(a) Salvo!';
                    msgEl.textContent = 'O registro do discente foi processado com sucesso.';
                } else if (text.includes('professor') || text.includes('docente')) {
                    titleEl.textContent = 'Docente Salvo!';
                    msgEl.textContent = 'O registro do professor foi processado com sucesso.';
                } else if (text.includes('gestor') || text.includes('diretor')) {
                    titleEl.textContent = 'Gestor Salvo!';
                    msgEl.textContent = 'O registro do gestor foi processado com sucesso.';
                } else {
                    titleEl.textContent = 'Sucesso!';
                    msgEl.textContent = msg.textContent.trim();
                }
                
                overlay.classList.add('active');
                
                // Auto-close overlay after 3 seconds
                setTimeout(() => {
                    overlay.classList.remove('active');
                }, 3000);
            }
        }

        // Standard Toast Auto-hide
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px) scale(0.9)';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });

    // Logout Animation Intercept
    document.body.addEventListener('click', function(e) {
        const logoutBtn = e.target.closest('.link-sair');
        if (logoutBtn) {
            e.preventDefault();
            
            // Create full screen overlay
            const overlay = document.createElement('div');
            Object.assign(overlay.style, {
                position: 'fixed', top: '0', left: '0',
                width: '100vw', height: '100vh',
                background: 'var(--bg-base)',
                zIndex: '99999', display: 'flex',
                flexDirection: 'column', alignItems: 'center',
                justifyContent: 'center', opacity: '0',
                transition: 'opacity 0.4s ease-in-out'
            });
            
            overlay.innerHTML = `
                <div style="text-align: center;">
                    <i class="fa-solid fa-right-from-bracket" style="font-size: 3.5rem; color: #f87171; animation: arrowExitFalling 1s infinite ease-in-out"></i>
                    <h2 style="margin-top: 25px; color: var(--text-primary); font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 700;">Encerrando sessão...</h2>
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 10px;">Aguarde um momento</p>
                </div>
            `;
            
            document.body.appendChild(overlay);
            
            // Trigger reflow & fade in
            void overlay.offsetWidth;
            overlay.style.opacity = '1';
            
            // Redirect after animation plays for a bit
            setTimeout(() => {
                window.location.href = logoutBtn.href;
            }, 900);
        }
    });

});
