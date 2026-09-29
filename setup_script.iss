[Setup]
; Información básica de tu aplicación
AppName=Aplicación calculo diferencial
AppVersion=1.0
AppPublisher=Tu Nombre
DefaultDirName={autopf}\MiAplicacionPython
DefaultGroupName=Mi Aplicacion Python
UninstallDisplayIcon={app}\main.exe
Compression=lzma2
SolidCompression=yes
OutputDir=Output
OutputBaseFilename=Instalador_MiAplicacion_v1.0

[Tasks]
; Opción para crear un acceso directo en el Escritorio
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Archivo ejecutable principal
Source: "dist\main\main.exe"; DestDir: "{app}"; Flags: ignoreversion

; Copiar TODOS los archivos y subcarpetas que generó PyInstaller
Source: "dist\main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Accesos directos en el menú Inicio
Name: "{group}\Mi Aplicacion Python"; Filename: "{app}\main.exe"
Name: "{group}\{cm:UninstallProgram,Mi Aplicacion Python}"; Filename: "{uninstallexe}"

; Acceso directo opcional en el escritorio
Name: "{autodesktop}\Mi Aplicacion Python"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
; Opción para ejecutar la aplicación al finalizar la instalación
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,Aplicación de calculo de grafica}"; Flags: nowait postinstall skipifsilent