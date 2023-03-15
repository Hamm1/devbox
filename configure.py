
import os
import subprocess
import time
import sys
import platform

def main():
  from pathlib import Path
  home = str(Path.home())
  if platform.system() == "Linux" and os.name == "posix":
    print("Linux")
    linux(home)
  if platform.system() == "Windows" and os.name == "nt":
    print("Windows")
    windows(home)
  if platform.system() == "Darwin" and os.name == "posix":
    print("MacOS")
    macos(home)

def macos(home):
  if os.name == "posix":
    if not os.path.exists("/opt/homebrew/bin/brew"):
      print("Homebrew is not installed...")
      command = f'/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"'
      proc = subprocess.Popen(command, shell=True, stdout=True)
      (output, err) = proc.communicate()
      returncode_brew = proc.wait()
      print(f"returncode_brew : {returncode_brew}")

    if not os.path.exists("/opt/homebrew/bin/node"):
      print("NodeJS is not installed...")
      subprocess.call(["brew", "install", "node"])
    else:
      if not os.path.exists("./node_modules"):
        print('NPM modules are not installed...')
        subprocess.call(["npm", "install"])

    if not os.path.exists("/opt/homebrew/bin/rustc"):
      print("Rust is not installed...")
      subprocess.call(["brew", "install", "rust"])
    else:
      if not os.path.exists(home + "/.cargo/bin/cargo-tauri"):
        print('Tauri is not installed...')
        subprocess.call(["cargo", "install", "tauri-cli"])

def windows(home):
  if os.name == "nt":
    if not os.path.exists(home + "\\.cargo\\bin\\rustc.exe"):
      print("Rust is not installed...")
      if not os.path.exists("C:\\ProgramData\\chocolatey\\bin\\choco.exe"):
        os.system("powershell Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol \
                  = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;\
                  iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))")
      if os.path.exists("C:\\ProgramData\\chocolatey\\bin\\choco.exe"):
        os.system("C:\\ProgramData\\chocolatey\\bin\\choco.exe install visualstudio2022-workload-vctools -y")
        os.system("C:\\ProgramData\\chocolatey\\bin\\choco.exe install rustup.install -y")

    if os.path.exists(home + "\\.cargo\\bin\\rustc.exe"):
      if not os.path.exists(home + "\\.cargo\\bin\\cargo-tauri.exe"):
        print("Tauri is not installed...")
        subprocess.call([home + "\\.cargo\\bin\\cargo.exe", "install", "tauri-cli"])

    if not os.path.exists("C:\\Program Files\\nodejs\\node.exe"):
      print("Node.js is not installed...")
      if not os.path.exists("C:\\ProgramData\\chocolatey\\bin\\choco.exe"):
        os.system("powershell Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol \
                  = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;\
                  iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))")
      if os.path.exists("C:\\ProgramData\\chocolatey\\bin\\choco.exe"):
        os.system("C:\\ProgramData\\chocolatey\\bin\\choco.exe install nodejs -y")
        os.environ['PATH'] += os.pathsep + 'C:/Program Files/nodejs/'

    if not os.path.exists(home + ".\\AppData\\Roaming\\npm\\astro.cmd"):
      print("Astro not installed...")
      subprocess.call(["C:\\Program Files\\nodejs\\npm.cmd", "install", "astro", "-g"])


def linux(home):
  if os.name == "posix":
    if os.path.exists("/etc/lsb-release"):
      f = open("/etc/lsb-release")
      read = f.read()
    else:
      read = ""
    if "DISTRIB_ID=Ubuntu" in read:
      print("Ubuntu")
      import apt #type: ignore
      try:
        import requests #type: ignore
      except ImportError:
        os.system('sudo apt-get install python3-requests')
        import requests #type: ignore
        
      subprocess.call(["sudo", "apt", "update"])
      subprocess.call(["sudo", "apt", "upgrade", "-y"])
      needed_packages = ["curl", "wget", "zsh", "git", "ansible-core", "software-properties-common", \
                         "apt-transport-https", "ca-certificates", "lsb-release"]
      cache = apt.Cache()
      for package in needed_packages:
        if not cache[package].is_installed:
          cache[package].mark_install()

      if cache.install_count > 0:
        try:
          print("Installing missing APT Build packages")
          cache.commit()
        except Exception as arg:
          print("Sorry, package installation failed [{err}]".format(err=str(arg)))

      if not os.path.exists("/usr/bin/node") and not os.path.exists("/usr/bin/npm"):
        print('Node is not installed...')
        request = requests.get('https://deb.nodesource.com/setup_19.x')
        subprocess.call([request.content], shell=True)
        cache = apt.Cache()
        cache['nodejs'].mark_install()
        cache.commit()

      if not os.path.exists("/usr/bin/code"):
        print('VSCode is not installed...')
        command = f'/bin/bash -c "$(wget -O- https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor | sudo tee /usr/share/keyrings/vscode.gpg)"'
        proc = subprocess.Popen(command, shell=True, stdout=True)
        (output, err) = proc.communicate()
        command2 = f'/bin/bash -c "$(echo deb [arch=amd64 signed-by=/usr/share/keyrings/vscode.gpg] https://packages.microsoft.com/repos/vscode stable main | sudo tee /etc/apt/sources.list.d/vscode.list)"'
        proc = subprocess.Popen(command, shell=True, stdout=True)
        (output, err) = proc.communicate()
        subprocess.call(["sudo", "apt", "update"])
        subprocess.call(["sudo", "apt", "install", "code", "-y"])

      if not os.path.exists("/usr/local/bin/starship"):
        command = f'/bin/bash -c "$(curl https://starship.rs/install.sh --output /tmp/starship.sh)"'
        proc = subprocess.Popen(command, shell=True, stdout=True)
        (output, err) = proc.communicate()
        subprocess.call(['chmod', '+x', '/tmp/starship.sh'])
        subprocess.run(['sh', '/tmp/starship.sh', '-y'], shell=False)
        subprocess.run(['sudo', 'rm', '/tmp/starship.sh'])
      
      if not os.path.exists('/usr/bin/docker'):
        print('Docker is not installed...')
        subprocess.call(['sudo', 'mkdir', '-m', '0755', '-p', '/etc/apt/keyrings'])
        command = f'/bin/bash -c "$(curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg)"'
        proc = subprocess.Popen(command, shell=True, stdout=True)
        (output, err) = proc.communicate()
        command = f'/bin/bash -c "$(echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null)"'
        proc = subprocess.Popen(command, shell=True, stdout=True)
        (output, err) = proc.communicate()
        subprocess.run(['sudo', 'apt', 'update'])
        needed_packages = ["docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin", "docker-compose-plugin"]
        cache = apt.Cache()
        for package in needed_packages:
          if not cache[package].is_installed:
            cache[package].mark_install()

        if cache.install_count > 0:
          try:
            print("Installing missing APT Build packages")
            cache.commit()
          except Exception as arg:
            print("Sorry, package installation failed [{err}]".format(err=str(arg)))

      if not os.path.exists(home + "/.deno/bin/deno"):
        if os.geteuid() == 0:
          exit("You can't run Deno installation with sudo")
        else:
            request = requests.get('https://deno.land/x/install/install.sh')
            subprocess.call([request.content], shell=True)
            
      if not os.path.exists(home + "/.bun/bin/bun"):
        if os.geteuid() == 0:
          exit("You can't run Bun installation with sudo")
        else:
            command = f'/bin/bash -c "$(curl -fsSL https://bun.sh/install | bash)"'
            proc = subprocess.Popen(command, shell=True, stdout=True)
            (output, err) = proc.communicate()

      if not os.path.exists(home + "/.zshrc"):
        if os.geteuid() == 0:
          exit("You can't run zshrc with sudo")
        else:
            request = requests.get('https://raw.githubusercontent.com/Hamm1/devbox/main/zshrc')
            f = open(home + "/.zshrc", "w")
            f.write(request.text)
            f.close()
            command = f'/bin/bash -c "$(chsh -s `which zsh`)"'
            proc = subprocess.Popen(command, shell=True, stdout=True)
            (output, err) = proc.communicate()
        
      if not os.path.exists(home + "/.cargo/bin/rustc") and not os.path.exists("/usr/bin/rustc"):
        print('Rust is not installed...')
        if os.geteuid() == 0:
          exit("You can't run Rust installation with sudo")
        else:
          request = requests.get('https://sh.rustup.rs')
          f = open("./rust.sh", "w")
          f.write(request.text)
          f.close()
          subprocess.call(["chmod", "+x", "./rust.sh"])
          subprocess.call(["sh","./rust.sh","-y"])
          subprocess.call(["sh","rm","./rust.sh"])
          #subprocess.call([request.content], shell=True)
          #command = f'/bin/bash -c "$(curl https://sh.rustup.rs --output ./rust.sh;chmod +x ./rust.sh;./rust.sh -y;rm ./rust.sh)"'
          #proc = subprocess.Popen(command, shell=True, stdout=True)
          #(output, err) = proc.communicate()
          # subprocess.call(["sh", "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"])

    if 'DISTRIB_ID="Arch"' in read or os.path.exists('/etc/pacman.conf'):
      print("Arch")
      needed_packages = ["webkit2gtk", "curl", "wget" ,"openssl", "appmenu-gtk-module", "gtk3", "libappindicator-gtk3", "librsvg", "libvips", "nodejs", "rust", "rust-src", "docker"]
      # needed_packages.append("base-devel")
      subprocess.call(["pacman", "-Syy"])
      for package in needed_packages:
        check = subprocess.call(["pacman", "-Qe", package])
        if check != 0:
          subprocess.call(["sudo","pacman", "-S", "--needed", package, "--noconfirm"])

    if os.path.exists("/etc/fedora-release"):
      print("Fedora")
      import dnf #type: ignore
      import rpm #type: ignore
      try:
          import requests #type: ignore
      except ImportError:
          os.system('sudo apt-get install python3-requests')
      import requests #type: ignore
      ts = rpm.TransactionSet()
      needed_packages = ["webkit2gtk3-devel.x86_64", "openssl-devel", "curl", "wget", "libappindicator-gtk3", "librsvg2-devel","rust","nodejs"]
      missing_packages = []
      for package in needed_packages:
          mi = ts.dbMatch( 'name', package )

          rpmhit=0
          for h in mi:
              if h['name'] == package:
                  rpmhit=1
                  break

          if rpmhit == 0:
              print('Error: Package lsof not installed.')
              missing_packages.append(package)
      for missing in missing_packages:
          print("Installing " + missing)
          subprocess.call(["sudo","dnf","install",missing,"-y"])
  
if __name__ == "__main__":
  main()
