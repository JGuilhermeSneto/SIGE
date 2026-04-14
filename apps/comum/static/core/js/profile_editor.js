/* ============================================================
   SIGE — Profile Editor Module
   profile_editor.js
============================================================ */

/**
 * Initializes photo menu toggle, custom upload button, and preview.
 */
function initProfilePhotoEditor() {
    const btnFotoOpcoes = document.getElementById('btn-foto-opcoes');
    const menuFoto = document.getElementById('menu-foto-opcoes');
    const opcaoAlterar = document.getElementById('opcao-alterar-foto');
    const uploadImagemInput = document.getElementById('upload-imagem');

    if (btnFotoOpcoes && menuFoto) {
        btnFotoOpcoes.addEventListener('click', (e) => {
            e.stopPropagation();
            menuFoto.style.display = menuFoto.style.display === 'flex' ? 'none' : 'flex';
        });
    }

    if (opcaoAlterar && uploadImagemInput) {
        opcaoAlterar.addEventListener('click', () => {
            uploadImagemInput.click();
            if (menuFoto) menuFoto.style.display = 'none';
        });
    }

    document.addEventListener('click', (e) => {
        if (menuFoto && !menuFoto.contains(e.target) && e.target !== btnFotoOpcoes) {
            menuFoto.style.display = 'none';
        }
    });

    if (uploadImagemInput) {
        uploadImagemInput.addEventListener('change', (e) => {
            const file = e.target.files && e.target.files[0];
            if (!file) return;

            // Campos disabled não vão no POST — precisa estar habilitado antes do envio.
            const emailInput = document.getElementById('id_email');
            if (emailInput) emailInput.disabled = false;

            const form = document.getElementById('perfil-form');
            if (!form) return;

            // Pré-visualização (assíncrona; não bloqueia o envio).
            const reader = new FileReader();
            reader.onload = (ev) => {
                const img = document.getElementById('imagem-perfil');
                if (!img || !ev.target || !ev.target.result) return;
                if (img.tagName === 'DIV') {
                    const newImg = document.createElement('img');
                    newImg.id = img.id;
                    newImg.className = img.className.replace('perfil-sem-foto', '').trim();
                    newImg.alt = 'Foto de Perfil';
                    newImg.src = ev.target.result;
                    img.replaceWith(newImg);
                } else {
                    img.src = ev.target.result;
                }
            };
            reader.readAsDataURL(file);

            // `form.submit()` ignora validação e, em alguns casos, comporta-se mal com FILE.
            // `requestSubmit()` envia multipart corretamente como um envio “real”.
            if (typeof form.requestSubmit === 'function') {
                form.requestSubmit();
            } else {
                form.submit();
            }
        });
    }
}

/**
 * Password Visibility Toggle
 * @param {string} inputId 
 */
function toggleSenhaVisibility(inputId) {
    const input = document.getElementById(inputId);
    const toggleBtn = input ? input.nextElementSibling : null;
    const icon = toggleBtn ? toggleBtn.querySelector('i') : null;

    if (!input || !icon) return;

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

/**
 * Controls the Edit/Save/Cancel flow for the profile page
 */
function initProfileEditorControls() {
    const emailInput = document.getElementById('id_email');
    const btnEditar = document.getElementById('btn-editar');
    const btnSalvar = document.getElementById('btn-salvar');
    const btnCancelar = document.getElementById('btn-cancelar');
    const secaoSenha = document.getElementById('secao-senha');
    const btnMudarSenha = document.getElementById('btn-mudar-senha');
    const textoBtnSenha = document.getElementById('texto-btn-senha');

    if (!btnEditar) return;

    let senhaAberta = false;
    let originalEmail = emailInput ? emailInput.value : '';

    // Initial state
    if (emailInput) emailInput.disabled = true;
    if (btnSalvar) btnSalvar.style.display = 'none';
    if (btnCancelar) btnCancelar.style.display = 'none';

    btnEditar.onclick = () => {
        if (emailInput) {
            emailInput.disabled = false;
            emailInput.focus();
        }
        btnEditar.style.display = 'none';
        if (btnSalvar) btnSalvar.style.display = 'flex';
        if (btnCancelar) btnCancelar.style.display = 'flex';
    };

    btnCancelar.onclick = () => {
        if (emailInput) {
            emailInput.value = originalEmail;
            emailInput.disabled = true;
        }
        if (senhaAberta) {
            toggleSecaoSenha(false);
        }
        btnEditar.style.display = 'flex';
        if (btnSalvar) btnSalvar.style.display = 'none';
        if (btnCancelar) btnCancelar.style.display = 'none';
    };

    if (btnMudarSenha) {
        btnMudarSenha.onclick = () => {
            const emEdicao = btnSalvar && btnSalvar.style.display === 'flex';
            if (!emEdicao) return;
            senhaAberta = !senhaAberta;
            toggleSecaoSenha(senhaAberta);
        };
    }

    function toggleSecaoSenha(show) {
        senhaAberta = show;
        if (secaoSenha) secaoSenha.style.display = show ? 'block' : 'none';
        if (textoBtnSenha) textoBtnSenha.textContent = show ? 'Cancelar Alteração' : 'Alterar Senha';
        if (btnMudarSenha) btnMudarSenha.style.backgroundColor = show ? '#dc2626' : '#e5e7eb';
        
        if (!show) {
            const novaSenha = document.getElementById('id_nova_senha');
            const confirmarSenha = document.getElementById('id_confirmar_senha');
            if (novaSenha) novaSenha.value = '';
            if (confirmarSenha) confirmarSenha.value = '';
        }
    }
}

// Global exposure
window.toggleSenha = (id) => toggleSenhaVisibility(id);

document.addEventListener('DOMContentLoaded', () => {
    initProfilePhotoEditor();
    initProfileEditorControls();
});
