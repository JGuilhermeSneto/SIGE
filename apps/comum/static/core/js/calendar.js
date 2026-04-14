/* ============================================================
   SIGE — Unified Calendar & DatePicker Logic
   calendar.js
============================================================ */

document.addEventListener('DOMContentLoaded', function() {
    initMiniCalendar();
    initFlatpickr();
});

/**
 * Initializes the mini calendar found in dashboards.
 */
function initMiniCalendar() {
    const grade = document.getElementById('cal-grade');
    if (!grade) return;

    const mesNomeEl = document.getElementById('cal-mes-nome');
    const anoEl = document.getElementById('cal-ano');

    const MESES = [
        'JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO',
        'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'
    ];
    
    const hoje = new Date();
    const ano = hoje.getFullYear();
    const mes = hoje.getMonth();
    const diaHj = hoje.getDate();

    // Check if days are already rendered by Django
    const renderedDays = grade.querySelectorAll('.dia');
    if (renderedDays.length > 0) {
        console.log('Mini-calendar days already rendered by server.');
        return;
    }

    const primDia = new Date(ano, mes, 1).getDay();
    const totalDias = new Date(ano, mes + 1, 0).getDate();

    // Add empty slots
    for (let i = 0; i < primDia; i++) {
        const v = document.createElement('div');
        v.className = 'dia vazio';
        grade.appendChild(v);
    }

    // Add days
    for (let d = 1; d <= totalDias; d++) {
        const c = document.createElement('div');
        c.className = (d === diaHj) ? 'dia atual' : 'dia';
        c.textContent = d;
        grade.appendChild(c);
    }
}

/**
 * Initializes Flatpickr on all date inputs.
 */
function initFlatpickr() {
    if (typeof flatpickr === 'undefined') {
        console.warn('Flatpickr not loaded.');
        return;
    }

    // Localization for Portuguese
    flatpickr.l10ns.pt = {
        weekdays: {
            shorthand: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"],
            longhand: [
                "Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira",
                "Quinta-feira", "Sexta-feira", "Sábado",
            ],
        },
        months: {
            shorthand: [
                "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                "Jul", "Ago", "Set", "Out", "Nov", "Dez",
            ],
            longhand: [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
            ],
        },
        rangeSeparator: " até ",
    };

    // Target inputs with type="date" and convert them
    const dateInputs = document.querySelectorAll('input[type="date"]');
    
    dateInputs.forEach(input => {
        // Skip disabled fields
        if (input.disabled) return;

        // Change type to text so we can apply Flatpickr (mobile safe)
        const originalValue = input.value;
        input.setAttribute('type', 'text');
        input.value = originalValue;
        
        // Wrap for better styling
        if (!input.parentElement.classList.contains('date-input-wrapper')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'date-input-wrapper';
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);
            
            // Add icon AFTER input for CSS + selector to work
            const icon = document.createElement('i');
            icon.className = 'fa-solid fa-calendar-days';
            wrapper.appendChild(icon);
        }

        flatpickr(input, {
            locale: "pt",
            dateFormat: "Y-m-d",
            altInput: true,
            altFormat: "d/m/Y",
            allowInput: true,
            disableMobile: "true",
            monthSelectorType: "dropdown", // Better month selection
            yearSelectorType: "dropdown",  // Changed to dropdown as requested (logic depends on theme support)
            onReady: function(selectedDates, dateStr, instance) {
                // Ensure altInput inherits common styles/classes
                if (instance.altInput) {
                    instance.altInput.classList.add('flatpickr-custom');
                    if (input.classList.contains('campo-erro')) {
                        instance.altInput.classList.add('campo-erro');
                    }
                }
            }
        });
    });
}
