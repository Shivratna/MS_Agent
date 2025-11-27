document.addEventListener('DOMContentLoaded', async () => {
    const form = document.getElementById('profileForm');
    const resultsArea = document.getElementById('resultsArea');
    const programsList = document.getElementById('programsList');
    const resetBtn = document.getElementById('resetBtn');
    const submitBtn = form.querySelector('button[type="submit"]');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');

    const agentFlowArea = document.getElementById('agentFlowArea');
    const agentFlowContainer = document.getElementById('agentFlowContainer');
    const statusMessage = document.getElementById('statusMessage');

    // Load Agent Flow HTML
    try {
        const response = await fetch('agents.html');
        const html = await response.text();
        agentFlowContainer.innerHTML = html;
    } catch (e) {
        console.error("Failed to load agents.html", e);
    }

    // Modal Functionality
    const aboutAgentsBtn = document.getElementById('aboutAgentsBtn');
    const agentModal = document.getElementById('agentModal');
    const modalClose = document.querySelector('.modal-close');

    if (aboutAgentsBtn && agentModal && modalClose) {
        aboutAgentsBtn.addEventListener('click', () => {
            agentModal.classList.remove('hidden');
        });

        modalClose.addEventListener('click', () => {
            agentModal.classList.add('hidden');
        });

        // Close modal when clicking outside
        agentModal.addEventListener('click', (e) => {
            if (e.target === agentModal) {
                agentModal.classList.add('hidden');
            }
        });
    } else {
        console.error("Modal elements not found");
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Loading State
        setLoading(true);
        form.classList.add('hidden'); // Hide form
        agentFlowArea.classList.remove('hidden');
        resultsArea.classList.add('hidden');
        resetAgents();

        // Gather Data
        const formData = {
            gpa: parseFloat(document.getElementById('gpa').value),
            target_degree: document.getElementById('target_degree').value,
            target_countries: document.getElementById('target_countries').value.split(',').map(s => s.trim()),
            budget: document.getElementById('budget').value,
            interests: document.getElementById('interests').value.split(',').map(s => s.trim()),
            target_intake: document.getElementById('target_intake').value,
            test_scores: {}
        };

        const gre = document.getElementById('gre_score').value;
        const toefl = document.getElementById('toefl_score').value;
        if (gre) formData.test_scores['GRE'] = gre;
        if (toefl) formData.test_scores['TOEFL'] = toefl;

        try {
            const response = await fetch('/api/generate-plan-stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const jsonStr = line.substring(6);
                        try {
                            const data = JSON.parse(jsonStr);
                            handleStreamUpdate(data);
                        } catch (e) {
                            console.error("Error parsing stream data", e);
                        }
                    }
                }
            }

        } catch (error) {
            alert('Error generating plan: ' + error.message);
            setLoading(false);
        }
    });

    resetBtn.addEventListener('click', () => {
        resultsArea.classList.add('hidden');
        agentFlowArea.classList.add('hidden');
        form.classList.remove('hidden');
        form.reset();
        programsList.innerHTML = '';
    });

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        if (isLoading) {
            btnText.textContent = 'Generating Plan...';
            btnLoader.classList.remove('hidden');
        } else {
            btnText.textContent = 'Generate Plan';
            btnLoader.classList.add('hidden');
        }
    }

    function handleStreamUpdate(data) {
        if (data.type === 'status') {
            updateAgentStatus(data.agent, data.message);
        } else if (data.type === 'result') {
            renderResults(data.data);
            resultsArea.classList.remove('hidden');
            setLoading(false);
            statusMessage.textContent = "Plan Generated Successfully!";
            markAllAgentsDone();
        } else if (data.type === 'error') {
            alert('Error: ' + data.message);
            setLoading(false);
        }
    }

    function updateAgentStatus(agentName, message) {
        statusMessage.textContent = message;

        // Reset all active
        document.querySelectorAll('.agent-node').forEach(node => {
            node.classList.remove('active');
        });

        // Set current active
        const activeNode = document.getElementById(`agent-${agentName}`);
        if (activeNode) {
            activeNode.classList.add('active');
            activeNode.classList.add('done'); // Mark as visited/done
            activeNode.querySelector('.agent-status').textContent = "Working...";
        }
    }

    function markAllAgentsDone() {
        document.querySelectorAll('.agent-node').forEach(node => {
            node.classList.remove('active');
            node.classList.add('done');
            node.querySelector('.agent-status').textContent = "Done";
        });
    }

    function resetAgents() {
        document.querySelectorAll('.agent-node').forEach(node => {
            node.classList.remove('active');
            node.classList.remove('done');
            node.querySelector('.agent-status').textContent = "Waiting";
        });
        statusMessage.textContent = "Initializing...";
    }

    function renderResults(data) {
        programsList.innerHTML = '';

        if (!data.shortlist || data.shortlist.length === 0) {
            programsList.innerHTML = '<p>No programs found.</p>';
            return;
        }

        data.shortlist.forEach((item, index) => {
            const prog = item.program;
            const timeline = item.timeline;
            const warnings = item.warnings;

            const card = document.createElement('div');
            card.className = 'program-card';
            card.style.animationDelay = `${index * 0.1}s`;

            let timelineHtml = timeline.map(task => `
                <li class="timeline-item">
                    <div class="timeline-icon">📅</div>
                    <div class="timeline-content">
                        <span class="task-date">${task.due_date}</span>
                        <span class="task-title">${task.title}</span>
                    </div>
                </li>
            `).join('');

            let warningsHtml = '';
            if (warnings && warnings.length > 0) {
                warningsHtml = `
                    <div class="warnings-section">
                        <h4>⚠️ Warnings</h4>
                        <div class="warning-box">
                            ${warnings.map(w => `<p>• ${w}</p>`).join('')}
                        </div>
                    </div>
                `;
            }

            card.innerHTML = `
                <div class="program-header">
                    <div class="program-title">
                        <h3>${prog.name}</h3>
                        <p class="program-uni">${prog.university}, ${prog.country}</p>
                    </div>
                    <div class="tag">${prog.application_deadline}</div>
                </div>
                
                <div class="program-meta">
                    <span>💰 ${prog.tuition_range}</span>
                </div>

                <div class="timeline-section">
                    <h4>📅 Application Timeline</h4>
                    <ul class="timeline-list">
                        ${timelineHtml}
                    </ul>
                </div>

                ${warningsHtml}
            `;

            programsList.appendChild(card);
        });
    }
});
