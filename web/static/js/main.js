// BMI 噗噗星球：前端只負責畫面、動畫與歷史紀錄，實際 BMI 計算與分類一律呼叫
// 後端 /api/bmi（重用 app.py 的 calculate_bmi/classify_bmi），避免前後端邏輯漂移。

const THRESH = {under:18.5, normal:24, over:27}; // 僅用於畫量表分區顏色，非計算依據
const COLORS = {under:'#8ec7ff', normal:'#5fd39a', over:'#ffcf5c', obese:'#ff7d7d'};

const GMIN=10, GMAX=40, CX=150, CY=150, R=120;
function angleForBmi(bmi){
  const clamped = Math.min(GMAX, Math.max(GMIN, bmi));
  return 180 - (clamped - GMIN) / (GMAX - GMIN) * 180;
}
function pointFor(angleDeg, radius){
  const rad = angleDeg * Math.PI / 180;
  return { x: CX + radius * Math.cos(rad), y: CY - radius * Math.sin(rad) };
}
function arcPath(bmiA, bmiB){
  const a1 = angleForBmi(bmiA), a2 = angleForBmi(bmiB);
  const p1 = pointFor(a1, R), p2 = pointFor(a2, R);
  return `M ${p1.x} ${p1.y} A ${R} ${R} 0 0 1 ${p2.x} ${p2.y}`;
}
document.getElementById('track-under').setAttribute('d', arcPath(GMIN, THRESH.under));
document.getElementById('track-under').setAttribute('stroke', COLORS.under);
document.getElementById('track-normal').setAttribute('d', arcPath(THRESH.under, THRESH.normal));
document.getElementById('track-normal').setAttribute('stroke', COLORS.normal);
document.getElementById('track-over').setAttribute('d', arcPath(THRESH.normal, THRESH.over));
document.getElementById('track-over').setAttribute('stroke', COLORS.over);
document.getElementById('track-obese').setAttribute('d', arcPath(THRESH.over, GMAX));
document.getElementById('track-obese').setAttribute('stroke', COLORS.obese);

let needleState = { angle: 180 };
function setNeedle(bmi, animate){
  const target = angleForBmi(bmi);
  const draw = () => {
    const p = pointFor(needleState.angle, R - 20);
    document.getElementById('needle').setAttribute('x2', p.x);
    document.getElementById('needle').setAttribute('y2', p.y);
    const rp = pointFor(needleState.angle, R + 15);
    document.getElementById('rocket').setAttribute('x', rp.x);
    document.getElementById('rocket').setAttribute('y', rp.y);
  };
  if (animate) {
    gsap.to(needleState, { angle: target, duration: 1.1, ease: 'elastic.out(1,0.6)', onUpdate: draw });
  } else {
    needleState.angle = target; draw();
  }
}
setNeedle(GMIN, false);

const HISTORY_KEY = 'bmiHistory_conceptA';
function loadHistory(){ try { return JSON.parse(localStorage.getItem(HISTORY_KEY)) || []; } catch(e){ return []; } }
function saveHistory(list){ localStorage.setItem(HISTORY_KEY, JSON.stringify(list)); }

let chart;
function renderChart(){
  const history = loadHistory();
  const ctx = document.getElementById('historyChart');
  const data = {
    labels: history.map((h,i)=>`#${i+1}`),
    datasets: [{
      label: 'BMI', data: history.map(h=>h.bmi),
      borderColor: '#ff7fa3', backgroundColor:'rgba(255,127,163,.15)', fill:true, tension:.35,
      pointBackgroundColor: history.map(h=>COLORS[h.category]), pointRadius:6
    }]
  };
  if (chart) { chart.data = data; chart.update(); }
  else {
    chart = new Chart(ctx, { type:'line', data, options:{ animation:{duration:900}, plugins:{legend:{display:false}},
      scales:{ y:{ suggestedMin:10, suggestedMax:35 } } } });
  }
}
renderChart();

function countUp(el, target){
  const obj = { v: 0 };
  gsap.to(obj, { v: target, duration: 1.2, ease:'power2.out',
    onUpdate: () => el.textContent = obj.v.toFixed(2) });
}

function showError(message){
  const badge = document.getElementById('badge');
  badge.textContent = message;
  badge.style.background = '#9a9ab0';
  document.getElementById('bmiNum').textContent = '--';
}

document.getElementById('launchBtn').addEventListener('click', async () => {
  const weight = parseFloat(document.getElementById('weight').value);
  const height = parseFloat(document.getElementById('height').value);
  if (!weight || !height) return;

  gsap.fromTo('#launchBtn', {x:0}, {x:4, duration:.05, yoyo:true, repeat:5});
  gsap.fromTo('#mascot', {rotate:-6}, {rotate:6, duration:.15, yoyo:true, repeat:3, transformOrigin:'50% 50%'});
  flyRocket(document.getElementById('launchBtn'), document.getElementById('bmiNum'));
  tiltGaugeReveal();

  let result;
  try {
    const res = await fetch('/api/bmi', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ weight, height })
    });
    const data = await res.json();
    if (!res.ok) { showError(data.error || '發生錯誤，請確認輸入'); return; }
    result = data;
  } catch (e) {
    showError('無法連線到伺服器');
    return;
  }

  const { bmi, category, label } = result;
  const badge = document.getElementById('badge');
  badge.textContent = label;
  badge.style.background = COLORS[category];

  countUp(document.getElementById('bmiNum'), bmi);
  setNeedle(bmi, true);

  const history = loadHistory();
  history.push({ t: Date.now(), weight, height, bmi, category });
  saveHistory(history);
  renderChart();

  if (category === 'normal') {
    confetti({ particleCount: 120, spread: 70, origin: { y: 0.6 }, colors:['#ff9fc0','#ffe3a3','#a3f7c8'] });
  }
});

// ---- D3.js 2.5D 效果區 --------------------------------------------------

// 靜態等角傾斜：用仿射 skew + scale 讓量表看起來像放在傾斜桌面上（2.5D 景深）。
d3.select('#gaugeGroup').attr('transform', 'skewX(-6) scale(1,0.94)');

// 送出結果時，用 d3.interpolateTransformCss 內插 transform 字串，
// 讓量表卡片做一次「傾斜翻面再回正」的 2.5D 揭曉動畫。
function tiltGaugeReveal(){
  const wrap = d3.select('.gauge-wrap');
  const flat = 'skewY(0deg) scale(1) rotateX(0deg)';
  const tilted = 'skewY(-4deg) scale(1.05) rotateX(8deg)';
  wrap.style('transform-style', 'preserve-3d');
  wrap.transition().duration(650)
    .styleTween('transform', () => d3.interpolateTransformCss(flat, tilted))
    .transition().duration(650)
    .styleTween('transform', () => d3.interpolateTransformCss(tilted, flat));
}

// 周邊飄浮 emoji：用 d3.scaleLinear 把隨機「深度」映射成大小/透明度/飛行速度，
// 製造近大快、遠小慢的 2.5D 視差效果；實際位移仍由 GSAP 補間。
const floatLayer = document.getElementById('floatLayer');
const FLOAT_EMOJIS = ['⭐','✨','🪐','☁️','🌙','💫','🛸','🎈'];
const depthToScale = d3.scaleLinear().domain([0, 1]).range([0.6, 1.6]);
const depthToOpacity = d3.scaleLinear().domain([0, 1]).range([0.25, 0.85]);
const depthToDuration = d3.scaleLinear().domain([0, 1]).range([26, 12]);

function spawnFloaty(){
  const depth = Math.random(); // 0 = 遠景, 1 = 近景
  const el = document.createElement('div');
  el.textContent = FLOAT_EMOJIS[Math.floor(Math.random()*FLOAT_EMOJIS.length)];
  el.style.cssText = `position:absolute; font-size:22px; opacity:${depthToOpacity(depth)};
    transform:scale(${depthToScale(depth)}); will-change:transform; filter:blur(${(1-depth)*1.2}px);`;
  floatLayer.appendChild(el);
  const fly = () => {
    const startX = Math.random()*window.innerWidth;
    const endX = Math.random()*window.innerWidth;
    gsap.set(el, { x:startX, y:window.innerHeight+40, rotate: Math.random()*360 });
    gsap.to(el, {
      x:endX, y:-60, rotate:`+=${180+Math.random()*360}`,
      duration: depthToDuration(depth), ease:'none', onComplete: fly
    });
  };
  fly();
}
for (let i=0; i<16; i++) spawnFloaty();

// 小火箭從發射按鈕飛向結果數字，沿途灑落拖尾粒子帶出轉場。
// 用兩段式補間（起點→中繼高點→終點）模擬弧線飛行，避免依賴額外的 GSAP 外掛。
function flyRocket(fromEl, toEl){
  const fr = fromEl.getBoundingClientRect();
  const tr = toEl.getBoundingClientRect();
  const rocket = document.createElement('div');
  rocket.textContent = '🚀';
  rocket.style.cssText = 'position:fixed; font-size:28px; z-index:40; pointer-events:none; left:0; top:0;';
  document.body.appendChild(rocket);
  const startX = fr.left + fr.width/2, startY = fr.top;
  const midX = (fr.left+tr.left)/2, midY = Math.min(fr.top, tr.top) - 140;
  const endX = tr.left + tr.width/2, endY = tr.top + tr.height/2;
  const pos = { x:startX, y:startY };
  gsap.set(rocket, { x:pos.x, y:pos.y, rotate:-90 });
  const spark = () => {
    if (Math.random() < .35) {
      confetti({ particleCount:2, startVelocity:3, spread:30, ticks:35, gravity:.4,
        origin:{ x:pos.x/window.innerWidth, y:pos.y/window.innerHeight }, colors:['#ffd9c7','#ff9fc0','#fff2a8'] });
    }
  };
  gsap.timeline({ onComplete: () => rocket.remove() })
    .to(pos, { x:midX, y:midY, duration:.55, ease:'power1.out',
      onUpdate(){ gsap.set(rocket, { x:pos.x, y:pos.y }); spark(); } })
    .to(rocket, { rotate:0, duration:.2 }, '<')
    .to(pos, { x:endX, y:endY, duration:.55, ease:'power1.in',
      onUpdate(){ gsap.set(rocket, { x:pos.x, y:pos.y }); spark(); } });
}

// 磁吸按鈕：滑鼠靠近時輕輕追隨游標。
const launchBtn = document.getElementById('launchBtn');
launchBtn.addEventListener('mousemove', (e) => {
  const r = launchBtn.getBoundingClientRect();
  gsap.to(launchBtn, { x:(e.clientX-r.left-r.width/2)*.25, y:(e.clientY-r.top-r.height/2)*.5, duration:.3 });
});
launchBtn.addEventListener('mouseleave', () => gsap.to(launchBtn, { x:0, y:0, duration:.5, ease:'elastic.out(1,0.4)' }));

// 卡片進場動畫。滑鼠懸浮傾斜互動要等進場動畫完全結束後才綁定，
// 避免兩個 GSAP tween 同時搶奪同一個元素的 transform，導致進場動畫卡在半透明。
gsap.from('.card', {
  y:60, opacity:0, duration:.9, stagger:.15, ease:'back.out(1.4)',
  onComplete(){
    document.querySelectorAll('.card').forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left)/r.width - .5, py = (e.clientY - r.top)/r.height - .5;
        gsap.to(card, { rotateY: px*6, rotateX: -py*6, transformPerspective:600, duration:.4 });
      });
      card.addEventListener('mouseleave', () => gsap.to(card, { rotateX:0, rotateY:0, duration:.6 }));
    });
  }
});
