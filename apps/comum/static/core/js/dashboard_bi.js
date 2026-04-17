/**
 * dashboard_bi.js — Charts de Business Intelligence do SIGE
 * Lê os dados JSON embutidos via atributos data-* no elemento #bi-data
 * e instancia os gráficos Chart.js adaptados ao Design System.
 */

(function () {
  "use strict";

  /* ---------- Helpers de estilo ---------- */
  function cssVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function rgba(hex, alpha) {
    // Accepts CSS var strings or raw colors — Chart.js handles this natively
    return hex;
  }

  /* ---------- Paleta do Design System ---------- */
  const VIOLET  = cssVar("--accent-violet")  || "#7c6fff";
  const CYAN    = cssVar("--accent-cyan")    || "#22d3ee";
  const EMERALD = cssVar("--accent-emerald") || "#34d399";
  const AMBER   = cssVar("--accent-amber")  || "#fbbf24";
  const RED     = cssVar("--accent-red")    || "#f87171";
  const TEXT    = cssVar("--text-muted")     || "#94a3b8";
  const BORDER  = cssVar("--border-subtle")  || "rgba(255,255,255,0.08)";
  const BG_SURF= cssVar("--bg-surface")      || "#1e293b";

  Chart.defaults.color = TEXT;
  Chart.defaults.borderColor = BORDER;
  Chart.defaults.font.family = "'Inter', sans-serif";
  Chart.defaults.font.size = 12;

  /* ---------- Leitura dos dados embutidos ---------- */
  const el = document.getElementById("bi-data");
  if (!el) return;

  const turmasLabels   = JSON.parse(el.dataset.turmasLabels   || "[]");
  const turmasData     = JSON.parse(el.dataset.turmasData     || "[]");
  const statusLabels   = JSON.parse(el.dataset.statusLabels   || "[]");
  const statusData     = JSON.parse(el.dataset.statusData     || "[]");
  const evolucaoLabels = JSON.parse(el.dataset.evolucaoLabels || "[]");
  const evolucaoData   = JSON.parse(el.dataset.evolucaoData   || "[]");
  const atestadoLabels = JSON.parse(el.dataset.atestadoLabels || "[]");
  const atestadoData   = JSON.parse(el.dataset.atestadoData   || "[]");

  const basePlugin = {
    tooltip:  { backgroundColor: BG_SURF, borderColor: BORDER, borderWidth: 1, cornerRadius: 8, padding: 10 },
    legend:   { labels: { usePointStyle: true, pointStyle: "circle", padding: 16 } },
  };

  /* ---------- 1. Alunos por Turma (barra horizontal) ---------- */
  const ctxTurmas = document.getElementById("chartTurmas");
  if (ctxTurmas && turmasLabels.length) {
    new Chart(ctxTurmas, {
      type: "bar",
      data: {
        labels: turmasLabels,
        datasets: [{
          label: "Alunos",
          data: turmasData,
          backgroundColor: `${VIOLET}99`,
          borderColor: VIOLET,
          borderWidth: 2,
          borderRadius: 6,
        }],
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: { ...basePlugin, legend: { display: false } },
        scales: {
          x: { grid: { color: BORDER }, ticks: { precision: 0 } },
          y: { grid: { display: false } },
        },
        animation: { duration: 800, easing: "easeOutQuart" },
      },
    });
  }

  /* ---------- 2. Status de Matrícula (Doughnut) ---------- */
  const ctxStatus = document.getElementById("chartStatus");
  if (ctxStatus) {
    const colors = [EMERALD, AMBER, RED, CYAN, VIOLET];
    new Chart(ctxStatus, {
      type: "doughnut",
      data: {
        labels: statusLabels,
        datasets: [{
          data: statusData,
          backgroundColor: colors.map(c => `${c}CC`),
          borderColor: BG_SURF,
          borderWidth: 3,
          hoverOffset: 8,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "70%",
        plugins: { ...basePlugin },
        animation: { animateRotate: true, duration: 900, easing: "easeOutQuart" },
      },
    });
  }

  /* ---------- 3. Evolução de Matrículas (linha) ---------- */
  const ctxEvolucao = document.getElementById("chartEvolucao");
  if (ctxEvolucao && evolucaoLabels.length) {
    new Chart(ctxEvolucao, {
      type: "line",
      data: {
        labels: evolucaoLabels,
        datasets: [{
          label: "Total de Alunos Matriculados",
          data: evolucaoData,
          borderColor: CYAN,
          backgroundColor: `${CYAN}22`,
          borderWidth: 2.5,
          pointBackgroundColor: CYAN,
          pointRadius: 5,
          pointHoverRadius: 7,
          fill: true,
          tension: 0.4,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { ...basePlugin },
        scales: {
          y: { grid: { color: BORDER }, ticks: { precision: 0 }, beginAtZero: true },
          x: { grid: { display: false } },
        },
        animation: { duration: 900, easing: "easeOutQuart" },
      },
    });
  }

  /* ---------- 4. Atestados por Status (barra vertical) ---------- */
  const ctxAtestado = document.getElementById("chartAtestados");
  if (ctxAtestado) {
    const atColors = [AMBER, EMERALD, RED];
    new Chart(ctxAtestado, {
      type: "bar",
      data: {
        labels: atestadoLabels,
        datasets: [{
          label: "Atestados",
          data: atestadoData,
          backgroundColor: atColors.map(c => `${c}99`),
          borderColor: atColors,
          borderWidth: 2,
          borderRadius: 8,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { ...basePlugin, legend: { display: false } },
        scales: {
          y: { grid: { color: BORDER }, ticks: { precision: 0 }, beginAtZero: true },
          x: { grid: { display: false } },
        },
        animation: { duration: 700, easing: "easeOutQuart" },
      },
    });
  }
})();
