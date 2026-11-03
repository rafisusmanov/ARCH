import sys,pathlib,json,hashlib,datetime
ROOT=pathlib.Path(__file__).resolve().parent
reader,op=sys.argv[1:3];folder=ROOT/'reviews'/reader
facts=(folder/'facts.txt').read_text();chunks=[facts[i:i+12000] for i in range(0,len(facts),12000)]
if op=='info':out=json.dumps({'fact_chunks':len(chunks),'items':json.loads((folder/'items.json').read_text())},ensure_ascii=False,indent=2)
elif op=='facts':out=chunks[int(sys.argv[3])]
elif op=='item':out=(folder/(sys.argv[3]+'.json')).read_text()
else:raise ValueError(op)
with (folder/'actions.jsonl').open('a') as f:f.write(json.dumps({'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operation':op,'argument':sys.argv[3] if len(sys.argv)>3 else None,'output_sha256':hashlib.sha256(out.encode()).hexdigest(),'characters':len(out)})+'\n')
print(out,end='')
