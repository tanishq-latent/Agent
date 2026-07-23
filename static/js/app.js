// Autonomous Resume Screening Agent Frontend JS Application

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const apiKeyInput = document.getElementById('apiKeyInput');
  const jdTextarea = document.getElementById('jdTextarea');
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');
  const fileList = document.getElementById('fileList');
  const runBtn = document.getElementById('runBtn');
  
  const progressContainer = document.getElementById('progressContainer');
  const progressLogs = document.getElementById('progressLogs');
  
  const resultsSection = document.getElementById('resultsSection');
  const candidateGrid = document.getElementById('candidateGrid');
  const candidateCountSpan = document.getElementById('candidateCountSpan');
  const pipelineTimeSpan = document.getElementById('pipelineTimeSpan');

  const detailModal = document.getElementById('detailModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalBody = document.getElementById('modalBody');

  // State
  let uploadedFiles = []; // Array of File objects

  // Drag and Drop setup
  dropzone.addEventListener('click', () => fileInput.click());

  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
  });

  dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('dragover');
  });

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(Array.from(e.dataTransfer.files));
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(Array.from(e.target.files));
    }
  });

  function handleFiles(files) {
    for (const f of files) {
      if (!uploadedFiles.some(existing => existing.name === f.name)) {
        uploadedFiles.push(f);
      }
    }
    renderFileList();
  }

  function renderFileList() {
    fileList.innerHTML = '';
    if (uploadedFiles.length === 0) {
      fileList.style.display = 'none';
      return;
    }
    fileList.style.display = 'flex';

    uploadedFiles.forEach((file, index) => {
      const item = document.createElement('div');
      item.className = 'file-item';
      item.innerHTML = `
        <span class="file-name">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          ${file.name}
        </span>
        <button class="btn-remove-file" data-index="${index}">&times;</button>
      `;
      fileList.appendChild(item);
    });

    document.querySelectorAll('.btn-remove-file').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const idx = parseInt(e.target.getAttribute('data-index'));
        uploadedFiles.splice(idx, 1);
        renderFileList();
      });
    });
  }

  // Add log entry to UI progress log window
  function appendLog(agent, message) {
    const timeStr = new Date().toLocaleTimeString();
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.innerHTML = `
      <span class="log-time">[${timeStr}]</span>
      <span class="log-agent">${agent}:</span>
      <span class="log-msg">${message}</span>
    `;
    progressLogs.appendChild(entry);
    progressLogs.scrollTop = progressLogs.scrollHeight;
  }

  // Execute Screening Pipeline
  runBtn.addEventListener('click', async () => {
    const jdText = jdTextarea.value.trim();
    const apiKey = apiKeyInput ? apiKeyInput.value.trim() : '';

    if (!jdText) {
      alert('Please paste or type a Job Description first!');
      jdTextarea.focus();
      return;
    }

    if (uploadedFiles.length === 0) {
      alert('Please upload at least one candidate resume (PDF or TXT)!');
      return;
    }

    // UI Loading state
    runBtn.disabled = true;
    runBtn.innerHTML = `<div class="spinner"></div> Running Autonomous Multi-Agent Pipeline...`;
    progressContainer.style.display = 'block';
    progressLogs.innerHTML = '';
    resultsSection.style.display = 'none';

    appendLog('System', 'Initializing multi-agent workflow...');

    try {
      const formData = new FormData();
      formData.append('jd_text', jdText);
      if (apiKey) {
        formData.append('api_key', apiKey);
      }

      for (const file of uploadedFiles) {
        formData.append('resume_files', file);
      }

      appendLog('Pipeline', `Submitting Job Description and ${uploadedFiles.length} candidate resumes...`);

      const response = await fetch('/api/screen', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Pipeline execution failed.');
      }

      const result = await response.json();

      // Log agent progress summary
      result.candidates.forEach(cand => {
        if (cand.agent_logs) {
          cand.agent_logs.forEach(log => appendLog(log.agent, log.message));
        }
      });

      appendLog('System', `Pipeline completed in ${result.pipeline_time_seconds}s! Rendering results...`);

      // Render candidates
      renderCandidateResults(result);

    } catch (err) {
      appendLog('Error', err.message);
      alert('Screening error: ' + err.message);
    } finally {
      runBtn.disabled = false;
      runBtn.innerHTML = `
        <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
        Execute Multi-Agent Screening
      `;
    }
  });

  // Render Candidates Grid
  function renderCandidateResults(data) {
    resultsSection.style.display = 'block';
    candidateCountSpan.textContent = data.total_candidates;
    pipelineTimeSpan.textContent = data.pipeline_time_seconds;

    candidateGrid.innerHTML = '';

    data.candidates.forEach((candidate, index) => {
      const card = document.createElement('div');
      const badgeClass = `badge-${candidate.badge_color || 'amber'}`;
      card.className = `candidate-card ${badgeClass}`;

      const redFlagsCount = candidate.evaluation.red_flags ? candidate.evaluation.red_flags.length : 0;
      const greenFlagsCount = candidate.evaluation.green_flags ? candidate.evaluation.green_flags.length : 0;

      card.innerHTML = `
        <div class="candidate-top">
          <div>
            <div class="candidate-rank">Rank #${index + 1}</div>
            <div class="candidate-name">${candidate.candidate_name}</div>
          </div>
          <div class="score-badge ${badgeClass}">${Math.round(candidate.final_score)}</div>
        </div>

        <div class="rec-pill ${badgeClass}">${candidate.recommendation.replace('_', ' ')}</div>

        <p class="exec-summary">${candidate.synthesis.executive_summary || 'No summary available.'}</p>

        <div class="flags-preview">
          ${greenFlagsCount > 0 ? `<span class="flag-chip green">✓ ${greenFlagsCount} Green Flags</span>` : ''}
          ${redFlagsCount > 0 ? `<span class="flag-chip red">⚠ ${redFlagsCount} Red Flags</span>` : ''}
        </div>

        <button class="btn-detail" data-candidate-index="${index}">
          View Rubric & Interview Questions →
        </button>
      `;

      candidateGrid.appendChild(card);
    });

    // Attach click listeners to detail buttons
    document.querySelectorAll('.btn-detail').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const index = parseInt(e.currentTarget.getAttribute('data-candidate-index'));
        openCandidateModal(data.candidates[index]);
      });
    });

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
  }

  // Open Detailed Modal
  function openCandidateModal(cand) {
    const evalData = cand.evaluation;
    const synthData = cand.synthesis;
    const badgeClass = `badge-${cand.badge_color || 'amber'}`;

    let scoreMetersHTML = '';
    if (evalData.category_evaluations) {
      for (const [catKey, catVal] of Object.entries(evalData.category_evaluations)) {
        const catName = catKey.replace('_', ' ').toUpperCase();
        const score = catVal.score || 0;
        const quotes = catVal.evidence_quotes || [];
        const quoteHTML = quotes.length > 0 ? `<div class="quote-evidence">"${quotes[0]}"</div>` : '';

        scoreMetersHTML += `
          <div class="score-meter-item">
            <div class="meter-header">
              <span>${catName} (Weight: ${catVal.weight_percent}%)</span>
              <span>${score}/100</span>
            </div>
            <div class="meter-bar-bg">
              <div class="meter-bar-fill" style="width: ${score}%"></div>
            </div>
            <div class="meter-justification">${catVal.justification}</div>
            ${quoteHTML}
          </div>
        `;
      }
    }

    let questionsHTML = '';
    if (synthData.interview_questions) {
      questionsHTML = synthData.interview_questions.map((q, idx) => `
        <div class="question-card">
          <div class="q-category">${q.category}</div>
          <div class="q-text">Q${idx+1}: ${q.question}</div>
          <div class="q-rationale"><strong>Rationale:</strong> ${q.context_rationale}</div>
          <div class="q-signals">
            ${(q.ideal_answer_signals || []).map(s => `<span class="signal-tag">${s}</span>`).join('')}
          </div>
        </div>
      `).join('');
    }

    modalBody.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem;">
        <div>
          <h2 style="font-size:1.75rem; font-weight:800; color:#fff;">${cand.candidate_name}</h2>
          <div class="rec-pill ${badgeClass}" style="margin-top:0.5rem;">${cand.recommendation.replace('_', ' ')}</div>
        </div>
        <div class="score-badge ${badgeClass}" style="font-size:2rem;">${Math.round(cand.final_score)}</div>
      </div>

      <div class="modal-section">
        <div class="modal-section-title">Executive Hiring Manager Brief</div>
        <p style="color:var(--text-secondary); line-height:1.6;">${synthData.executive_summary}</p>
      </div>

      <div class="modal-section">
        <div class="modal-section-title">Rubric Category Score Breakdown</div>
        <div class="score-meter-list">
          ${scoreMetersHTML}
        </div>
      </div>

      <div class="modal-section">
        <div class="modal-section-title">Tailored Interview Questions</div>
        ${questionsHTML}
      </div>
    `;

    detailModal.style.display = 'flex';
  }

  modalCloseBtn.addEventListener('click', () => {
    detailModal.style.display = 'none';
  });

  detailModal.addEventListener('click', (e) => {
    if (e.target === detailModal) {
      detailModal.style.display = 'none';
    }
  });
});
