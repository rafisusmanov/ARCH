import sys,json,pathlib,base64,gzip,hashlib
source,run,destination=sys.argv[1:4]
p=json.loads(pathlib.Path(source).read_text());out=pathlib.Path(destination);out.mkdir(parents=True,exist_ok=True)
def decode(x):
 b=gzip.decompress(base64.b64decode(x['gzip_base64']));assert hashlib.sha256(b).hexdigest()==x['sha256'];return b
(out/'bundle.txt').write_bytes(decode(p['bundles'][p['run_bundles'][run]]))
for name,x in p['extra_documents'].items():
 target=out/'extra'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(decode(x))
print('Decoded and verified',run)
