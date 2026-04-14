/* ============================================================
   SIGE — Attendance & Frequency Module
   attendance.js
============================================================ */

/**
 * Syncs label text and observation input state with the presence checkbox
 */
function updateAttendanceState(cb) {
    const id = cb.value;
    const obs = document.getElementById(`obs_${id}`);
    const lbl = cb.nextElementSibling ? cb.nextElementSibling.querySelector('.status-txt') : null;

    if (cb.checked) {
        // Present
        if (obs) {
            obs.disabled = true;
            obs.value = '';
        }
        if (lbl) lbl.textContent = 'Presente';
    } else {
        // Absent
        if (obs) obs.disabled = false;
        if (lbl) lbl.textContent = 'Falta';
    }
}

/**
 * Toggles presence for a specific student
 */
function toggleAttendance(studentId, isPresent) {
    const cb = document.getElementById(`aluno_${studentId}`);
    if (cb) updateAttendanceState(cb);
}

/**
 * Marks all students in the list as present or absent
 */
function markAllAttendance(isPresent) {
    const checkboxes = document.querySelectorAll('.presenca-toggle input[type="checkbox"]');
    checkboxes.forEach(cb => {
        cb.checked = isPresent;
        updateAttendanceState(cb);
    });
}

// Auto-run initialization for lancar_chamada page
document.addEventListener('DOMContentLoaded', () => {
    const attendanceCheckboxes = document.querySelectorAll('.presenca-toggle input[type="checkbox"]');
    attendanceCheckboxes.forEach(cb => updateAttendanceState(cb));
});

/**
 * Calculates and updates summary stats for the frequency history page
 */
function initHistoryStats() {
    let totalP = 0, totalF = 0;
    document.querySelectorAll('.hist-row[data-presencas]').forEach(row => {
        totalP += parseInt(row.dataset.presencas, 10) || 0;
        totalF += parseInt(row.dataset.faltas, 10) || 0;
    });
    const elP = document.getElementById('total-presencas');
    const elF = document.getElementById('total-faltas');
    if (elP) elP.textContent = totalP;
    if (elF) elF.textContent = totalF;
}

// Global exposure
window.toggleObservacao = (id, present) => toggleAttendance(id, present);
window.marcarTodos = (present) => markAllAttendance(present);
window.initHistoryStats = () => initHistoryStats();
