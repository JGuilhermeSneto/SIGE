/* ============================================================
   SIGE — Registration Wizard Module
   registration_wizard.js
============================================================ */

const RegistrationWizard = {
    config: {},
    currentStep: 1,

    init(config) {
        this.config = config;
        this.attachEvents();
        this.updateIndicators(1);
    },

    attachEvents() {
        // Password validation
        const senhaInput = document.getElementById('id_senha') || document.getElementById('id_nova_senha');
        const confirmaInput = document.getElementById('id_senha_confirmacao') || document.getElementById('id_confirmar_senha');
        
        if (senhaInput) {
            senhaInput.addEventListener('input', () => this.handlePasswordInput(senhaInput, confirmaInput));
        }

        if (confirmaInput) {
            confirmaInput.addEventListener('input', () => this.handlePasswordInput(senhaInput, confirmaInput));
        }

        // Photo preview
        const inputFoto = document.getElementById('id_foto') || document.getElementById('upload-imagem');
        if (inputFoto) {
            inputFoto.addEventListener('change', (e) => this.handlePhotoPreview(e));
        }

        // NE Toggles
        const neCheckbox = document.querySelector('input[name="possui_necessidade_especial"]');
        if (neCheckbox) {
            neCheckbox.addEventListener('change', (e) => {
                const container = document.getElementById('descricao-ne-container');
                if (container) container.style.display = e.target.checked ? 'block' : 'none';
            });
        }
    },

    validarEtapa(n) {
        const etapa = document.getElementById(`etapa-${n}`);
        if (!etapa) return;

        const campos = etapa.querySelectorAll('input[required], select[required]');
        let valido = true;

        campos.forEach(campo => {
            const erroEl = campo.parentElement.querySelector('.erro-inline');
            if (!campo.value.trim()) {
                campo.classList.add('campo-erro');
                if (erroEl) {
                    erroEl.textContent = 'Campo obrigatório';
                    erroEl.style.display = 'block';
                }
                valido = false;
            } else {
                campo.classList.remove('campo-erro');
                if (erroEl) erroEl.style.display = 'none';
            }
        });

        if (valido && n < this.config.totalSteps) {
            this.goToStep(n + 1);
        }
        return valido;
    },

    goToStep(n) {
        const current = document.querySelector('.etapa.ativa');
        const next = document.getElementById(`etapa-${n}`);
        
        if (current && next) {
            current.classList.remove('ativa');
            next.classList.add('ativa');
            this.currentStep = n;
            this.updateIndicators(n);
            window.scrollTo(0, 0);
        }
    },

    voltarEtapa(n) {
        this.goToStep(n - 1);
    },

    updateIndicators(n) {
        for (let i = 1; i <= this.config.totalSteps; i++) {
            const el = document.getElementById(`passo-${i}`);
            if (!el) continue;
            el.classList.remove('ativo', 'completo');
            if (i < n) el.classList.add('completo');
            else if (i === n) el.classList.add('ativo');
        }

        const meta = this.config.stepsMeta[n];
        if (meta) {
            const iconEl = document.getElementById('etapa-icone');
            const titleEl = document.getElementById('etapa-titulo');
            const descEl = document.getElementById('etapa-desc');

            if (iconEl) iconEl.className = `fa-solid ${meta.icone}`;
            if (titleEl) titleEl.textContent = meta.titulo;
            if (descEl) descEl.textContent = meta.desc;
        }
    },

    handlePasswordInput(senhaInput, confirmaInput) {
        const matchMsg = document.getElementById('senha-match-msg');
        const regras = [
            { id: 'req-maiuscula', regex: /[A-Z]/ },
            { id: 'req-minuscula', regex: /[a-z]/ },
            { id: 'req-numero', regex: /\d/ },
            { id: 'req-caractere', regex: /.{6,}/ }
        ];

        // Toggle containers if edition
        if (this.config.isEdition && senhaInput.id === 'id_senha') {
            const show = senhaInput.value.length > 0;
            const confirms = document.getElementById('confirmar-senha-container');
            const reqs = document.getElementById('requisitos-senha-container');
            if (confirms) confirms.style.display = show ? 'block' : 'none';
            if (reqs) reqs.style.display = show ? 'block' : 'none';
        }

        regras.forEach(r => {
            const el = document.getElementById(r.id);
            if (!el) return;
            const ok = r.regex.test(senhaInput.value);
            el.classList.toggle('valid', ok);
            const icon = el.querySelector('i');
            if (icon) icon.className = ok ? 'fa-solid fa-check' : 'fa-solid fa-xmark';
        });

        if (matchMsg && confirmaInput) {
            if (confirmaInput.value === '') {
                matchMsg.style.display = 'none';
                return;
            }
            const ok = senhaInput.value === confirmaInput.value;
            matchMsg.style.display = 'block';
            matchMsg.textContent = ok ? 'Senhas coincidem ✓' : 'As senhas não coincidem';
            matchMsg.className = 'confirmacao-senha ' + (ok ? 'valid' : 'invalido');
        }
    },

    handlePhotoPreview(e) {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = (ev) => {
                const img = document.getElementById('preview-imagem') || document.getElementById('imagem-perfil');
                if (img) {
                    if (img.tagName === 'DIV') {
                        // For profile page replacing div with img
                        const newImg = document.createElement('img');
                        newImg.id = img.id;
                        newImg.className = img.className;
                        newImg.src = ev.target.result;
                        img.replaceWith(newImg);
                    } else {
                        img.src = ev.target.result;
                        img.style.display = 'block';
                    }
                }
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    }
};

// Global Exposure for onclick handlers
window.validarEtapa = (n) => RegistrationWizard.validarEtapa(n);
window.voltarEtapa = (n) => RegistrationWizard.voltarEtapa(n);
