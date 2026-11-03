import pathlib,json,hashlib,statistics,collections
ROOT=pathlib.Path(__file__).resolve().parent
CRITERIA=['Позиционирование','Профессиональная конкретика','Сила авторской мысли','Качество языка','Заголовки','Композиция','Убедительность','Фактологическая точность','Пригодность к публикации']
mapping=json.loads((ROOT/'evidence/blind-map.json').read_text());expected={r['id'] for r in json.loads((ROOT/'runs.json').read_text())}
rows=[];issues=[];seals={};resolved=[];original_issues=[]
for reader in ['editor_ace','editor_bdfg']:
 p=ROOT/'reviews'/reader;raw=(p/'review.json').read_bytes();seals[reader]=hashlib.sha256(raw).hexdigest();review=json.loads(raw)
 assigned={x['id'] for x in json.loads((p/'items.json').read_text())}
 addenda=json.loads((p/'addendum.json').read_text()).get('corrections',[]) if (p/'addendum.json').exists() else []
 if {x['id'] for x in review['items']}!=assigned:issues.append({'reader':reader,'issue':'assignment mismatch'})
 for item in review['items']:
  rid=mapping[item['id']];run=ROOT/'runs'/rid;text=(run/'response.md').read_text();f=run/'followup-response.md'
  if f.exists():text+='\n'+f.read_text()
  if {x['name'] for x in item['criteria']}!=set(CRITERIA) or len(item['criteria'])!=9:issues.append({'run':rid,'issue':'criteria mismatch'})
  for c in item['criteria']:
   if not isinstance(c['score'],(int,float)) or not 0<=c['score']<=5:issues.append({'run':rid,'issue':'score out of bounds','criterion':c['name']})
   if not c['quote'] or c['quote'] not in text:
    problem={'run':rid,'issue':'quote not verbatim','criterion':c['name'],'quote':c['quote']};original_issues.append(problem)
    fixes=[a for a in addenda if a['id']==item['id'] and a['criterion']==c['name'] and a.get('field')=='quote' and a.get('corrected_quote') in text]
    if len(fixes)==1:resolved.append({**problem,'editor_addendum':str(p/'addendum.json'),'corrected_quote':fixes[0]['corrected_quote'],'score_unchanged':True})
    else:issues.append(problem)
  for c in item['critical_errors']:
   if c.get('quote') and c['quote'] not in text:issues.append({'run':rid,'issue':'critical quote not verbatim'})
  version,scenario,repeat=rid.split('-')
  rows.append({'run_id':rid,'blind_id':item['id'],'reviewer':reader,'version':version,'scenario':scenario,'repeat':int(repeat),'status':item['status'],'mean':statistics.mean(x['score'] for x in item['criteria']),'scores':{x['name']:x['score'] for x in item['criteria']},'critical_errors':item['critical_errors'],'editorial_verdict':item['editorial_verdict']})
if {x['run_id'] for x in rows}!=expected or len(rows)!=len(expected):issues.append({'issue':'not exactly 20 assigned runs'})
validation={'review_sha256':seals,'reviews':len(seals),'texts':len(rows),'criteria_checked':sum(9 for _ in rows),'original_issues':original_issues,'resolved_by_editor_addenda':resolved,'issues':issues,'pass':not issues}
(ROOT/'evidence/review-validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
summary={'runs':sorted(rows,key=lambda r:r['run_id']),'scenarios':{},'paired_equal_scenario_mean_A_to_E':{}}
for scenario in 'ABCDEFG':
 groups={v:[x for x in rows if x['scenario']==scenario and x['version']==v] for v in ['baseline','candidate']}
 result={}
 for version,items in groups.items():
  result[version]={'runs':len(items),'mean':statistics.mean(x['mean'] for x in items),'mean_range':[min(x['mean'] for x in items),max(x['mean'] for x in items)],'scores':{k:statistics.mean(x['scores'][k] for x in items) for k in CRITERIA},'statuses':dict(collections.Counter(x['status'] for x in items)),'critical_errors':sum(len(x['critical_errors']) for x in items)}
 result['delta']=result['candidate']['mean']-result['baseline']['mean'];result['score_deltas']={k:result['candidate']['scores'][k]-result['baseline']['scores'][k] for k in CRITERIA}
 summary['scenarios'][scenario]=result
for version in ['baseline','candidate']:
 summary['paired_equal_scenario_mean_A_to_E'][version]=statistics.mean(summary['scenarios'][s][version]['mean'] for s in 'ABCDE')
summary['paired_equal_scenario_mean_A_to_E']['delta']=summary['paired_equal_scenario_mean_A_to_E']['candidate']-summary['paired_equal_scenario_mean_A_to_E']['baseline']
(ROOT/'evidence/comparison-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'validation':validation,'scenario_means':{s:{'baseline':x['baseline']['mean'],'candidate':x['candidate']['mean'],'delta':x['delta']} for s,x in summary['scenarios'].items()},'A_to_E':summary['paired_equal_scenario_mean_A_to_E']},ensure_ascii=False,indent=2))
