
import os
import subprocess # nosec
import time
import sys
import platform
import shutil

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
      proc = subprocess.Popen(command, shell=True, stdout=True) # nosec
      (output, err) = proc.communicate()
      returncode_brew = proc.wait()
      print(f"returncode_brew : {returncode_brew}")
    
    check = ["/opt/homebrew/bin/node;node",
             "/opt/homebrew/bin/bun;bun",
             "/opt/homebrew/bin/deno;deno",
             "/opt/homebrew/bin/git;git",
             "/opt/homebrew/bin/code;code",
             "/usr/local/bin/docker;docker",
             "/opt/homebrew/bin/curl;curl",
             "/opt/homebrew/bin/tsc;typescript",
             "/opt/homebrew/bin/rustc;rust"]
    
    for c in check:
      if not os.path.exists(c.split(";")[0]):
        print(c.split(";")[0] + " is not installed...")
        if os.path.exists("/opt/homebrew/bin/brew"):
          os.system("/opt/homebrew/bin/brew install " + c.split(";")[1]) # nosec

    if not os.path.exists(home + "/.cargo/bin/cargo-tauri") and os.path.exists("/opt/homebrew/bin/rustc"):
      print('Tauri is not installed...')
      subprocess.call(["cargo", "install", "tauri-cli"], shell=False) # nosec

def windows(home):
  if os.name == "nt":
    if not os.path.exists("C:\\ProgramData\\chocolatey\\bin\\choco.exe"):
        os.system("powershell Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol \
                  = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;\
                  iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))") # nosec
    
    if not os.path.exists(home + "\\.cargo\\bin\\rustc.exe"):
      print("Rust is not installed...")
      if os.path.exists("C:\\ProgramData\\chocolatey\\bin\\choco.exe"):
        os.system("C:\\ProgramData\\chocolatey\\bin\\choco.exe install visualstudio2022-workload-vctools -y") # nosec
        os.system("C:\\ProgramData\\chocolatey\\bin\\choco.exe install rustup.install -y") # nosec

    if os.path.exists(home + "\\.cargo\\bin\\rustc.exe"):
      if not os.path.exists(home + "\\.cargo\\bin\\cargo-tauri.exe"):
        print("Tauri is not installed...")
        subprocess.call([home + "\\.cargo\\bin\\cargo.exe", "install", "tauri-cli"], shell=False) # nosec

    check = ["C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe;docker-desktop",
             "C:\\ProgramData\\chocolatey\\lib\\deno\\deno.exe;deno",
             "C:\\Program Files\\Microsoft VS Code\\bin\\code;vscode",
             "C:\\Program Files\\Git\\cmd\\git.exe;git",
             "C:\\Program Files\\PowerShell\\7\\pwsh.exe;powershell-core",
             "C:\\Program Files\\nodejs\\node.exe;nodejs",
             "C:\\ProgramData\\chocolatey\\bin\\make.exe;make",
             "C:\\Strawberry\\perl\\bin\\perl.exe;StrawberryPerl",
             "C:\\tools\\neovim\\nvim-win64\\bin\\nvim-qt.exe;neovim"
             ]
    
    for c in check:
      if not os.path.exists(c.split(";")[0]):
        print(c.split(";")[0] + " is not installed...")
        if os.path.exists("C:\\ProgramData\\chocolatey\\bin\\choco.exe"):
          os.system("C:\\ProgramData\\chocolatey\\bin\\choco.exe install " + c.split(";")[1] + " -y") # nosec

    if not os.path.exists(home + ".\\AppData\\Roaming\\npm\\astro.cmd"):
      print("Astro not installed...")
      os.environ['PATH'] += os.pathsep + 'C:/Program Files/nodejs/'
      subprocess.call(["C:\\Program Files\\nodejs\\npm.cmd", "install", "astro", "-g"], shell=False) # nosec

    if not os.path.exists("C:\\ProgramData\\tailwinds\\tailwindcss.exe"):
      subprocess.call(["C:\\Windows\\System32\\curl.exe","-sLO","https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe"], shell=False) # nosec
      if not os.path.exists("C:\\ProgramData\\tailwinds"):
        os.makedirs("C:\\ProgramData\\tailwinds")
        shutil.move("./tailwindcss-windows-x64.exe","C:\\ProgramData\\tailwinds\\tailwindcss.exe")

    if not os.path.exists(home + ".\\AppData\\Local\\nvim"):
      print("Neovim Kickstart not installed...")
      subprocess.call(["C:\\Program Files\\Git\\cmd\\git.exe", "clone", "https://github.com/nvim-lua/kickstart.nvim.git", f'{home}\\AppData\\Local\\nvim'], shell=False) # nosec
      file_size = os.path.getsize(home + "\\AppData\\Local\\nvim\\init.lua")
      with open(home + "\\AppData\\Local\\nvim\\init.lua", 'r', buffering=file_size) as file :
        try:
            filedata = file.read(file_size)
        except OverflowError as err:
          print(err)
          filedata = ""
        filedata = filedata.replace(f'-- pyright = {{}},', 'pyright = {}, svelte = {}, astro = {}, zls = {}, powershell_es = {},')
        filedata = filedata.replace('-- rust_analyzer', 'rust_analyzer')
        filedata = filedata.replace('-- tsserver', 'tsserver')
      with open(home + "\\AppData\\Local\\nvim\\init.lua", 'w', buffering=file_size) as file:
        file.write(filedata)

def linux(home):
  if os.name == "posix":
    if os.path.exists("/etc/lsb-release"):
      file_size = os.path.getsize("/etc/lsb-release")
      f = open("/etc/lsb-release","r",buffering=file_size)
      read = f.read(file_size)
    else:
      read = ""
    if os.path.exists("/etc/os-release"):
      file_size = os.path.getsize("/etc/os-release")
      f = open("/etc/os-release","r",buffering=file_size)
      read = f.read(file_size)
    else:
      read = ""
    if "DISTRIB_ID=Ubuntu" in read or 'NAME="Ubuntu"' in read  or 'NAME="Debian GNU/Linux"' in read:
      print("Ubuntu/Debian")
      import apt #type: ignore # pylint: disable=import-error
      try:
        import requests #type: ignore # pylint: disable=import-error
      except ImportError:
        os.system('sudo apt-get install python3-requests') # nosec
        import requests #type: ignore # nosec

      if 'NAME="Debian GNU/Linux"' in read:
        if os.geteuid() == 0:
          # Setting Debian Stable to Debian Testing
          file_size = os.path.getsize('/etc/apt/sources.list')
          with open('/etc/apt/sources.list', 'r',buffering=file_size) as file :
            filedata = file.read(file_size)
          filedata = filedata.replace('stable', 'testing')
          with open('/etc/apt/sources.list', 'w', buffering=file_size) as file:
            file.write(filedata)
        
      subprocess.call(["sudo", "apt", "update"], shell=False) # nosec
      subprocess.call(["sudo", "apt", "upgrade", "-y"], shell=False) # nosec
      needed_packages = ["curl", "wget", "zsh", "git", "ansible-core", "software-properties-common", "neovim", "unzip", \
                         "apt-transport-https", "ca-certificates", "lsb-release", "libwebkit2gtk-4.0-dev", \
                         "build-essential", "libssl-dev", "libgtk-3-dev", "libayatana-appindicator3-dev", \
                         "librsvg2-dev", "libfuse2","libjavascriptcoregtk-4.1-dev","libwebkit2gtk-4.1-dev","libsoup-3.0-dev"
                        ]
      cache = apt.Cache() # nosec
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
        try:
          request = requests.get('https://deb.nodesource.com/setup_20.x', timeout=600)
          subprocess.call([request.content], shell=False) # nosec
          cache = apt.Cache()
          cache['nodejs'].mark_install()
          cache.commit()
        except requests.exceptions.Timeout:
          print("Nodejs Timed Out")

      if not os.path.exists("/usr/bin/code"):
        print('VSCode is not installed...')
        command = f'/bin/bash -c "$(wget -O- https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor | sudo tee /usr/share/keyrings/vscode.gpg)"'
        proc = subprocess.Popen(command, shell=True, stdout=True) # nosec
        (output, err) = proc.communicate()
        command2 = f'/bin/bash -c "$(echo deb [arch=amd64 signed-by=/usr/share/keyrings/vscode.gpg] https://packages.microsoft.com/repos/vscode stable main | sudo tee /etc/apt/sources.list.d/vscode.list)"'
        proc = subprocess.Popen(command2, shell=True, stdout=True) # nosec
        (output, err) = proc.communicate()
        subprocess.call(["sudo", "apt", "update"], shell=False) # nosec 
        subprocess.call(["sudo", "apt", "install", "code", "-y"], shell=False) # nosec

      if not os.path.exists("/usr/local/bin/starship"):
        command = f'/bin/bash -c "$(curl https://starship.rs/install.sh --output /tmp/starship.sh)"'
        proc = subprocess.Popen(command, shell=True, stdout=True) # nosec
        (output, err) = proc.communicate()
        subprocess.call(['chmod', '+x', '/tmp/starship.sh'], shell=False) # nosec
        subprocess.run(['sh', '/tmp/starship.sh', '-y'], shell=False) # nosec
        subprocess.run(['sudo', 'rm', '/tmp/starship.sh'], shell=False) # nosec

      if not os.path.exists('/usr/bin/docker'):
        print('Docker is not installed...')
        if "DISTRIB_ID=Ubuntu" in read or 'NAME="Ubuntu"' in read:
          subprocess.call(['sudo', 'mkdir', '-m', '0755', '-p', '/etc/apt/keyrings']) # nosec
          command = f'/bin/bash -c "$(curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg)"'
          proc = subprocess.Popen(command, shell=True, stdout=True) # nosec
          (output, err) = proc.communicate()
          command = f'/bin/bash -c "$(echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null)"'
          proc = subprocess.Popen(command, shell=True, stdout=True) # nosec
          (output, err) = proc.communicate()
        elif 'NAME="Debian GNU/Linux"' in read:
          subprocess.call(['sudo', 'mkdir', '-m', '0755', '-p', '/etc/apt/keyrings']) # nosec
          command = f'/bin/bash -c "$(curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg)"'
          proc = subprocess.Popen(command, shell=True, stdout=True) # nosec
          (output, err) = proc.communicate()
          command = f'/bin/bash -c "$(echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null)"'
          proc = subprocess.Popen(command, shell=True, stdout=True) # nosec
          (output, err) = proc.communicate()
        try:
          subprocess.run(['sudo', 'apt', 'update'], shell=False) # nosec
          needed_packages = ["docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin", "docker-compose-plugin"]
          cache = apt.Cache() # nosec
          for package in needed_packages:
            if not cache[package].is_installed:
              cache[package].mark_install()
        except:
          print("Error with Docker apt")

        if cache.install_count > 0:
          try:
            print("Installing missing APT Build packages")
            cache.commit()
          except Exception as arg:
            print("Sorry, package installation failed [{err}]".format(err=str(arg)))

      if not os.path.exists(home + "/.config/nvim"):
        if not os.geteuid() == 0:
          subprocess.call(["git", "clone", "https://github.com/nvim-lua/kickstart.nvim.git", home + "/.config/nvim"], shell=False) # nosec
          file_size = os.path.getsize(home + "/.config/nvim/init.lua")
          with open(home + "/.config/nvim/init.lua", 'r', buffering=file_size) as file :
            filedata = file.read(file_size)
          filedata = filedata.replace(f'-- pyright = {{}},', 'pyright = {}, svelte = {}, astro = {}, zls = {}, powershell_es = {},')
          filedata = filedata.replace('-- rust_analyzer', 'rust_analyzer')
          filedata = filedata.replace('-- tsserver', 'tsserver')
          with open(home + "/.config/nvim/init.lua", 'w', buffering=file_size) as file:
            file.write(filedata)
      
      if not os.path.exists(home + "/.deno/bin/deno"):
        if os.geteuid() == 0:
          exit("You can't run Deno installation with sudo")
        else:
            try:
              request = requests.get('https://deno.land/x/install/install.sh', timeout=600)
              subprocess.call([request.content], shell=False) #nosec
            except requests.exceptions.Timeout:
              print("Deno Timed Out")
            
      if not os.path.exists(home + "/.bun/bin/bun"):
        if os.geteuid() == 0:
          exit("You can't run Bun installation with sudo")
        else:
            command = f'/bin/bash -c "$(curl -fsSL https://bun.sh/install | bash)"'
            proc = subprocess.Popen(command, shell=True, stdout=True) # nosec
            (output, err) = proc.communicate()

      if not os.path.exists(home + "/.zshrc"):
        if os.geteuid() == 0:
          exit("You can't run zshrc with sudo")
        else:
            try:
              request = requests.get('https://raw.githubusercontent.com/Hamm1/devbox/main/zshrc', timeout=600)
              f = open(home + "/.zshrc", "w")
              f.write(request.text)
              f.close()
            except requests.exceptions.Timeout:
              print("ZSHRC Timed out")
            
            command = f'/bin/bash -c "$(chsh -s $(which zsh))"'
            proc = subprocess.Popen(command, shell=True, stdout=True) # nosec
            (output, err) = proc.communicate()
            home = os.path.expanduser('~')
            subprocess.call(["git", "clone", "https://github.com/zsh-users/zsh-autosuggestions", f'{home}/.zsh/zsh-autosuggestions']) # nosec
        
      if not os.path.exists(home + "/.cargo/bin/rustc") and not os.path.exists("/usr/bin/rustc"):
        print('Rust is not installed...')
        if os.geteuid() == 0:
          exit("You can't run Rust installation with sudo")
        else:
          try:
            request = requests.get('https://sh.rustup.rs',timeout=600)
            f = open("./rust.sh", "w")
            f.write(request.text)
            f.close()
          except requests.exceptions.Timeout:
            print("Rust Timed Out")
          
          subprocess.call(["chmod", "+x", "./rust.sh"], shell=False) # nosec
          subprocess.call(["sh","./rust.sh","-y"], shell=False) # nosec
          subprocess.call(["sh","rm","./rust.sh"], shell=False) # nosec
          #subprocess.call([request.content], shell=True)
          #command = f'/bin/bash -c "$(curl https://sh.rustup.rs --output ./rust.sh;chmod +x ./rust.sh;./rust.sh -y;rm ./rust.sh)"'
          #proc = subprocess.Popen(command, shell=True, stdout=True)
          #(output, err) = proc.communicate()
          # subprocess.call(["sh", "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"])

    if 'DISTRIB_ID="Arch"' in read or os.path.exists('/etc/pacman.conf'):
      print("Arch")
      subprocess.call(["sudo", "pacman-key", "--init"], shell=False) # nosec
      subprocess.call(["sudo", "pacman-key", "--populate", "archlinux"], shell=False) # nosec
      needed_packages = ["gst-plugins-base", "gst-plugins-base-libs", "webkit2gtk", "webkit2gtk-4.1", "curl", "wget" ,"openssl", "appmenu-gtk-module" \
                         , "gtk3", "libappindicator-gtk3", "librsvg", "llvm-libs" \
                         , "libvips", "nodejs", "npm", "rust", "rust-src", "docker", "unzip", "deno", "zsh", "starship", "python-requests", "neovim"]
      # needed_packages.append("base-devel")
      subprocess.call(["sudo", "pacman", "-Syy"], shell=False) # nosec
      for package in needed_packages:
        check = subprocess.call(["pacman", "-Qe", package], shell=False) # nosec
        if check != 0:
          subprocess.call(["sudo","pacman", "-S", "--needed", package, "--noconfirm"], shell=False) # nosec

      if not os.path.exists("/usr/bin/yay"):
        if os.geteuid() == 0:
          print("You can't run yay with sudo")
        else:
          subprocess.call(["git", "clone", "https://aur.archlinux.org/yay.git"], shell=False) # nosec
          subprocess.call(["sudo", "chown", "-R" "$(whoami)", ":", "$(whoami)", "./yay"], shell=False) # nosec
          cwd = os.getcwd()
          os.chdir(cwd + "/yay")
          subprocess.call(["makepkg", "-si", "--noconfirm"], shell=False) # nosec
          os.chdir(cwd)
          subprocess.call(["sudo", "rm", "-rf", "yay"], shell=False) # nosec
      
      if not os.path.exists(home + "/.zshrc"):
        if os.geteuid() == 0:
          print("You can't run zshrc with sudo")
        else:
          import requests #type: ignore # pylint: disable=import-error
          try:
            request = requests.get('https://raw.githubusercontent.com/Hamm1/devbox/main/zshrc', timeout=600)
            f = open(home + "/.zshrc", "w")
            f.write(request.text)
            f.close()
          except requests.exceptions.Timeout:
            print("ZSHRC Timed Out")
          
          command = f'/bin/bash -c "$(chsh -s $(which zsh))"'
          proc = subprocess.Popen(command, shell=True, stdout=True) # nosec
          (output, err) = proc.communicate()
          subprocess.call(["git", "clone", "https://github.com/zsh-users/zsh-autosuggestions", home + "/.zsh/zsh-autosuggestions"], shell=False) # nosec

      if os.path.exists("/usr/bin/yay") and not os.path.exists("/usr/bin/bun"):
        subprocess.call(["yay", "-S", "bun-bin", "--noconfirm"], shell=False) # nosec

      if os.path.exists("/usr/bin/yay") and not os.path.exists("/usr/bin/code"):
        subprocess.call(["yay", "-S", "visual-studio-code-bin", "--noconfirm"], shell=False) # nosec

      if not os.path.exists(home + "/.config/nvim"):
        if not os.geteuid() == 0:
          subprocess.call(["git", "clone", "https://github.com/nvim-lua/kickstart.nvim.git", home + "/.config/nvim"], shell=False) # nosec
          file_size = os.path.getsize(home + "/.config/nvim/init.lua")
          with open(home + "/.config/nvim/init.lua", 'r', buffering=file_size) as file :
            try:
              filedata = file.read(file_size)
            except OverflowError as err:
              filedata = ""
          filedata = filedata.replace(f'-- pyright = {{}},', 'pyright = {}, svelte = {}, astro = {}, zls = {}, powershell_es = {},')
          filedata = filedata.replace('-- rust_analyzer', 'rust_analyzer')
          filedata = filedata.replace('-- tsserver', 'tsserver')
          with open(home + "/.config/nvim/init.lua", 'w', buffering=file_size) as file:
            file.write(filedata)

      if os.geteuid() != 0:
        print("You have to run the python script as sudo to modify pacman.conf")
      else:
        import requests #type: ignore # pylint: disable=import-error
        try:
          request = requests.get('https://raw.githubusercontent.com/Hamm1/devbox/main/pacman.conf', timeout=600)
          f = open("/etc/pacman.conf", "w")
          f.write(request.text)
          f.close()
        except requests.exceptions.Timeout:
          print("Pacman Timed Out")

    if os.path.exists("/etc/fedora-release"):
      print("Fedora") 
      import rpm #type: ignore # pylint: disable=import-error
      try:
          import requests #type: ignore # pylint: disable=import-error
      except ImportError:
          os.system('sudo apt-get install python3-requests') # nosec
      import requests #type: ignore # pylint: disable=import-error
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
          subprocess.call(["sudo","dnf","install",missing,"-y"], shell=False) # nosec
  
if __name__ == "__main__":
  main()
