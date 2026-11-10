import argparse
import concurrent.futures
import hashlib
import io
import json
import tarfile
import urllib.request
from pathlib import Path



def inspect(entry):
    project, image = entry
    name, tag = image.removeprefix('ghcr.io/').split(':')
    target = ROOT / project
    target.mkdir(exist_ok=True)
    token = json.load(urllib.request.urlopen('https://ghcr.io/token?service=ghcr.io&scope=repository:' + name + ':pull'))['token']

    def fetch(kind, ref):
        req = urllib.request.Request('https://ghcr.io/v2/' + name + '/' + kind + '/' + ref, headers={
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/vnd.oci.image.index.v1+json, application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json',
        })
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
        if ref.startswith('sha256:'):
            assert hashlib.sha256(data).hexdigest() == ref.split(':')[1]
        return data

    index_bytes = fetch('manifests', tag)
    index = json.loads(index_bytes)
    digest = 'sha256:' + hashlib.sha256(index_bytes).hexdigest()
    if 'manifests' in index:
        digest = next(x['digest'] for x in index['manifests'] if x.get('platform') == {'architecture': 'amd64', 'os': 'linux'})
        manifest = json.loads(fetch('manifests', digest))
    else:
        manifest = index
    config = json.loads(fetch('blobs', manifest['config']['digest']))
    layers = iter(manifest['layers'])
    layer_info = []
    for h in config['history']:
        if h.get('empty_layer'):
            continue
        layer = next(layers)
        command = h.get('created_by', '')
        layer_info.append(dict(layer, command=command))
        # Read only small source/metadata layers, never ML runtimes or datasets.
        if layer['size'] > 25_000_000 or not any(x in command for x in ('COPY task.md', 'COPY evaluation.md', 'COPY entrypoint.sh', 'COPY download_data.py', 'COPY reproduction/runs/', 'COPY repo/', 'COPY AGENTS.md')):
            continue
        raw = fetch('blobs', layer['digest'])
        with tarfile.open(fileobj=io.BytesIO(raw), mode='r:*') as archive:
            for member in archive:
                if not member.isfile() or member.size > 2_000_000:
                    continue
                p = Path(member.name)
                if p.is_absolute() or '..' in p.parts:
                    raise ValueError(member.name)
                if p.suffix not in {'.md', '.py', '.sh', '.json', '.yaml', '.yml', '.txt'}:
                    continue
                dest = target / p
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(archive.extractfile(member).read())
    metadata = dict(project=project, source_image=image, pinned_image='ghcr.io/' + name + '@' + digest,
                    config=config['config'], layers=layer_info)
    (target / 'image.json').write_text(json.dumps(metadata, indent=2) + '\n')
    return project, len(list(target.rglob('*'))), sum(x['size'] for x in manifest['layers'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inspect GHCR metadata and small source layers; no datasets or ML runtime layers')
    parser.add_argument('--upstream', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    ROOT = args.output.resolve()
    ROOT.mkdir(parents=True, exist_ok=True)
    SOURCE = args.upstream / 'agent4sci/registry.yaml'
    entries = []
    for line in SOURCE.read_text().splitlines():
        if line and not line.startswith((' ', '#')):
            project = line[:-1]
        elif line.startswith('  image: '):
            entries.append((project, line.split('  image: ')[1]))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for row in pool.map(inspect, entries):
            print(*row, flush=True)
