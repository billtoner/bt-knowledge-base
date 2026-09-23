# ansible

Agentless configuration management and orchestration over SSH. Covers the whole family: `ansible` (ad-hoc), `ansible-playbook` (playbooks), `ansible-vault` (secrets), `ansible-inventory`, `ansible-galaxy`, `ansible-config`, `ansible-doc`.

**Tags:** iac

## Cool features

- **Agentless.** Only needs Python on the target and SSH access — no daemon to install.
- **Idempotent by design.** Re-running a playbook is safe; modules report `changed: false` when nothing needed doing.
- **`--check` is a dry run.** Plus `--diff` shows what *would* change, line by line.
- **`--start-at-task "<name>"`** resumes mid-playbook — invaluable when a long playbook fails near the end.
- **`--limit <pattern>`** restricts a run to a subset of inventory without editing inventory files.
- **`--step`** prompts before each task — like a debugger for playbooks.
- **Verbosity is layered.** Same flag (`-v`...`-vvvv`), env var, or config — pick whichever fits the moment.

## Verbosity (three ways to set it)

```bash
# CLI flags — each v adds a level
ansible-playbook site.yml                     # level 0: only changed/failed/recap
ansible-playbook site.yml -v                  # level 1: task results, loop items
ansible-playbook site.yml -vv                 # level 2: task input + output
ansible-playbook site.yml -vvv                # level 3: connection info (which SSH command)
ansible-playbook site.yml -vvvv               # level 4: SSH transport debugging (paramiko/ssh debug)

# Env var — handy for one run without touching CLI
ANSIBLE_VERBOSITY=3 ansible-playbook site.yml

# Persistent in ansible.cfg
# [defaults]
# verbosity = 2
```

**Suppressing output for sensitive tasks:** set `no_log: true` on the task — overrides any verbosity level.

```yaml
- name: register a license key
  command: /usr/local/bin/register {{ license_key }}
  no_log: true
```

## Ad-hoc commands (the `ansible` binary)

```bash
ansible all -m ping                                 # connectivity check
ansible web -m shell -a 'uptime'                    # run shell on the web group
ansible db -m service -a 'name=postgresql state=restarted' --become
ansible all -m setup                                # dump all facts (huge)
ansible all -m setup -a 'filter=ansible_distribution*'   # filtered facts
ansible all -a 'df -h' -o                           # -o = one line per host (compact)
```

## Playbooks (`ansible-playbook`)

```bash
ansible-playbook site.yml                                       # run everything
ansible-playbook site.yml --check --diff                        # dry run + show changes
ansible-playbook site.yml --limit web                           # subset of inventory
ansible-playbook site.yml --limit 'web:!web03'                  # group minus a host
ansible-playbook site.yml --tags "deploy,restart"               # only tagged tasks
ansible-playbook site.yml --skip-tags "slow"                    # skip tagged tasks
ansible-playbook site.yml --start-at-task "Configure nginx"     # resume from a task
ansible-playbook site.yml --step                                # prompt before each task
ansible-playbook site.yml --syntax-check                        # parse only, don't run
ansible-playbook site.yml --list-hosts                          # who would run
ansible-playbook site.yml --list-tasks                          # what would run
ansible-playbook site.yml -e "version=1.2.3 env=prod"           # extra vars
ansible-playbook site.yml -e "@vars/prod.yml"                   # extra vars from file
```

## Inventory

```bash
ansible-inventory --list                              # full inventory as JSON
ansible-inventory --graph                             # tree view of groups
ansible-inventory --host web01                        # vars for one host
ansible-playbook -i inventory/prod site.yml           # alternate inventory
ansible all --list-hosts                              # who matches "all"
```

## Vault (secrets at rest)

```bash
ansible-vault create   vars/secrets.yml
ansible-vault edit     vars/secrets.yml
ansible-vault view     vars/secrets.yml
ansible-vault encrypt  vars/secrets.yml
ansible-vault decrypt  vars/secrets.yml
ansible-vault rekey    vars/secrets.yml                          # change password
ansible-vault encrypt_string 'supersecret' --name 'db_password'  # single value inline
ansible-playbook site.yml --ask-vault-pass                       # prompt for password
ansible-playbook site.yml --vault-password-file ~/.vault_pass    # password from file
```

## Galaxy (roles & collections)

```bash
ansible-galaxy collection install community.general
ansible-galaxy role install geerlingguy.docker
ansible-galaxy install -r requirements.yml             # install everything in the file
ansible-galaxy collection list                          # what's installed
```

## Discoverability

```bash
ansible-doc -l                                         # list all modules
ansible-doc shell                                      # docs for the shell module
ansible-doc -t lookup file                             # docs for a non-module plugin type
ansible-config dump                                    # current config
ansible-config dump --only-changed                     # just non-default settings
```

## Killer flags (shared across the family)

- `-v` / `-vv` / `-vvv` / `-vvvv` — verbosity (also `ANSIBLE_VERBOSITY=N`)
- `--check` — dry run; `--diff` pairs with it to show line-level changes
- `--limit <pattern>` — restrict to inventory subset
- `--tags` / `--skip-tags` — selectively run tagged tasks
- `--start-at-task "<name>"` — resume from a specific task
- `--step` — interactive, task-by-task
- `-e "<vars>"` — extra vars (also `-e "@file.yml"`)
- `-i <inventory>` — use alternate inventory
- `--become` / `-K` — privilege escalation (`-K` prompts for sudo password)
- `--ask-vault-pass` / `--vault-password-file` — vault password sources
