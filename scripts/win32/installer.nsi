!ifndef VERSION
  !define VERSION 'Elfec'
!endif
!addplugindir "nsisPlugins"

; The name of the installer
Name "${VERSION}"

; The file to write
OutFile "${VERSION}.exe"

; The default installation directory
InstallDir $PROGRAMFILES\${VERSION}

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\${VERSION}" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

; Set the LZMA compressor to reduce size.
SetCompressor /SOLID lzma
;--------------------------------

!include "MUI2.nsh"
!include Library.nsh

!define MUI_ICON "dist/Elfec/resources/elfec.ico"
!define MUI_BGCOLOR FFFFFF

; Directory page defines
!define MUI_DIRECTORYPAGE_VERIFYONLEAVE

; Header
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_RIGHT
!define MUI_HEADERIMAGE_BITMAP "header.bmp"
!define MUI_HEADERIMAGE_BITMAP_NOSTRETCH 
; Don't show the component description box
!define MUI_COMPONENTSPAGE_NODESC

;Do not leave (Un)Installer page automaticly
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_UNFINISHPAGE_NOAUTOCLOSE

;Run Cura after installing
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT "Iniciar ${VERSION}"
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchLink"

; Pages
;!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "Spanish"

; Reserve Files
!insertmacro MUI_RESERVEFILE_LANGDLL
ReserveFile '${NSISDIR}\Plugins\InstallOptions.dll'
ReserveFile "header.bmp"

;--------------------------------

; The stuff to install
Section "${VERSION}"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /r "dist\"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM "SOFTWARE\${VERSION}" "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${VERSION}" "DisplayName" "${VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${VERSION}" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${VERSION}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${VERSION}" "NoRepair" 1
  WriteUninstaller "uninstall.exe"

  ; Write start menu entries for all users
  SetShellVarContext all
  
  CreateDirectory "$SMPROGRAMS\${VERSION}"
  CreateShortCut "$SMPROGRAMS\${VERSION}\Uninstall ${VERSION}.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\${VERSION}\${VERSION}.lnk" "$INSTDIR\python\pythonw.exe" '-m "Elfec.main"' "$INSTDIR\Elfec\resources\elfec.ico" 0

  ; Give all users write permissions in the install directory, so they can read/write profile and preferences files.
  AccessControl::GrantOnFile "$INSTDIR" "(S-1-5-32-545)" "FullAccess"
SectionEnd

Function LaunchLink
  ; Write start menu entries for all users
  SetShellVarContext all
  ExecShell "" "$SMPROGRAMS\${VERSION}\${VERSION}.lnk"
FunctionEnd

Section "Instalar ftdi Drivers"
  ; Set output path to the driver directory.
  SetOutPath "$INSTDIR\drivers\"
  File /r "dist\drivers\"
  
  ${If} ${RunningX64}
    ExecWait '"$INSTDIR\drivers\ftdi.exe"'
  ${Else}
    ExecWait '"$INSTDIR\drivers\ftdi.exe"'
  ${EndIf}
SectionEnd

; Uninstaller
Section "Uninstall"
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${VERSION}"
  DeleteRegKey HKLM "SOFTWARE\${VERSION}"

  ; Write start menu entries for all users
  SetShellVarContext all
  ; Remove directories used
  RMDir /r "$SMPROGRAMS\${VERSION}"
  RMDir /r "$INSTDIR"
SectionEnd
