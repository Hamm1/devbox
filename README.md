# 🦅SMDC Help Desk Development Environment Build Scripts🦅
```
Scripts and ansible playbooks that will completely build the development
environment for several operating systems.
```
- Windows
```
Run the windows_configure.ps1 script
```
- MacOS
```
Run python configure.py script
```
- Ubuntu/Debian
```
Run configure.py or ansible-playbook linux_setup.yaml.
Python script has to be ran twice, once with sudo, once
without.
```
- Arch
```
Run configure.py or ansible-playbook linux_setup.yaml.
Python script has to be ran twice, once with sudo, once
without.
```
- Fedora/Red hat
```
Run python configure.py script
Python script has to be ran twice, once with sudo, once
without.
```
- NixOS or Nix Package Manager
```
Run nix-shell in the directory containing shell.nix to
automatically set up environment.
```