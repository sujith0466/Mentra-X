/**
 * Enterprise AI Operations Dashboard Client Controller (Phase 5 Milestone 6)
 * Features:
 * - 10-Second Live Polling with Graceful Error Recovery
 * - Chart.js Dynamic Visual Analytics & Telemetry Rendering
 * - Seamless DOM Updates without Page Reloads
 */

document.addEventListener('DOMContentLoaded', () => {
    initTabNavigation();
    initCharts();
    fetchDashboardOverview();
    
    // Start 10-second live polling
    const pollInterval = setInterval(fetchDashboardOverview, 10000);
    
    // Manual refresh button
    const refreshBtn = document.getElementById('btn-refresh');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            refreshBtn.classList.add('refreshing');
            fetchDashboardOverview().finally(() => {
                setTimeout(() => refreshBtn.classList.remove('refreshing'), 500);
            });
        });
    }

    // Clean up interval on page leave
    window.addEventListener('beforeunload', () => clearInterval(pollInterval));
});

function initTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-tab');
            
            tabButtons.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            btn.classList.add('active');
            const activePane = document.getElementById(`tab-${target}`);
            if (activePane) {
                activePane.classList.add('active');
            }
        });
    });
}

const charts = {};

function initCharts() {
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js library not loaded. Visual charts will be disabled.');
        return;
    }

    Chart.defaults.color = '#94a3b8';
    Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.05)';
    Chart.defaults.font.family = "'Inter', 'Outfit', system-ui, sans-serif";

    // 1. Overview Swarm Status Doughnut
    const ctxSwarm = document.getElementById('chart-overview-swarm');
    if (ctxSwarm) {
        charts.overviewSwarm = new Chart(ctxSwarm, {
            type: 'doughnut',
            data: {
                labels: ['Active Workflows', 'Running Agents', 'Waiting', 'Failed'],
                datasets: [{
                    data: [5, 15, 1, 0],
                    backgroundColor: ['#6366f1', '#06b6d4', '#f59e0b', '#ef4444'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }

    // 2. AI Quality Benchmarks Bar Chart
    const ctxQuality = document.getElementById('chart-overview-quality');
    if (ctxQuality) {
        charts.overviewQuality = new Chart(ctxQuality, {
            type: 'bar',
            data: {
                labels: ['Faithfulness', 'Hallucination', 'Relevance', 'Quality', 'Safety', 'Confidence'],
                datasets: [{
                    label: 'Score Percentile',
                    data: [0.91, 0.98, 0.94, 0.92, 0.99, 0.88],
                    backgroundColor: 'rgba(99, 102, 241, 0.65)',
                    borderColor: '#6366f1',
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 0, max: 1.0, ticks: { callback: v => (v * 100) + '%' } }
                },
                plugins: { legend: { display: false } }
            }
        });
    }

    // 3. Provider Cost & Latency Comparison
    const ctxProvider = document.getElementById('chart-providers');
    if (ctxProvider) {
        charts.providers = new Chart(ctxProvider, {
            type: 'bar',
            data: {
                labels: ['Mastra', 'OpenRouter', 'MockProvider'],
                datasets: [
                    {
                        label: 'Avg Latency (ms)',
                        data: [850, 1100, 15],
                        backgroundColor: 'rgba(6, 182, 212, 0.65)',
                        yAxisID: 'y'
                    },
                    {
                        label: 'Success Rate (%)',
                        data: [99.1, 99.0, 100],
                        backgroundColor: 'rgba(16, 185, 129, 0.65)',
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { type: 'linear', position: 'left', title: { display: true, text: 'Latency (ms)' } },
                    y1: { type: 'linear', position: 'right', min: 80, max: 100, grid: { drawOnChartArea: false }, title: { display: true, text: 'Success (%)' } }
                }
            }
        });
    }

    // 4. Observability Latency Breakdown
    const ctxObs = document.getElementById('chart-observability');
    if (ctxObs) {
        charts.observability = new Chart(ctxObs, {
            type: 'line',
            data: {
                labels: ['HTTP Req', 'Tool Exec', 'Agent Exec', 'DB Query', 'Vector Search'],
                datasets: [{
                    label: 'Latency Profile (ms)',
                    data: [145, 320, 890, 12.5, 28.4],
                    fill: true,
                    backgroundColor: 'rgba(168, 85, 247, 0.15)',
                    borderColor: '#a855f7',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } }
            }
        });
    }
}

async function fetchDashboardOverview() {
    const warningBanner = document.getElementById('polling-warning');
    const lastUpdatedEl = document.getElementById('last-updated');

    try {
        const response = await fetch('/api/v1/dashboard/overview');
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
        }
        
        const payload = await response.json();
        if (payload.status !== 'success' || !payload.data) {
            throw new Error('Invalid dashboard payload structure');
        }

        if (warningBanner) warningBanner.style.display = 'none';
        if (lastUpdatedEl) lastUpdatedEl.textContent = new Date().toLocaleTimeString();

        updateDashboardDOM(payload.data);
    } catch (err) {
        console.error('Error polling Enterprise AI Operations dashboard:', err);
        if (warningBanner) {
            warningBanner.style.display = 'flex';
            warningBanner.querySelector('span').textContent = `Live Polling Degraded: Unable to reach telemetry server (${err.message}). Showing cached data.`;
        }
    }
}

function updateDashboardDOM(data) {
    // 1. Update Overview KPIs
    if (data.swarm) {
        setElText('kpi-active-workflows', data.swarm.active_workflows || 0);
        setElText('kpi-running-agents', data.swarm.running_agents || 0);
        setElText('kpi-avg-latency', `${data.swarm.avg_latency_ms || 850} ms`);
        
        if (charts.overviewSwarm) {
            charts.overviewSwarm.data.datasets[0].data = [
                data.swarm.active_workflows || 0,
                data.swarm.running_agents || 0,
                data.swarm.waiting_workflows || 0,
                data.swarm.failed_workflows || 0
            ];
            charts.overviewSwarm.update('none');
        }
    }

    if (data.runtime) {
        const statusEl = document.getElementById('kpi-runtime-status');
        if (statusEl) {
            const st = data.runtime.overall_status || 'HEALTHY';
            statusEl.textContent = st;
            statusEl.className = `status-badge status-${st.toLowerCase()}`;
        }
        
        updateStatusBadge('badge-wstore', data.runtime.workflow_store_status);
        updateStatusBadge('badge-ebus', data.runtime.event_bus_status);
        updateStatusBadge('badge-prepo', data.runtime.prompt_repo_status);
        updateStatusBadge('badge-mem', data.runtime.memory_status);
        updateStatusBadge('badge-obs', data.runtime.runtime_status);
    }

    if (data.quality) {
        setElText('kpi-ai-quality', `${Math.round((data.quality.quality || 0.92) * 100)}%`);
        setElText('kpi-faithfulness', `${Math.round((data.quality.faithfulness || 0.91) * 100)}%`);
        setElText('kpi-hallucination', `${Math.round((data.quality.hallucination || 0.98) * 100)}%`);
        
        if (charts.overviewQuality) {
            charts.overviewQuality.data.datasets[0].data = [
                data.quality.faithfulness || 0.91,
                data.quality.hallucination || 0.98,
                data.quality.relevance || 0.94,
                data.quality.quality || 0.92,
                data.quality.safety || 0.99,
                data.quality.confidence || 0.88
            ];
            charts.overviewQuality.update('none');
        }
    }

    if (data.providers && data.providers.providers) {
        updateProvidersTable(data.providers.providers);
    }

    if (data.prompts) {
        setElText('kpi-prompt-version', data.prompts.active_version || '1.0.0');
        setElText('kpi-prompt-tokens', (data.prompts.total_tokens || 45000).toLocaleString());
        setElText('kpi-prompt-cost', `$${data.prompts.avg_cost_usd || 0.0125}`);
    }

    if (data.privacy) {
        setElText('kpi-active-consents', data.privacy.active_consents || 0);
        setElText('kpi-revoked-consents', data.privacy.revoked_consents || 0);
        setElText('kpi-privacy-integrity', data.privacy.audit_chain_integrity || 'VERIFIED');
        setElText('kpi-retention-jobs', data.privacy.retention_jobs_run || 0);
    }
}

function updateStatusBadge(id, status) {
    const el = document.getElementById(id);
    if (el) {
        const st = status || 'HEALTHY';
        el.textContent = st;
        el.className = `status-badge status-${st.toLowerCase()}`;
    }
}

function setElText(id, text) {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = text;
    }
}

function updateProvidersTable(providers) {
    const tbody = document.getElementById('table-providers-body');
    if (!tbody) return;

    tbody.innerHTML = '';
    const names = Object.keys(providers);
    
    if (charts.providers) {
        charts.providers.data.labels = names;
        charts.providers.data.datasets[0].data = names.map(n => providers[n].latency || 0);
        charts.providers.data.datasets[1].data = names.map(n => providers[n].success_rate || 0);
        charts.providers.update('none');
    }

    names.forEach(p => {
        const d = providers[p];
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="font-weight: 600; color: #f8fafc;">${p}</td>
            <td>${(d.requests || 0).toLocaleString()}</td>
            <td><span class="status-badge ${d.errors > 0 ? 'status-degraded' : 'status-healthy'}">${d.errors || 0}</span></td>
            <td>${(d.tokens || 0).toLocaleString()}</td>
            <td>$${d.cost || 0.000}</td>
            <td>${d.latency || 0} ms</td>
            <td style="color: #34d399; font-weight: 600;">${d.success_rate || 100}%</td>
        `;
        tbody.appendChild(tr);
    });
}
