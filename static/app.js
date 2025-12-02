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

    // Q&A Chat Box elements
    const qnaBar = document.getElementById('qnaBar');
    const qnaChatToggle = document.getElementById('qnaChatToggle');
    const qnaClose = document.getElementById('qnaClose');
    const qnaQuestions = document.getElementById('qnaQuestions');

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

    // Q&A Chat Box toggle
    if (qnaChatToggle && qnaBar) {
        qnaChatToggle.addEventListener('click', () => {
            qnaBar.classList.toggle('open');
        });
    }

    if (qnaClose && qnaBar) {
        qnaClose.addEventListener('click', () => {
            qnaBar.classList.remove('open');
        });
    }

    // Onboarding Logic
    const welcomePanel = document.getElementById('welcomePanel');
    const startPlanningBtn = document.getElementById('startPlanningBtn');

    startPlanningBtn.addEventListener('click', () => {
        welcomePanel.classList.add('hidden');
        form.classList.remove('hidden');
        updateSidebar('profile');
    });

    // Stepper Logic
    let currentStep = 1;
    const totalSteps = 3;
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    // submitBtn is already defined at the top, we'll use that
    const formSteps = document.querySelectorAll('.form-step');

    // Initialize first step
    showStep(currentStep);

    nextBtn.addEventListener('click', () => {
        if (validateStep(currentStep)) {
            currentStep++;
            showStep(currentStep);
        }
    });

    prevBtn.addEventListener('click', () => {
        currentStep--;
        showStep(currentStep);
    });

    function showStep(step) {
        formSteps.forEach(el => el.classList.remove('active'));
        document.querySelector(`.form-step[data-step="${step}"]`).classList.add('active');

        // Button State
        prevBtn.classList.toggle('hidden', step === 1);

        if (step === totalSteps) {
            nextBtn.classList.add('hidden');
            submitBtn.classList.remove('hidden');
        } else {
            nextBtn.classList.remove('hidden');
            submitBtn.classList.add('hidden');
        }

        // Update Sidebar
        updateSidebar(step);
    }

    function validateStep(step) {
        const currentStepEl = document.querySelector(`.form-step[data-step="${step}"]`);
        const inputs = currentStepEl.querySelectorAll('input, select');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.checkValidity()) {
                isValid = false;
                input.reportValidity();
            }
        });

        return isValid;
    }

    function updateSidebar(stepOrId) {
        // Map step numbers to IDs
        const stepMap = {
            1: 'profile',
            2: 'profile', // Keep profile active for preferences too
            3: 'profile',
            'shortlist': 'shortlist',
            'requirements': 'requirements',
            'timeline': 'timeline'
        };

        const activeId = stepMap[stepOrId] || stepOrId;

        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
            if (item.dataset.step === activeId) {
                item.classList.add('active');
            }
        });
    }

    // Resume Text Paste Logic
    const autoFillBtn = document.getElementById('autoFillBtn');
    const resumeText = document.getElementById('resumeText');
    const uploadStatus = document.getElementById('uploadStatus');
    const charCount = document.querySelector('.char-count');

    if (resumeText && charCount) {
        resumeText.addEventListener('input', () => {
            const currentLength = resumeText.value.length;
            charCount.textContent = `${currentLength}/5000`;
            if (currentLength > 5000) {
                charCount.style.color = 'var(--error-color)';
            } else {
                charCount.style.color = 'var(--text-tertiary)';
            }
        });
    }

    if (autoFillBtn && resumeText) {
        autoFillBtn.addEventListener('click', async () => {
            const text = resumeText.value.trim();
            if (!text) {
                alert("Please paste your resume text first.");
                return;
            }
            if (text.length > 5000) {
                alert("Text is too long. Please limit to 5000 characters.");
                return;
            }
            await handleResumeParse(text);
        });
    }

    async function handleResumeParse(text) {
        uploadStatus.textContent = "Parsing resume... ⏳";
        uploadStatus.className = "upload-status";
        autoFillBtn.disabled = true;

        try {
            const response = await fetch('/api/parse-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) throw new Error("Parsing failed");

            const result = await response.json();
            if (result.success && result.data) {
                populateForm(result.data);
                uploadStatus.textContent = "Auto-filled! ✅";
                uploadStatus.className = "upload-status success";
            } else {
                throw new Error("Parsing failed");
            }
        } catch (error) {
            console.error(error);
            uploadStatus.textContent = "Failed to parse ❌";
            uploadStatus.className = "upload-status error";
        } finally {
            autoFillBtn.disabled = false;
        }
    }

    function populateForm(data) {
        // Helper to set value if exists
        const setVal = (id, val) => {
            const el = document.getElementById(id);
            if (el && val !== undefined && val !== null && val !== 0 && val !== "") {
                el.value = val;
            }
        };

        setVal('gpa', data.gpa);
        setVal('target_degree', data.target_degree);
        setVal('undergrad_major', data.undergrad_major);
        setVal('work_experience_years', data.work_experience_years);
        setVal('backlogs', data.backlogs);
        setVal('research_papers', data.research_papers);

        // Handle Test Scores
        if (data.test_scores) {
            setVal('gre_score', data.test_scores.GRE);
            setVal('toefl_score', data.test_scores.TOEFL);
        }

        // Handle Interests (array to string)
        if (data.interests && Array.isArray(data.interests)) {
            setVal('interests', data.interests.join(', '));
        }
    }

    // Form Submission
    submitBtn.addEventListener('click', async (e) => {
        e.preventDefault();

        // Basic Validation
        const requiredFields = ['gpa', 'target_degree', 'target_countries', 'target_intake', 'interests'];
        const missing = requiredFields.filter(id => !document.getElementById(id).value);

        if (missing.length > 0) {
            alert(`Please fill in all required fields: ${missing.join(', ')}`);
            return;
        }

        // UI Updates
        setLoading(true);
        form.classList.add('hidden');
        agentFlowArea.classList.remove('hidden');
        resultsArea.classList.add('hidden');
        updateSidebar('shortlist');

        // Reset Flow Visualization
        resetAgents(); // Renamed from resetAgentFlow to match existing function

        // Collect Data
        const formData = collectFormData();

        // Start Streaming
        await startPlanGeneration(formData);
    });

    function collectFormData() {
        return {
            gpa: parseFloat(document.getElementById('gpa').value),
            target_degree: document.getElementById('target_degree').value,
            target_countries: document.getElementById('target_countries').value.split(',').map(s => s.trim()),
            budget: document.getElementById('budget').value,
            interests: document.getElementById('interests').value.split(',').map(s => s.trim()),
            target_intake: document.getElementById('target_intake').value,
            undergrad_major: document.getElementById('undergrad_major').value,
            work_experience_years: parseFloat(document.getElementById('work_experience_years').value) || 0,
            backlogs: parseInt(document.getElementById('backlogs').value) || 0,
            research_papers: parseInt(document.getElementById('research_papers').value) || 0,
            test_scores: {
                GRE: document.getElementById('gre_score').value,
                TOEFL: document.getElementById('toefl_score').value
            }
        };
    }

    async function startPlanGeneration(formData) {
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
    }

    resetBtn.addEventListener('click', () => {
        resultsArea.classList.add('hidden');
        agentFlowArea.classList.add('hidden');
        welcomePanel.classList.remove('hidden'); // Go back to welcome
        qnaBar.classList.add('hidden'); // Hide Q&A bar
        form.reset();
        programsList.innerHTML = '';
        qnaQuestions.innerHTML = ''; // Clear Q&A

        // Clear pills and export button
        const pillsContainer = document.getElementById('universityPills');
        if (pillsContainer) pillsContainer.innerHTML = '';
        const exportBtn = document.getElementById('exportBtn');
        if (exportBtn) exportBtn.classList.add('hidden');

        // Reset global state
        allProgramsData = [];
        currentProgramIndex = 0;

        currentStep = 1;
        showStep(1);
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
            updateSidebar('timeline');

            // Show Q&A bar if questions are available
            if (data.data.qna_questions && data.data.qna_questions.length > 0) {
                renderQNA(data.data.qna_questions);
                qnaBar.classList.remove('hidden');
            }
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

    // Global variable to store all programs data
    let allProgramsData = [];
    let currentProgramIndex = 0;

    function renderResults(data) {
        if (!data.shortlist || data.shortlist.length === 0) {
            programsList.innerHTML = '<p>No programs found.</p>';
            return;
        }

        // Store data globally
        allProgramsData = data.shortlist;
        currentProgramIndex = 0;

        // Render university pills
        renderUniversityPills();

        // Render first program
        renderSingleProgram(0);

        // Show export button
        const exportBtn = document.getElementById('exportBtn');
        if (exportBtn) {
            exportBtn.classList.remove('hidden');
        }
    }

    function renderUniversityPills() {
        const pillsContainer = document.getElementById('universityPills');
        pillsContainer.innerHTML = '';

        allProgramsData.forEach((item, index) => {
            const prog = item.program;
            const pill = document.createElement('div');
            pill.className = `university-pill ${index === 0 ? 'active' : ''}`;
            pill.dataset.index = index;

            // Country flag mapping
            const countryFlags = {
                'USA': '🇺🇸',
                'Germany': '🇩🇪',
                'Canada': '🇨🇦',
                'UK': '🇬🇧',
                'Australia': '🇦🇺',
                'France': '🇫🇷',
                'Netherlands': '🇳🇱',
                'Sweden': '🇸🇪'
            };

            const flag = countryFlags[prog.country] || '🌍';

            pill.innerHTML = `
                <div class="pill-country">${flag}</div>
                <div class="pill-name">${prog.university}</div>
                <div class="pill-program">${prog.name.substring(0, 30)}${prog.name.length > 30 ? '...' : ''}</div>
            `;

            pill.addEventListener('click', () => switchProgram(index));
            pillsContainer.appendChild(pill);
        });
    }

    function switchProgram(index) {
        currentProgramIndex = index;

        // Update active pill
        document.querySelectorAll('.university-pill').forEach((pill, i) => {
            if (i === index) {
                pill.classList.add('active');
            } else {
                pill.classList.remove('active');
            }
        });

        // Render selected program
        renderSingleProgram(index);
    }

    function renderSingleProgram(index) {
        const item = allProgramsData[index];
        const prog = item.program;
        const timeline = item.timeline;
        const warnings = item.warnings;

        programsList.innerHTML = '';

        const card = document.createElement('div');
        card.className = 'program-card fade-in';

        // Timeline items
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
                    <span class="tag">💰 ${prog.tuition_range}</span>
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
    }

    // Render Q&A questions
    function renderQNA(qnaData) {
        qnaQuestions.innerHTML = '';

        // Update badge count
        const chatBadge = document.querySelector('.chat-badge');
        if (chatBadge) {
            chatBadge.textContent = qnaData.length;
        }

        qnaData.forEach((qna, index) => {
            const qnaItem = document.createElement('div');
            qnaItem.className = 'qna-item';

            const categoryBadge = `<span class="qna-category-badge ${qna.category}">${qna.category}</span>`;

            qnaItem.innerHTML = `
                <button class="qna-question-btn" data-index="${index}" aria-expanded="false">
                    <span>
                        ${qna.question}
                        ${categoryBadge}
                    </span>
                    <span class="qna-question-icon">▼</span>
                </button>
                <div class="qna-answer" id="qna-answer-${index}">
                    <p class="qna-answer-text">${qna.answer}</p>
                </div>
            `;

            qnaQuestions.appendChild(qnaItem);
        });

        // Add click handlers for questions
        document.querySelectorAll('.qna-question-btn').forEach(btn => {
            btn.addEventListener('click', function () {
                const index = this.getAttribute('data-index');
                const answer = document.getElementById(`qna-answer-${index}`);
                const isExpanded = this.getAttribute('aria-expanded') === 'true';

                // Close all others
                document.querySelectorAll('.qna-question-btn').forEach(b => {
                    if (b !== this) {
                        b.classList.remove('active');
                        b.setAttribute('aria-expanded', 'false');
                        const otherIndex = b.getAttribute('data-index');
                        document.getElementById(`qna-answer-${otherIndex}`).classList.remove('expanded');
                    }
                });

                // Toggle current
                if (isExpanded) {
                    this.classList.remove('active');
                    this.setAttribute('aria-expanded', 'false');
                    answer.classList.remove('expanded');
                } else {
                    this.classList.add('active');
                    this.setAttribute('aria-expanded', 'true');
                    answer.classList.add('expanded');
                }
            });
        });
    }

    // Excel Export Functionality
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            if (allProgramsData.length > 0) {
                exportToExcel(currentProgramIndex);
            }
        });
    }

    function exportToExcel(index) {
        const item = allProgramsData[index];
        const prog = item.program;
        const timeline = item.timeline;

        // Prepare data for Excel
        const excelData = timeline.map((task, idx) => ({
            'No.': idx + 1,
            'Task': task.title,
            'Due Date': task.due_date,
            'Status': 'Pending'
        }));

        // Create worksheet
        const worksheet = XLSX.utils.json_to_sheet(excelData);

        // Set column widths
        worksheet['!cols'] = [
            { wch: 5 },  // No.
            { wch: 50 }, // Task
            { wch: 15 }, // Due Date
            { wch: 12 }  // Status
        ];

        // Create workbook
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Timeline');

        // Generate filename
        const filename = `${prog.university}_${prog.name.replace(/[^a-z0-9]/gi, '_')}_Timeline.xlsx`;

        // Download
        XLSX.writeFile(workbook, filename);
    }
});
