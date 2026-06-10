import fs from 'fs';
import vm from 'vm';
import path from 'path';

const root = path.resolve('th062/ecl_sources');
const context = { console };
vm.createContext(context);
for (const file of ['priw8-ins.js', 'priw8-vars.js']) {
  let code = fs.readFileSync(path.join(root, file), 'utf8');
  code = code.replace(/const\s+([A-Z0-9_]+)\s*=/g, 'this.$1 =');
  vm.runInContext(code, context, { filename: file });
}

const gameInfo = [
  { key: 8, suffix: '08', code: 'TH08', title: '东方永夜抄', generation: '第一世代', ins: true, vars: true },
  { key: 10, suffix: '10', code: 'TH10', title: '东方风神录', generation: '第二世代', ins: false, vars: true },
  { key: 11, suffix: '11', code: 'TH11', title: '东方地灵殿', generation: '第二世代', ins: false, vars: true },
  { key: 12, suffix: '12', code: 'TH12', title: '东方星莲船', generation: '第三世代', ins: false, vars: true },
  { key: 125, suffix: '125', code: 'TH12.5', title: 'Double Spoiler', generation: '第三世代', ins: false, vars: true },
  { key: 128, suffix: '128', code: 'TH12.8', title: '妖精大战争', generation: '第三世代', ins: false, vars: true },
  { key: 13, suffix: '13', code: 'TH13', title: '东方神灵庙', generation: '第四世代', ins: true, vars: true },
  { key: 14, suffix: '14', code: 'TH14', title: '东方辉针城', generation: '第四世代', ins: true, vars: true },
  { key: 143, suffix: '143', code: 'TH14.3', title: '弹幕天邪鬼', generation: '第四世代', ins: true, vars: true },
  { key: 15, suffix: '15', code: 'TH15', title: '东方绀珠传', generation: '第四世代', ins: true, vars: true },
  { key: 16, suffix: '16', code: 'TH16', title: '东方天空璋', generation: '第四世代', ins: true, vars: true },
  { key: 165, suffix: '165', code: 'TH16.5', title: '秘封噩梦日记', generation: '第四世代', ins: true, vars: true },
  { key: 17, suffix: '17', code: 'TH17', title: '东方鬼形兽', generation: '第四世代', ins: true, vars: true },
  { key: 18, suffix: '18', code: 'TH18', title: '东方虹龙洞', generation: '第四世代', ins: true, vars: false },
  { key: 185, suffix: '185', code: 'TH18.5', title: '弹幕狂们的黑市', generation: '第四世代', ins: true, vars: false },
];

const thbwikiFiles = [
  { file: 'th062/ecl.txt', title: '脚本对照表/ECL 总览', generation: '总览' },
  { file: 'th062/ecl1.txt', title: 'THBWiki 第一世代 ECL', generation: '第一世代' },
  { file: 'th062/ecl2.txt', title: 'THBWiki 第二世代 ECL', generation: '第二世代' },
  { file: 'th062/ecl3.txt', title: 'THBWiki 第三世代 ECL', generation: '第三世代' },
  { file: 'th062/ecl4.txt', title: 'THBWiki 第四世代 ECL', generation: '第四世代' },
];

const generationGames = {
  '第一世代': '红魔乡、妖妖梦、永夜抄、花映塚、文花帖；其中妖妖梦/永夜抄/花映塚/文花帖存在新增差异。',
  '第二世代': '风神录、地灵殿；地灵殿存在新增指令。',
  '第三世代': '星莲船、Double Spoiler、妖精大战争；THBWiki 以 TH12 为主体，DS/大战争有少量差异。',
  '第四世代': '神灵庙之后的整数作与小数作；页面标注辉针城、天邪鬼、绀珠传、天空璋、噩梦日记、鬼形兽等新增差异。',
};

const groupZh = {
  'Normal': '普通指令',
  'Timeline': '时间轴指令',
  'System': '系统/流程/栈/算术',
  'Enemy creation and ANM script management': '敌机创建与 ANM 管理',
  'Movement management': '移动管理',
  'Enemy property management and other miscellaneous things': '敌机属性与杂项',
  'Bullet creation and deletion': '子弹创建与删除',
  'Laser creation': '激光创建',
  'Enemy interaction': '敌机交互',
  'Debug': '调试',
  'Game specific': '游戏特有',
};

function normalizeGameVersion(num) {
  if (typeof num === 'string') num = parseFloat(num);
  while (Math.floor(num) !== num) num *= 10;
  return num;
}
function obj(name) { return context[name] || {}; }
function getGroups(game) { return obj(`GROUPS_${game}`) || []; }
function getVarLimits(game) { return context[`VARLIMIT_${game}`]; }
function getVarFromList(list, id) {
  const ret = list[id];
  if (typeof ret === 'undefined') return null;
  return ret;
}
function getVarNoCheck(game, id) {
  let ret = null;
  switch (game) {
    case 18: ret = getVarFromList(obj('VAR_18'), id);
    case 17: if (!ret) ret = getVarFromList(obj('VAR_17'), id);
    case 165: if (!ret) ret = getVarFromList(obj('VAR_165'), id);
    case 16: if (!ret) ret = getVarFromList(obj('VAR_16'), id);
    case 15: if (!ret) ret = getVarFromList(obj('VAR_15'), id);
    case 143: if (!ret) ret = getVarFromList(obj('VAR_143'), id);
    case 14: if (!ret) ret = getVarFromList(obj('VAR_14'), id);
    case 13: if (!ret) ret = getVarFromList(obj('VAR_13'), id);
    case 128: if (!ret) ret = getVarFromList(obj('VAR_128'), id);
    case 125: if (!ret) ret = getVarFromList(obj('VAR_125'), id);
    case 12: if (!ret) ret = getVarFromList(obj('VAR_12'), id);
    case 11: if (!ret) ret = getVarFromList(obj('VAR_11'), id);
    case 10: if (!ret) ret = getVarFromList(obj('VAR_10'), id); break;
    case 8: if (!ret) ret = getVarFromList(obj('VAR_8'), id);
  }
  return ret;
}
function getOpcodeFromList(list, num) {
  const ret = list[num];
  if (typeof ret === 'undefined') return null;
  if (ret == null) return { number: -1, game: -1, args: '', argnames: [], description: '', documented: false };
  return ret;
}
function getOpcodeNoCheck(game, num, timeline=false) {
  let ret = null;
  if (timeline) return getOpcodeFromList(obj(`INS_${game}`), num);
  switch (game) {
    case 185:
      ret = getOpcodeFromList(obj('INS_185'), num); if (ret) { if (ret.noInherit && ret.game !== 185) ret = null; else break; }
    case 18:
      ret = getOpcodeFromList(obj('INS_18'), num); if (ret) { if (ret.noInherit && ret.game !== 18) ret = null; else break; }
    case 17:
      ret = getOpcodeFromList(obj('INS_17'), num); if (ret) { if (ret.noInherit && ret.game !== 17) ret = null; else break; }
    case 165:
      ret = getOpcodeFromList(obj('INS_165'), num); if (ret) { if (ret.noInherit && ret.game !== game) ret = null; else break; }
    case 16:
      ret = getOpcodeFromList(obj('INS_16'), num); if (ret) { if (ret.noInherit && ret.game !== game) ret = null; else break; }
    case 15:
      ret = getOpcodeFromList(obj('INS_15'), num); if (ret) { if (ret.noInherit && ret.game !== game) ret = null; else break; }
    case 143:
      ret = getOpcodeFromList(obj('INS_143'), num); if (ret) { if (ret.noInherit && ret.game !== game) ret = null; else break; }
    case 14:
      ret = getOpcodeFromList(obj('INS_14'), num); if (ret) { if (ret.noInherit && ret.game !== game) ret = null; else break; }
    case 13:
      ret = getOpcodeFromList(obj('INS_13'), num); if (ret) { if (ret.noInherit && ret.game !== game) ret = null; else break; }
    case 8:
      ret = getOpcodeFromList(obj('INS_8'), num);
  }
  return ret;
}

function parseEclmap(file) {
  const text = fs.existsSync(file) ? fs.readFileSync(file, 'utf8').replace(/\r/g, '') : '';
  const map = { ins: {}, timeline: {}, vars: {}, types: {} };
  let section = '';
  for (let raw of text.split('\n')) {
    const line = raw.replace(/#.*/, '').trim();
    if (!line) continue;
    if (line.startsWith('!')) { section = line; continue; }
    const m = line.match(/^(-?\d+)\s+(.+)$/);
    if (!m) continue;
    const id = Number(m[1]);
    const value = m[2].trim();
    if (section === '!ins_names') map.ins[id] = value;
    else if (section === '!timeline_ins_names') map.timeline[id] = value;
    else if (section === '!gvar_names') map.vars[id] = value;
    else if (section === '!gvar_types') map.types[id] = value;
  }
  return map;
}
const maps = Object.fromEntries(gameInfo.map(g => [g.key, parseEclmap(path.join(root, 'eclmap', `th${g.suffix}.eclm`))]));

function esc(s) {
  return String(s ?? '')
    .replace(/\r?\n/g, '<br>')
    .replace(/\|/g, '\\|')
    .replace(/\[br\]/g, '<br>')
    .replace(/\[hr\]/g, '---')
    .replace(/\[c=red\]/g, '')
    .replace(/\[c=lightgreen\]/g, '')
    .replace(/\[\/c\]/g, '')
    .replace(/\[game=([^\]]+)\]([^[]+)\[\/game\]/g, '$2')
    .replace(/\[ins=([^,\]]+),?[^\]]*\]/g, 'ins_$1')
    .replace(/\[var(?:_notip)?=([^,\]]+),?[^\]]*\]/g, 'var_$1')
    .replace(/\[#s=([^\]]+)\]/g, '$1')
    .replace(/\s+/g, ' ')
    .trim();
}
function args(op) {
  if (!op) return '';
  const names = op.argnames || [];
  if (!op.args && names.length === 0) return '—';
  return `${op.args || ''}${names.length ? ` (${names.join(', ')})` : ''}`;
}
function origin(op, currentGame) {
  if (!op) return '';
  return op.game === currentGame ? '本作' : `继承自 ${formatGame(op.game)}`;
}
function formatGame(key) {
  const g = gameInfo.find(x => x.key === key);
  return g ? g.code : `TH${key}`;
}
function groupOf(groups, id, timeline=false) {
  const g = groups.find(x => !!x.timeline === timeline && id >= x.min && id <= x.max);
  if (!g) return '未分组';
  const zh = groupZh[g.title] || g.title;
  return zh === g.title ? zh : `${zh} / ${g.title}`;
}
function varType(v, fallbackType) {
  const t = v?.type || fallbackType;
  return t === '%' ? 'float' : 'int';
}
function accessZh(v) { return v?.access === 'rw' ? '读写' : '只读'; }
function scopeZh(v) { return v?.scope === 'l' ? 'local/敌机局部' : 'global/全局'; }

function instructionRows(g, timeline=false) {
  const groups = getGroups(g.key).filter(x => !!x.timeline === timeline);
  const ids = new Set();
  for (const gr of groups) for (let i = gr.min; i <= gr.max; i++) ids.add(i);
  if (ids.size === 0 && !timeline) {
    for (const k of Object.keys(obj(`INS_${g.key}`))) ids.add(Number(k));
  }
  return [...ids].sort((a,b)=>a-b).map(id => {
    const op = getOpcodeNoCheck(g.key, id, timeline);
    const name = timeline ? maps[g.key].timeline[id] : maps[g.key].ins[id];
    return {
      id,
      name: name || `ins_${id}`,
      group: groupOf(getGroups(g.key), id, timeline),
      args: op ? args(op) : '—',
      desc: op ? esc(op.description) : '未在 Priw8 表中记录/待确认',
      documented: op ? (op.documented ? '是' : '否/待确认') : '否/待确认',
      origin: op ? origin(op, g.key) : '—',
    };
  });
}
function variableRows(g) {
  const lim = getVarLimits(g.key);
  if (!lim) return [];
  const rows = [];
  for (let id = lim[0]; id <= lim[1]; id++) {
    const v = getVarNoCheck(g.key, id);
    if (!v) continue;
    rows.push({
      id: v.type === '$' ? String(id) : `${id}.0f`,
      name: maps[g.key].vars[id] || `[${id}]`,
      type: varType(v, maps[g.key].types[id]),
      access: accessZh(v),
      scope: scopeZh(v),
      desc: esc(v.desc),
      documented: v.documented ? '是' : '否/待确认',
      origin: v.game === g.key ? '本作' : `继承自 ${formatGame(v.game)}`,
    });
  }
  return rows;
}
function mdTable(headers, rows) {
  const out = [];
  out.push(`| ${headers.join(' | ')} |`);
  out.push(`| ${headers.map(()=> '---').join(' | ')} |`);
  for (const row of rows) out.push(`| ${row.map(esc).join(' | ')} |`);
  return out.join('\n');
}

function extractThbwikiOverview(text) {
  const matches = [...text.matchAll(/^概述\s*$/gm)];
  if (!matches.length) return '';
  const start = matches[matches.length - 1].index + matches[matches.length - 1][0].length;
  const nextHead = text.slice(start).search(/\n(?:通用|弹幕系|单位系|特殊系|特殊变量表|设置贴图.*|单位移动.*|单位固有属性.*|弹幕相关.*|\d+系\s+.*)\n/);
  const end = nextHead >= 0 ? start + nextHead : Math.min(text.length, start + 1200);
  let overview = text.slice(start, end).trim().split('\n').map(x => x.trim()).filter(Boolean).join(' ');
  if (overview.length > 500) overview = `${overview.slice(0, 500)}…`;
  return overview;
}

function isThbwikiHeading(line) {
  return /^(概述|通用|弹幕系|单位系|特殊系|特殊变量表|设置贴图|单位移动|单位固有属性|弹幕相关|激光相关|单位互动|Debug|备用|子弹类型|变换列表|FLAG表|Flag表|\d+系\s+|\d+[-\d]+指令详解|\d+指令详解|辉针城|天邪鬼|绀珠传|天空璋|噩梦日记|兽王园)/.test(line);
}

function thbwikiSectionName(text, offset) {
  const before = text.slice(0, offset).split('\n').map(x => x.trim()).filter(Boolean);
  for (let i = before.length - 1; i >= 0; --i) {
    const line = before[i];
    if (isThbwikiHeading(line)) {
      return line;
    }
  }
  return '未分组';
}

function parseThbwikiOpcodes(file) {
  if (!fs.existsSync(file) || fs.statSync(file).size === 0) return { overview: '', rows: [] };
  const text = fs.readFileSync(file, 'utf8').replace(/\r/g, '');
  const matches = [...text.matchAll(/^(\d{1,4})(?:-(\d{1,4}))?\(([^\n]*)\);?\s*(.*)$/gm)];
  const rows = [];
  for (let i = 0; i < matches.length; ++i) {
    const match = matches[i];
    const start = match.index;
    const end = match.index + match[0].length;
    let next = i + 1 < matches.length ? matches[i + 1].index : text.length;
    const heading = text.slice(end, next).search(/\n[^\n]+\n/);
    if (heading >= 0) {
      const lines = text.slice(end, next).split('\n');
      let consumed = 0;
      for (const line of lines) {
        if (line && isThbwikiHeading(line.trim())) break;
        consumed += line.length + 1;
      }
      next = Math.min(next, end + consumed);
    }
    let desc = `${match[4] || ''}\n${text.slice(end, next)}`
      .split('\n')
      .map(x => x.trim())
      .filter(Boolean)
      .filter(x => !/^目录$|^跳到导航跳到搜索$|^<\s*脚本对照表/.test(x))
      .join(' ');
    desc = desc.replace(/\s+/g, ' ').trim();
    if (desc.length > 320) desc = `${desc.slice(0, 320)}…`;
    const id = match[2] ? `${match[1]}-${match[2]}` : match[1];
    rows.push([id, match[3].trim() || '—', thbwikiSectionName(text, start), desc || '—']);
  }
  return { overview: extractThbwikiOverview(text), rows };
}

function thbwikiSummaryRows() {
  return thbwikiFiles.map(entry => {
    const parsed = parseThbwikiOpcodes(entry.file);
    return [entry.generation, entry.title, entry.file, generationGames[entry.generation] || '见总览页面。', parsed.rows.length, parsed.overview || (fs.existsSync(entry.file) && fs.statSync(entry.file).size === 0 ? '文件为空。' : '—')];
  });
}
function instructionSummary(g) {
  if (!g.ins) return 'ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。';
  const normal = instructionRows(g, false);
  const timeline = instructionRows(g, true);
  const total = normal.length + timeline.length;
  const documented = [...normal, ...timeline].filter(x => x.documented === '是').length;
  const groups = [...new Set(normal.map(x => x.group))].join('；');
  return `普通指令 ${normal.length} 条${timeline.length ? `，时间轴指令 ${timeline.length} 条` : ''}；已说明 ${documented}/${total}。主要分组：${groups}。`;
}
function variableSummary(g) {
  if (!g.vars) return 'ecl-web.txt 未列出该作变量表。';
  const rows = variableRows(g);
  const lim = getVarLimits(g.key);
  return `变量范围 ${lim[0]}..${lim[1]}；本文列出有说明/命名记录的 ${rows.length} 条，未列空洞/未知项。`;
}

const sources = fs.readFileSync('th062/ecl-web.txt', 'utf8').trim().split('\n');
const splitOutputDir = 'th062/ecl-by-game';

function headerText() {
  let out = '';
  out += '> 根据 `th062/ecl-web.txt` 中列出的 Priw8 ECL 指令表、变量表、flags/MERLIN 文档，以及本地提供的 THBWiki 文本 `th062/ecl*.txt` 整理。具体 opcode/变量主表以 Priw8 源数据为准，THBWiki 中文说明作为代际补充与交叉索引。\n\n';
  out += '## 阅读说明\n\n';
  out += '- `ID` 为 ECL opcode 或变量编号；`助记名` 来自 priw8 的 eclmap。\n';
  out += '- `参数` 中前半为格式串，括号内为参数名；`S/$` 常见为整数，`f/%` 常见为浮点，`o` 常见为跳转 offset/label。\n';
  out += '- `来源` 表示该条在 Priw8 继承链中的定义来源；第四世代大量指令会从 TH13 继承。\n';
  out += '- 变量表只列有记录的变量；范围内未列出的编号通常为空洞或未调查。\n\n';
  return out;
}

function sourceIndexSection() {
  let out = '## 来源网页索引\n\n';
  out += mdTable(['序号', '用途', 'URL'], sources.map((url, i) => {
    const purpose = url.includes('modding/ins') ? 'Priw8 指令表' : url.includes('modding/vars') ? 'Priw8 变量表' : url.includes('modding/flags') ? '敌机 flags' : url.includes('MERLIN') ? 'MERLIN 敌机常量' : 'THBWiki ECL';
    return [String(i+1), purpose, url];
  }));
  out += '\n\n## THBWiki 本地文本索引\n\n';
  out += mdTable(['代际', '标题', '文件', '适用范围', '抽取 opcode 数', '概述摘要'], thbwikiSummaryRows());
  out += '\n\n';
  return out;
}

function gameOverviewSection() {
  let out = '## 游戏总览\n\n';
  out += mdTable(['游戏', '作品', '代际/体系', '指令表覆盖', '变量表覆盖', '摘要'], gameInfo.map(g => [g.code, g.title, g.generation, g.ins ? '有' : '未列', g.vars ? '有' : '未列', `${instructionSummary(g)} ${variableSummary(g)}`]));
  out += '\n\n';
  return out;
}

function thbwikiGenerationEntriesForGame(g) {
  if (g.key === 8) return thbwikiFiles.filter(x => x.generation === '第一世代');
  if (g.key === 10 || g.key === 11) return thbwikiFiles.filter(x => x.generation === '第二世代');
  if ([12, 125, 128].includes(g.key)) return thbwikiFiles.filter(x => x.generation === '第三世代');
  if (g.key >= 13) return thbwikiFiles.filter(x => x.generation === '第四世代');
  return [];
}

function thbwikiGenerationSection(entries = thbwikiFiles) {
  let out = '## THBWiki 中文代际补充\n\n';
  out += '这些表保留 THBWiki 中文页面中的签名和说明，便于和 Priw8 分游戏 opcode 表互查；同一 opcode 的英文精确定义仍见各游戏主表。\n\n';
  for (const entry of entries) {
    const parsed = parseThbwikiOpcodes(entry.file);
    if (!parsed.rows.length) continue;
    out += `### ${entry.title}\n\n`;
    out += `- 适用范围：${generationGames[entry.generation] || '见总览页面。'}\n`;
    if (parsed.overview) out += `- 页面概述：${esc(parsed.overview)}\n`;
    out += `- 抽取 opcode：${parsed.rows.length} 条。\n\n`;
    out += mdTable(['ID', 'THBWiki 参数签名', '章节', '中文说明摘要'], parsed.rows);
    out += '\n\n';
  }
  return out;
}

function flagsSection() {
  let out = '## 敌机 Flags 速查\n\n';
  out += '### TH13-TH17/第四世代常用 Flags（MERLIN 常量）\n\n';
  out += mdTable(['Bit', '十进制', 'MERLIN 常量', '效果'], [
    ['0','1','FLAG_NO_HURTBOX','禁用 hurtbox，不能被自机子弹击中。'],
    ['1','2','FLAG_NO_HITBOX','禁用 hitbox，不能通过撞击击杀玩家。'],
    ['2','4','FLAG_OFFSCREEN_LR','离开屏幕左右边界时不删除敌机。'],
    ['3','8','FLAG_OFFSCREEN_UD','离开屏幕上下边界时不删除敌机。'],
    ['4','16','FLAG_INVINCIBLE','敌机无敌；若为 Boss，会隐藏血条。'],
    ['5','32','FLAG_INTANGIBLE','无形：同时具备 bit0/bit1 效果，并防止被部分清敌 opcode 删除。'],
    ['6','64','—','未知效果。'],
    ['7','128','FLAG_NO_DELETE','防止被 518/525 等清敌 opcode 删除。'],
    ['8','256','FLAG_ALWAYS_DELETE','保证会被 518/525 删除，无视其他 flag。'],
    ['9','512','FLAG_GRAZE','敌机可擦弹，类似激光的连续擦弹。'],
    ['10','1024','FLAG_ONLY_DIALOG_DELETE','防止被 525 删除，但对话出现时死亡。'],
    ['11','2048','FLAG_ETCLEAR_DIE','被 615 等清弹类处理杀死。'],
    ['12','4096','FLAG_RECT_HITBOX','敌机碰撞盒改为矩形而非椭圆。'],
    ['13','8192','FLAG_NO_TIMESTOP','TH14.3 中不受 547 影响；其他作品未知/无效果。'],
  ]);
  out += '\n\n补充常量：`FLAG_NO_COLLISION = FLAG_NO_HURTBOX | FLAG_NO_HITBOX`；`FLAG_OFFSCREEN_UDLR = FLAG_OFFSCREEN_LR | FLAG_OFFSCREEN_UD`。\n\n';
  out += '### TH08 Flags\n\n';
  out += mdTable(['Bit', '十进制', '效果'], [
    ['0','1','禁用 hurtbox，不能被自机子弹击中。'],
    ['1','2','禁用 hitbox，不能通过撞击击杀玩家。'],
    ['2','4','无敌/不受伤害。'],
    ['3','8','敌机不可见，且 hitbox/hurtbox 都禁用。'],
    ['4','16','敌机离开屏幕也不删除。'],
    ['5','32','类似或等同于十进制 4，差异未知。'],
  ]);
  out += '\n\n';
  return out;
}

function gameSection(g, level = 2) {
  const h = '#'.repeat(level);
  let out = `${h} ${g.code} ${g.title}\n\n`;
  out += `- 体系：${g.generation}\n`;
  out += `- 指令：${instructionSummary(g)}\n`;
  out += `- 变量：${variableSummary(g)}\n\n`;
  if (g.ins) {
    const normal = instructionRows(g, false);
    const byGroup = new Map();
    for (const row of normal) {
      if (!byGroup.has(row.group)) byGroup.set(row.group, []);
      byGroup.get(row.group).push(row);
    }
    for (const [group, rows] of byGroup) {
      out += `${h}# ${g.code} 指令：${group}\n\n`;
      out += mdTable(['ID', '助记名', '参数', '说明', '文档化', '来源'], rows.map(r => [r.id, r.name, r.args, r.desc, r.documented, r.origin]));
      out += '\n\n';
    }
    const timeline = instructionRows(g, true);
    if (timeline.length) {
      out += `${h}# ${g.code} 时间轴指令\n\n`;
      out += mdTable(['ID', '助记名', '参数', '说明', '文档化', '来源'], timeline.map(r => [r.id, r.name, r.args, r.desc, r.documented, r.origin]));
      out += '\n\n';
    }
  }
  if (g.vars) {
    const vars = variableRows(g);
    out += `${h}# ${g.code} 变量\n\n`;
    out += mdTable(['ID', '名称', '类型', '访问', '作用域', '说明', '文档化', '来源'], vars.map(v => [v.id, v.name, v.type, v.access, v.scope, v.desc, v.documented, v.origin]));
    out += '\n\n';
  }
  return out;
}

function splitFileName(g) {
  return `${String(g.code).toLowerCase().replace('.', '_')}-ecl.md`;
}

function splitIndexSection() {
  let out = '## 分游戏文档索引\n\n';
  out += mdTable(['游戏', '作品', '独立文档', '包含内容'], gameInfo.map(g => [g.code, g.title, `${splitOutputDir}/${splitFileName(g)}`, '对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量']));
  out += '\n\n';
  return out;
}

function buildMainDocument() {
  let out = '# ECL 分游戏速查表\n\n';
  out += headerText();
  out += sourceIndexSection();
  out += splitIndexSection();
  out += gameOverviewSection();
  out += thbwikiGenerationSection(thbwikiFiles);
  out += flagsSection();
  for (const g of gameInfo) out += gameSection(g, 2);
  return out;
}

function buildGameDocument(g) {
  let out = `# ${g.code} ${g.title} ECL 速查\n\n`;
  out += headerText();
  out += `- 返回总表：\`../ecl-reference-by-game.md\`\n`;
  out += `- 本文包含：${g.code} 对应世代 THBWiki 中文代码表、全局 flags/常量、该游戏 Priw8 指令/变量主表。\n\n`;
  out += '## 本游戏概览\n\n';
  out += mdTable(['游戏', '作品', '代际/体系', '指令表覆盖', '变量表覆盖', '摘要'], [[g.code, g.title, g.generation, g.ins ? '有' : '未列', g.vars ? '有' : '未列', `${instructionSummary(g)} ${variableSummary(g)}`]]);
  out += '\n\n';
  out += thbwikiGenerationSection(thbwikiGenerationEntriesForGame(g));
  out += flagsSection();
  out += gameSection(g, 2);
  return out;
}

const md = buildMainDocument();
fs.writeFileSync('th062/ecl-reference-by-game.md', md);
fs.rmSync(splitOutputDir, { recursive: true, force: true });
fs.mkdirSync(splitOutputDir, { recursive: true });
let index = '# ECL 分游戏文档索引\n\n';
index += splitIndexSection();
index += gameOverviewSection();
fs.writeFileSync(`${splitOutputDir}/README.md`, index);
for (const g of gameInfo) {
  fs.writeFileSync(`${splitOutputDir}/${splitFileName(g)}`, buildGameDocument(g));
}
console.log(`Wrote th062/ecl-reference-by-game.md (${md.split('\n').length} lines)`);
console.log(`Wrote ${gameInfo.length} split game documents to ${splitOutputDir}`);
