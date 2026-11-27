'use strict';
(() => {
  const data = window.AI4MATH_DEMO;
  const windowSelect = document.getElementById('window');
  const lambdaSelect = document.getElementById('lambda');
  const tbody = document.getElementById('scores');
  function render() {
    const key = `${windowSelect.value}:${lambdaSelect.value}`;
    const result = data.scenarios[key];
    const max = Math.max(...result.score, 1e-12);
    tbody.replaceChildren();
    const order = data.fields.map((_, i) => i).sort((a, b) => result.score[b] - result.score[a] || a - b);
    for (const i of order) {
      const tr = document.createElement('tr');
      for (const value of [data.fields[i], result.velocity[i].toFixed(3), result.score[i].toFixed(3)]) {
        const td = document.createElement('td'); td.textContent = value; tr.append(td);
      }
      const td = document.createElement('td');
      const bar = document.createElement('span'); bar.className = 'bar'; bar.setAttribute('aria-hidden', 'true');
      const fill = document.createElement('span'); fill.style.width = `${100 * result.score[i] / max}%`;
      bar.append(fill); td.append(bar); tr.append(td); tbody.append(tr);
    }
    document.getElementById('scenario').textContent = `合成数据 · 截断 ${data.cutoff} · 历史窗口 ${windowSelect.value} 天 · λ = ${lambdaSelect.value} · 活动分数，不是概率`;
  }
  windowSelect.addEventListener('change', render);
  lambdaSelect.addEventListener('change', render);
  document.getElementById('reset').addEventListener('click', () => {
    windowSelect.value = '180'; lambdaSelect.value = '0.5'; render();
  });
  render();
})();
