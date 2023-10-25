
if(!(Test-Path "C:\\Python312\\python.exe")){
    if (!(Test-Path "C:\\ProgramData\\chocolatey\\bin\\choco.exe")){
        Write-Host "Chocolatey is not installed..."
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    }
    
    if (Test-Path "C:\\ProgramData\\chocolatey\\bin\\choco.exe") {
        Start-Process "C:\\ProgramData\\chocolatey\\bin\\choco.exe" -ArgumentList "install python312 -y" -wait
    }
}

function Add-Path($Path) {
    $Path = [Environment]::GetEnvironmentVariable("PATH", "Machine") + [IO.Path]::PathSeparator + $Path
    [Environment]::SetEnvironmentVariable( "Path", $Path, "Machine" )
}

if (!(($env:PATH) | Select-String 'C:\\Program Files\\nodejs\\')){
    Add-Path 'C:\Program Files\nodejs\'
}

if (!(($env:PATH) | Select-String 'C:\\ProgramData\\tailwinds\\')){
    Add-Path 'C:\ProgramData\tailwinds\'
}

if (Test-Path "C:\\Python312\\python.exe"){
    Start-Process "C:\\Python312\\python.exe" -ArgumentList ".\configure.py" -wait -NoNewWindow
}