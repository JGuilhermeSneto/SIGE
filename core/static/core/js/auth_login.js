/* ============================================================
   SIGE — Login Page Animations & Logic
   auth_login.js
============================================================ */

(function () {
    const splash = document.getElementById('splash');
    const bar = document.getElementById('splashBar');
    const ringProg = document.getElementById('ringProgress');
    const ringGlow = document.getElementById('ringGlow');
    const page = document.getElementById('page');

    // 1. Splash Sequence
    if (splash) {
        let pct = 0;
        const iv = setInterval(() => {
            pct = Math.min(pct + 1, 100);
            if (bar) bar.style.width = pct + '%';
            
            // Circular ring animation
            const offset = 245 - (pct / 100) * 245;
            if (ringProg) ringProg.style.strokeDashoffset = offset;
            if (ringGlow) ringGlow.style.strokeDashoffset = offset;

            if (pct >= 100) clearInterval(iv);
        }, 30);

        const steps = [
            { id: 's1', delay: 800 },
            { id: 's2', delay: 1600 },
            { id: 's3', delay: 2400 }
        ];

        steps.forEach(s => {
            setTimeout(() => {
                const el = document.getElementById(s.id);
                if (el) {
                    const icon = el.querySelector('i');
                    icon.classList.remove('fa-circle-notch', 'fa-spin');
                    icon.classList.add('fa-check-circle', 'pop-in-icon');
                    el.classList.add('done');
                }
            }, s.delay);
        });

        setTimeout(() => {
            splash.classList.add('splash-out');
            if (page) page.classList.add('page-in');
            setTimeout(() => splash.style.display = 'none', 700);
        }, 3200);
    }

    // 2. Dynamic Input Animations
    const emailInput = document.getElementById('id_email') || document.querySelector('input[name="username"]');
    const passInput = document.getElementById('id_password') || document.querySelector('input[name="password"]');
    const iconEmail = document.getElementById('icon-email');
    const iconPass = document.getElementById('icon-password');
    const cardBorder = document.getElementById('cardBorder');

    function updateBorder() {
        let emailLen = (emailInput && emailInput.value) ? emailInput.value.length : 0;
        let passLen = (passInput && passInput.value) ? passInput.value.length : 0;
        
        let pEmail = Math.min(emailLen / 12, 1) * 50;
        let pPass = passLen > 0 ? 50 : 0;
        let p = pEmail + pPass;

        if (cardBorder) {
            cardBorder.style.setProperty('--border-progress', p + '%');
        }

        if (emailInput) {
            const w = emailInput.closest('.field-wrap');
            if (w) w.style.setProperty('--input-progress', Math.min(emailLen / 12, 1) * 100 + '%');
        }
        if (passInput) {
            const w = passInput.closest('.field-wrap');
            if (w) w.style.setProperty('--input-progress', (passLen > 0 ? 100 : 0) + '%');
        }
    }

    if (emailInput && iconEmail) {
        emailInput.addEventListener('focus', () => {
            iconEmail.className = 'fas fa-envelope-open field-icon';
            emailInput.closest('.field-wrap').classList.add('focused');
        });
        emailInput.addEventListener('blur', () => {
            if (!emailInput.value) {
                iconEmail.className = 'fas fa-envelope field-icon';
                emailInput.closest('.field-wrap').classList.remove('focused');
            }
        });
        emailInput.addEventListener('input', updateBorder);
    }

    if (passInput && iconPass) {
        passInput.addEventListener('input', () => {
            iconPass.className = passInput.value.length > 0 ? 'fas fa-lock-open field-icon' : 'fas fa-lock field-icon';
            updateBorder();
        });
        passInput.addEventListener('focus', () => passInput.closest('.field-wrap').classList.add('focused'));
        passInput.addEventListener('blur', () => {
            if (!passInput.value) {
                passInput.closest('.field-wrap').classList.remove('focused');
                iconPass.className = 'fas fa-lock field-icon';
            }
        });
    }

    // Password Visiblity
    const toggleBtn = document.getElementById('togglePw');
    if (toggleBtn && passInput) {
        toggleBtn.addEventListener('click', function() {
            const type = passInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passInput.setAttribute('type', type);
            const eye = document.getElementById('eyeIcon');
            if (eye) eye.className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
        });
    }

    // Backend Errors
    if (page && page.dataset.errors === '1') {
        const ov = document.getElementById('feedbackOverlay');
        const box = document.getElementById('feedbackBox');
        if (box) box.classList.add('error');
        const icon = document.getElementById('feedbackIcon');
        if (icon) icon.className = 'fas fa-shield-xmark';
        const msg = document.getElementById('feedbackMsg');
        if (msg) msg.textContent = 'Acesso Negado';
        if (ov) {
            ov.classList.add('show');
            setTimeout(() => ov.classList.remove('show'), 3000);
        }
    }

    // Form Submission Intercept
    const loginForm = document.getElementById('loginForm');
    const btnEntrar = document.getElementById('btnEntrar');
    if (loginForm && btnEntrar) {
        loginForm.addEventListener('submit', function() {
            btnEntrar.classList.add('loading');
            const txt = btnEntrar.querySelector('.btn-text');
            const loader = btnEntrar.querySelector('.btn-loader');
            if (txt) txt.style.opacity = '0';
            if (loader) loader.style.opacity = '1';
            // Allow form to submit naturally
        });
    }

    // Auto-run border check
    setTimeout(updateBorder, 500);
})();
