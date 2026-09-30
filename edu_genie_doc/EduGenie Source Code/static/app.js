const tools = {
  qa: { title: 'Ask a question', kicker: 'CLARITY ON DEMAND', description: 'Get a direct, learner-friendly answer to something you are studying.', label: 'Your question', placeholder: 'Why is the sky blue?', button: 'Get answer', endpoint: '/qa', key: 'answer', payload: 'text' },
  explain: { title: 'Explain a topic', kicker: 'MAKE IT CLICK', description: 'Break down a difficult concept with a plain-language explanation.', label: 'Topic', placeholder: 'Photosynthesis', button: 'Explain topic', endpoint: '/explain', key: 'explanation', payload: 'topic' },
  summarize: { title: 'Summarize notes', kicker: 'FIND THE SIGNAL', description: 'Reduce a long passage to the ideas worth remembering.', label: 'Passage', placeholder: 'Paste your study notes here...', button: 'Summarize', endpoint: '/summarize', key: 'summary', payload: 'text' },
  quiz: { title: 'Generate a quiz', kicker: 'CHECK YOURSELF', description: 'Create three multiple-choice questions from any topic or passage.', label: 'Topic or passage', placeholder: 'The water cycle', button: 'Generate quiz', endpoint: '/quiz', key: 'quiz', payload: 'text' },
  learn: { title: 'Build a learning path', kicker: 'KNOW WHAT IS NEXT', description: 'Move from beginner foundations to confident, practical knowledge.', label: 'What do you want to learn?', placeholder: 'Linear regression', button: 'Build path', endpoint: '/learn/recommendations', key: 'recommendation', payload: 'topic' }
};
let activeTool = 'qa';
const form = document.querySelector('#tool-form');
const input = document.querySelector('#prompt-input');
const result = document.querySelector('#result');
const body = document.querySelector('#result-body');
const count = document.querySelector('#char-count');
function selectTool(name) { activeTool = name; const tool = tools[name]; document.querySelector('#tool-kicker').textContent = tool.kicker; document.querySelector('#tool-title').textContent = tool.title; document.querySelector('#tool-description').textContent = tool.description; document.querySelector('#input-label').textContent = tool.label; input.placeholder = tool.placeholder; input.value = ''; document.querySelector('#submit-button').innerHTML = `${tool.button} <span>-></span>`; result.hidden = true; document.querySelectorAll('.tab').forEach(tab => tab.classList.toggle('active', tab.dataset.tool === name)); count.textContent = '0 / 12000'; }
document.querySelectorAll('.tab').forEach(tab => tab.addEventListener('click', () => selectTool(tab.dataset.tool)));
input.addEventListener('input', () => { count.textContent = `${input.value.length} / 12000`; });
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[char])); }
function formatInlineMarkdown(value) { return escapeHtml(value).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/\*([^*]+)\*/g, '<em>$1</em>').replace(/\$([^$\n]+)\$/g, '<span class="math">$1</span>'); }
function renderMarkdown(value) {
  const lines = String(value).split(/\r?\n/);
  let html = ''; let inList = false;
  const closeList = () => { if (inList) { html += '</ul>'; inList = false; } };
  lines.forEach(line => {
    const trimmed = line.trim();
    if (!trimmed) { closeList(); return; }
    if (/^---+$/.test(trimmed)) { closeList(); html += '<hr>'; return; }
    const heading = trimmed.match(/^(#{1,3})\s+(.+)$/);
    if (heading) { closeList(); const level = Math.min(heading[1].length + 1, 4); html += `<h${level}>${formatInlineMarkdown(heading[2])}</h${level}>`; return; }
    const bullet = trimmed.match(/^(?:[-*])\s+(.+)$/);
    if (bullet) { if (!inList) { html += '<ul>'; inList = true; } html += `<li>${formatInlineMarkdown(bullet[1])}</li>`; return; }
    closeList(); html += `<p>${formatInlineMarkdown(trimmed)}</p>`;
  });
  closeList();
  return html;
}
function renderQuiz(items) { return items.map((item, index) => `<article class="quiz-item"><h3>${index + 1}. ${escapeHtml(item.question)}</h3>${(item.options || []).map(option => `<label class="option"><input type="radio" name="q${index}" value="${escapeHtml(option)}"><span>${escapeHtml(option)}</span></label>`).join('')}<button class="check-answer" data-answer="${escapeHtml(item.answer)}">Check answer</button><p class="feedback" hidden></p></article>`).join(''); }
form.addEventListener('submit', async event => { event.preventDefault(); const value = input.value.trim(); if (!value) return; const tool = tools[activeTool]; const submit = document.querySelector('#submit-button'); submit.disabled = true; submit.innerHTML = 'Thinking <span>...</span>'; result.hidden = false; body.innerHTML = '<p class="loading">Preparing your response...</p>'; try { const response = await fetch(tool.endpoint, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ [tool.payload]: value }) }); const data = await response.json(); if (!response.ok) throw new Error(data.detail || data.error || 'Request failed'); body.innerHTML = tool.key === 'quiz' ? renderQuiz(data[tool.key]) : `<div class="rich-text">${renderMarkdown(data[tool.key])}</div>`; } catch (error) { body.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`; } finally { submit.disabled = false; submit.innerHTML = `${tool.button} <span>-></span>`; } });
body.addEventListener('click', event => { if (!event.target.classList.contains('check-answer')) return; const item = event.target.closest('.quiz-item'); const selected = item.querySelector('input:checked'); const feedback = item.querySelector('.feedback'); feedback.hidden = false; feedback.textContent = selected && selected.value === event.target.dataset.answer ? 'Correct. Keep going.' : `Not quite. Correct answer: ${event.target.dataset.answer}`; feedback.className = `feedback ${selected && selected.value === event.target.dataset.answer ? 'correct' : 'incorrect'}`; });
