const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=new TextDecoder('utf-8',{fatal:true}).decode(fs.readFileSync(require('node:path').join(__dirname,'ARCHITEKTONICA-brief-v9.html')));
assert.ok(!html.includes('\uFFFD'));
assert.ok(!/[^\x00-\x7F]/.test(html),'Transport is strictly ASCII');
const dataText=html.match(/<script type="application\/json" id="brief-data">([\s\S]*?)<\/script>/)[1];
const code=html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
const data=JSON.parse(dataText).flatMap(g=>g.services), handlers={};
assert.equal(JSON.parse(dataText)[4].desc,'Видео, анимация, визуализация, виртуальные пространства и звук');
assert.ok(!JSON.stringify(JSON.parse(dataText)).includes('\uFFFD'));
const node={focus(){},scrollIntoView(){},setAttribute(){},classList:{remove(){}},hidden:false,innerHTML:'',textContent:'',disabled:false};
const app={innerHTML:'',addEventListener(k,f){handlers[k]=f},querySelector(){return node}};
const document={getElementById(k){return k==='brief-data'?{textContent:dataText}:k==='arch4'?app:node}};
const store=new Map(),sessionStorage={getItem(k){return store.get(k)||null},setItem(k,v){store.set(k,v)},removeItem(k){store.delete(k)}};
vm.runInNewContext(code,{document,sessionStorage,console});
function click(d){handlers.click({target:{closest(selector){return selector==='button'?{dataset:d,disabled:false}:null}}})}
function change(id,dataset,value){handlers.change({target:{id,dataset,value,checked:true}})}
function input(id,dataset,value){handlers.input({target:{id,dataset,value}})}
function select(i,o){change('fake',{q:String(i),option:o},'')}
function has(s){assert.ok(app.innerHTML.includes(s),s)}
function checked(i,o){return [...app.innerHTML.matchAll(/<input[^>]+data-q="(\d+)" data-option="([^"]*)"([^>]*)>/g)].some(m=>m[1]===String(i)&&m[2]===o&&m[3].includes('checked'))}
assert.equal(data.length,84);
has('Видео, анимация, визуализация, виртуальные пространства и звук');
assert.equal(data.find(s=>s.id==='043').name,'Разработка и внедрение AI-системы');
assert.equal(data.find(s=>s.id==='074').name,'Бизнес-отчёты и панели показателей');
for(const s of data){click({id:s.id});click({act:'start'});has(`<h2>${s.name}</h2>`);for(const q of s.questions.filter(q=>!q.condition&&q.opts.length)){has(`type="${q.multi?'checkbox':'radio'}" name="question-${q.i}"`)}click({act:'prevbrief'});click({id:s.id})}
click({id:'004'});click({id:'016'});click({act:'start'});select(0,'Привлечение клиентов');select(0,'Увеличение продаж');select(0,'Выход на новый рынок');assert.ok(checked(0,'Привлечение клиентов')&&checked(0,'Увеличение продаж')&&checked(0,'Выход на новый рынок'));
select(0,'Пока не знаю');assert.ok(checked(0,'Пока не знаю'));assert.ok(!checked(0,'Привлечение клиентов'));
select(0,'Привлечение клиентов');select(0,'Увеличение продаж');select(0,'Свой вариант');input('txt-0',{text:'0'},'Новый сегмент');select(2,'Поисковая реклама');select(2,'Пока ничего');assert.ok(checked(2,'Пока ничего'));assert.ok(!checked(2,'Поисковая реклама'));
select(0,'Пока не знаю');assert.ok(!app.innerHTML.includes('Новый сегмент'));select(0,'Свой вариант');has('Новый сегмент');select(0,'Свой вариант');assert.ok(!app.innerHTML.includes('Новый сегмент'));select(0,'Свой вариант');has('Новый сегмент');select(0,'Привлечение клиентов');select(0,'Увеличение продаж');select(2,'Свой вариант');input('txt-2',{text:'2'},'Неактивный свой вариант');select(2,'Пока ничего');
click({act:'nextbrief'});select(0,'Одностраничный сайт');select(0,'Сайт-каталог');select(1,'Обновить существующий сайт');has('id="txt-2"');input('txt-2',{text:'2'},'Скрытый ответ');select(1,'Создать с нуля');assert.ok(checked(1,'Создать с нуля')&&checked(1,'Обновить существующий сайт'));has('id="txt-2"');select(1,'Обновить существующий сайт');assert.ok(!app.innerHTML.includes('id="txt-2"'));
click({act:'nextbrief'});has('Давайте познакомимся');assert.ok(!app.innerHTML.includes('бюджет'));has('.heic');has('.pptx');has('.zip');has('.xls');has('.pages');has('id="privacy-policy"');handlers.change({target:{id:'files',dataset:{},files:[{name:'brief.pdf'},{name:'brief.pdf'}]}});assert.equal((app.innerHTML.match(/brief\.pdf/g)||[]).length,2);click({removeFile:'0'});assert.equal((app.innerHTML.match(/brief\.pdf/g)||[]).length,1);input('fullname',{contact:'name'},'Тестовый Клиент');click({method:'Email'});input('contactvalue',{contact:'value'},'bad');click({act:'review'});assert.match(node.textContent,/электронной почты/);input('contactvalue',{contact:'value'},'test@example.com');click({act:'review'});has('Привлечение клиентов; Увеличение продаж; Новый сегмент');assert.ok(!app.innerHTML.includes('Скрытый ответ'));assert.ok(!app.innerHTML.includes('Неактивный свой вариант'));has('id="consent-document"');has('data-legal="privacy-policy"');has('id="send" disabled');assert.ok(!app.innerHTML.includes('бюджет'));change('consent',{},'');click({act:'send'});has('Данные не отправлены');click({act:'reset'});click({act:'other'});click({act:'start'});has('Помогите подобрать решение');
for(const [query,id] of [['разработку сайтов','016'],['сайтом','016'],['нейросети','046'],['квизы','020'],['воронки','057'],['чат-боты','046'],['CRM','057'],['мне нужна разработка сайта','016']]){input('search',{},query);assert.ok(node.innerHTML.includes(`data-id="${id}"`),query);console.log('Search OK:',query)}
for(const s of data){input('search',{},s.name);assert.ok(node.innerHTML.includes(`data-id="${s.id}"`),s.name)}
for(const [query,id] of [['сайт под ключ','016'],['логотип для компании','002'],['хочу разработку сайта под ключ','016'],['пожалуйста помогите нам сделать логотип для компании','002']]){input('search',{},query);assert.equal(node.innerHTML.match(/data-id="(\d+)"/)[1],id,query);console.log('Ranked search OK:',query)}
input('search',{},'сайт с чат-ботом');assert.ok(node.innerHTML.includes('data-id="016"'));assert.ok(node.innerHTML.includes('data-id="046"'));
for(const query of ['чат с ботом','чат со ботом','чат-боты','чат боту','какой чат с ботом','что такое чат-бот']){input('search',{},query);assert.ok(node.innerHTML.includes('data-id="046"'),query)}
for(const [query,id] of [['какую разработку сайта','016'],['какая разработка логотипа','002']]){input('search',{},query);assert.equal(node.innerHTML.match(/data-id="(\d+)"/)[1],id,query)}
input('search',{},'сайт qwerty zzzzz');assert.ok(node.innerHTML.includes('data-id="016"'));console.log('Multi-service and fallback search OK');
const count=vm.runInNewContext(code.match(/function serviceCount\(n\)\{[^\n]+\}/)[0]+'; serviceCount');for(const [n,expected] of [[0,'0 услуг'],[1,'1 услуга'],[2,'2 услуги'],[5,'5 услуг'],[11,'11 услуг'],[14,'14 услуг'],[21,'21 услуга'],[81,'81 услуга'],[84,'84 услуги'],[85,'85 услуг']])assert.equal(count(n),expected);
input('search',{},'zzzzzz');assert.match(node.innerHTML,/Ничего не найдено/);
// v6 regressions: use the generic brief to exercise open answers, empty review and consent.
click({act:'prevbrief'});click({act:'start'});input('txt-0',{text:'0'},'Сохранённый ответ');click({unknown:'0'});has('Сохранённый ответ');has('data-unknown="0" aria-pressed="true"');click({unknown:'0'});has('data-unknown="0" aria-pressed="false"');has('Сохранённый ответ');
click({unknown:'0'});input('txt-0',{text:'0'},'Обновлённый ответ');click({act:'nextbrief'});input('fullname',{contact:'name'},'Тестовый Клиент');input('contactvalue',{contact:'value'},'test@example.com');click({act:'review'});assert.match(node.textContent,/Telegram/);input('contactvalue',{contact:'value'},'@кириллица');click({act:'review'});assert.match(node.textContent,/Telegram/);input('contactvalue',{contact:'value'},'@test_user');click({act:'review'});has('Обновлённый ответ');has('id="send" disabled');
change('consent',{},'');click({act:'editproject'});input('note',{project:'note'},'Изменили комментарий');click({act:'review'});has('id="consent" checked');click({edit:'0'});input('txt-0',{text:'0'},'Изменили бриф');click({act:'nextbrief'});has('id="consent" checked');
click({act:'editproject'});input('fullname',{contact:'name'},'Другой Клиент');click({act:'review'});has('id="send" disabled');change('consent',{},'');click({act:'editproject'});click({method:'MAX'});input('contactvalue',{contact:'value'},'test@example.com');click({act:'review'});assert.match(node.textContent,/MAX/);input('contactvalue',{contact:'value'},'+7 900 000 00 00');click({act:'review'});has('id="send" disabled');
change('consent',{},'');click({act:'send'});has('Данные не отправлены');click({act:'reset'});click({act:'other'});click({act:'start'});click({unknown:'0'});click({act:'nextbrief'});input('fullname',{contact:'name'},'Тестовый Клиент');input('contactvalue',{contact:'value'},'https://t.me/test_user');click({act:'review'});assert.match(node.textContent,/мини-брифа/);input('business',{project:'business'},'Нужна консультация');click({act:'review'});has('Проверьте обращение');has('Пока не знаю');
assert.match(html,/<meta name="description"/);assert.match(html,/<meta property="og:title"/);assert.match(html,/<meta name="robots" content="noindex, nofollow"/);assert.match(html,/RELEASE CHECKLIST/);assert.match(html,/maxlength="3000"/);
console.log('PASS: 84 brief renders; field modes; multi/exclusive/custom; dependencies; validation; review; simulated send and fallback. Node DOM stub, not real browser.');
