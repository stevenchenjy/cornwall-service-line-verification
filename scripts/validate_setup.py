from pathlib import Path
import subprocess
import tomllib

root = Path(__file__).resolve().parents[1]
required = ['README.md', 'START_HERE.md', 'AGENTS.md', 'research/brief.md', 'research/analysis-plan.md', 'research/TASKS.md', 'research/STATUS.md', 'research/source-register.csv', 'research/claim-register.csv', 'research/questions-for-water-department.md', 'uv.lock']
for name in required:
    assert (root / name).is_file(), f'Missing: {name}'
config = tomllib.loads((root / '.codex/config.toml').read_text())
assert config['agents']['max_concurrent_threads_per_session'] <= 3
names = []
for path in sorted((root / '.codex/agents').glob('*.toml')):
    agent = tomllib.loads(path.read_text())
    assert all(agent.get(k) for k in ['name', 'description', 'developer_instructions']), path
    assert 'model' not in agent and 'sandbox_mode' not in agent and 'approval_policy' not in agent, path
    names.append(agent['name'])
assert len(names) == 5 and len(set(names)) == 5
tracked = subprocess.run(['git', 'ls-files', '-z'], cwd=root, capture_output=True, check=True).stdout.decode().split('\0')
local_roots = ('data/raw/', 'data/interim/', 'data/processed/', 'data/restricted/')
leaked = [p for p in tracked if p.startswith(local_roots) and not p.endswith('/.gitkeep')]
assert not leaked, f'Local-only data tracked: {leaked}'
print('Setup structure and 5 custom-agent files validated; local-only data absent from Git index.')
