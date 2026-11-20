import fs from 'node:fs';
import assert from 'node:assert/strict';
import vm from 'node:vm';

function cleanUtf8(bytes, label){
  const value=new TextDecoder('utf-8',{fatal:true}).decode(bytes);
  assert.ok(!value.includes('\uFFFD'),`U+FFFD replacement character in ${label}`);
  return value;
}
const readUtf8=path=>cleanUtf8(fs.readFileSync(path),path);
readUtf8(new URL(import.meta.url));

const descriptions = [
  'Сайты, магазины, приложения и цифровые сервисы',
  'Название, логотип, визуальный образ',
  'Продвижение, заявки, репутация и работа с клиентами',
  'Помощники, автоматизация, системы и безопасность',
  'Видео, анимация, визуализация, виртуальные пространства и звук',
  'Финансы, бухгалтерия, сотрудники, данные и операционные процессы',
];
const base = new URL('../',import.meta.url);
const lines = readUtf8(new URL('contact-briefs.tsv',base)).split(/\r?\n/);
const groups = [];
for (const line of lines) {
  if (line.startsWith('# Group: ')) {
    const index = groups.length;
    groups.push({title:line.slice(9),desc:descriptions[index],index,services:[]});
  }
  if (!line || line.startsWith('#')) continue;
  const [id,name,desc,...fields] = line.split('|');
  const questions = fields.map((raw,i) => {
    let condition = null;
    if (raw.startsWith('?')) {
      const colon=raw.indexOf(':');
      const [n,v]=raw.slice(1,colon).split('=');
      condition={n:Number(n),v};raw=raw.slice(colon+1);
    }
    const multi=raw.startsWith('+');if(multi)raw=raw.slice(1);
    const [label,...options]=raw.split('~');
    return {i,label,multi,exclusive:options.filter(o=>o.startsWith('!')).map(o=>o.slice(1)),opts:options.map(o=>o.replace(/^!/,'')),condition};
  });
  groups.at(-1).services.push({id,name,desc,questions});
}
const data = groups.flatMap(g=>g.services);
// Question text lives in the authoritative UTF-8 TSV; these tags are search-only.
const svc=id=>data.find(s=>s.id===id);
const tag=(ids,tags)=>ids.forEach(id=>{svc(id).tags=[svc(id).tags||'',tags].join(' ').trim()});
tag(['020'],'квиз квизы квизов опросник интерактивный тест');
tag(['002'],'логотип компании фирменный знак');
tag(['056','057','059','060','061'],'воронка воронки воронок продаж');
tag(['046'],'чатбот чатботы чат бот боты ассистент');
tag(['039','040','041','042','043','044','045','046','047','052','053','054','060'],'нейросеть нейросети нейросетей искусственный интеллект ИИ AI');
const canon = JSON.parse(readUtf8(new URL('public-service-catalogue.json',base)));
assert.deepEqual(groups.map(g=>g.services.length),[12,4,19,18,16,15]);
assert.deepEqual(data.map(s=>'svc-'+s.id).sort(),canon.services.map(s=>s.id).sort());
const publicServices=new Map(canon.services.map(s=>[s.id,s]));
for(const s of data){
  const entry=publicServices.get('svc-'+s.id);
  assert.ok(entry.display_title,`Missing public title: ${entry.id}`);
  assert.equal(s.name,entry.display_title,`Brief label must match catalogue: ${entry.id}`);
  assert.ok(Array.isArray(entry.search_aliases),`Missing search aliases: ${entry.id}`);
  s.aliases=entry.search_aliases;
}
assert.equal(new Set(data.map(s=>s.id)).size,84);
assert.equal(data.reduce((n,s)=>n+s.questions.length,0),344);
assert.ok(data.every(s=>s.questions.length>=4&&s.questions.length<=6));
assert.ok(!data.some(s=>s.questions.some(q=>/бюджет/i.test(q.label))));
assert.equal(groups[4].title,'Видео, 3D и интерактивные проекты');
assert.equal(groups[4].desc,'Видео, анимация, визуализация, виртуальные пространства и звук');
const template = readUtf8(new URL('architektonica-brief-template.html',import.meta.url));
assert.equal(template.split('__EMBEDDED_BRIEF_DATA__').length,2);
const output=new URL('ARCHITEKTONICA-brief-v9.html',import.meta.url);
const sourceHtml=template.replace('__EMBEDDED_BRIEF_DATA__',JSON.stringify(groups,null,2).replace(/</g,'\\u003c'));
assert.ok(!sourceHtml.includes('\uFFFD'),'U+FFFD replacement character in generated HTML');
// ASCII-only deliverable: transport cannot split a multibyte Russian character.
// HTML text/attributes use numeric character references; script and JSON use JS Unicode escapes.
// Verify the actual decoded catalogue, not just the encoded bytes.
const escapeScript=s=>s.replace(/[^\x00-\x7F]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));
const escapeHtml=s=>s.replace(/[^\x00-\x7F]/gu,c=>'&#'+c.codePointAt(0)+';');
const html=sourceHtml.split(/(<script\b[^>]*>[\s\S]*?<\/script>)/gi).map((chunk,i)=>i%2?escapeScript(chunk):escapeHtml(chunk)).join('');
assert.ok(!/[^\x00-\x7F]/.test(html),'Transport artifact must be ASCII-only');
assert.deepEqual(JSON.parse(html.match(/<script type="application\/json" id="brief-data">([\s\S]*?)<\/script>/)[1]),groups);
new vm.Script(html.match(/<script>\s*([\s\S]*?)<\/script>/)[1]);
fs.writeFileSync(output,html,'utf8');
assert.equal(readUtf8(output),html,'Output must round-trip as strict UTF-8');
console.log(`Built ${data.length} briefs, ${data.reduce((n,s)=>n+s.questions.length,0)} service questions; 6 entry groups.`);
