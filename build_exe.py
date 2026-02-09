"""
EXE Builder Script for HyperOS Bootloader Unlocker
Copyright © 2026 SerdarOnline
"""

import PyInstaller.__main__
import os

# Proje dizini
project_dir = os.path.dirname(os.path.abspath(__file__))

# Version info dosyası oluştur
version_info = """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'SerdarOnline'),
        StringStruct(u'FileDescription', u'HyperOS Bootloader Unlocker - Xiaomi Bootloader Kilit Açma Aracı'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'HyperOSUnlocker'),
        StringStruct(u'LegalCopyright', u'Copyright © 2026 SerdarOnline. Tüm hakları saklıdır.'),
        StringStruct(u'OriginalFilename', u'HyperOSUnlocker.exe'),
        StringStruct(u'ProductName', u'HyperOS Bootloader Unlocker'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""

# Version info dosyasını kaydet
version_file = os.path.join(project_dir, 'version_info.txt')
with open(version_file, 'w', encoding='utf-8') as f:
    f.write(version_info)

print("🚀 EXE oluşturuluyor...")
print("📦 PyInstaller başlatılıyor...")

# PyInstaller parametreleri
PyInstaller.__main__.run([
    'hyperosunlocker_gui.py',
    '--name=HyperOSUnlocker',
    '--onefile',
    '--windowed',
    f'--icon={os.path.join(project_dir, "xiaomi.ico")}',
    f'--version-file={version_file}',
    '--add-data=xiaomi.ico;.',
    '--add-data=forum_logo.png;.',
    '--clean',
    '--noconfirm',
    '--strip',
    '--optimize=2',
    '--upx-dir=.',
    '--noupx',  # UPX antivirüs tespiti artırıyor, kapalı tutalım
    # Qt5 modüllerini minimize et (sadece gerekenleri)
    '--exclude-module=PyQt5.QtBluetooth',
    '--exclude-module=PyQt5.QtDBus',
    '--exclude-module=PyQt5.QtDesigner',
    '--exclude-module=PyQt5.QtHelp',
    '--exclude-module=PyQt5.QtLocation',
    '--exclude-module=PyQt5.QtMultimedia',
    '--exclude-module=PyQt5.QtMultimediaWidgets',
    '--exclude-module=PyQt5.QtNetwork',
    '--exclude-module=PyQt5.QtNfc',
    '--exclude-module=PyQt5.QtOpenGL',
    '--exclude-module=PyQt5.QtPositioning',
    '--exclude-module=PyQt5.QtPrintSupport',
    '--exclude-module=PyQt5.QtQml',
    '--exclude-module=PyQt5.QtQuick',
    '--exclude-module=PyQt5.QtQuickWidgets',
    '--exclude-module=PyQt5.QtSensors',
    '--exclude-module=PyQt5.QtSerialPort',
    '--exclude-module=PyQt5.QtSql',
    '--exclude-module=PyQt5.QtSvg',
    '--exclude-module=PyQt5.QtTest',
    '--exclude-module=PyQt5.QtWebChannel',
    '--exclude-module=PyQt5.QtWebEngine',
    '--exclude-module=PyQt5.QtWebEngineCore',
    '--exclude-module=PyQt5.QtWebEngineWidgets',
    '--exclude-module=PyQt5.QtWebSockets',
    '--exclude-module=PyQt5.QtXml',
    '--exclude-module=PyQt5.QtXmlPatterns',
    '--exclude-module=PyQt5.Qt3DAnimation',
    '--exclude-module=PyQt5.Qt3DCore',
    '--exclude-module=PyQt5.Qt3DExtras',
    '--exclude-module=PyQt5.Qt3DInput',
    '--exclude-module=PyQt5.Qt3DLogic',
    '--exclude-module=PyQt5.Qt3DRender',
    # Selenium ve browser driver modülleri (çok yer kaplıyor)
    '--exclude-module=selenium.webdriver.chrome',
    '--exclude-module=selenium.webdriver.firefox',
    '--exclude-module=selenium.webdriver.edge',
    '--exclude-module=selenium.webdriver.safari',
    '--exclude-module=selenium.webdriver.ie',
    # Diğer gereksiz modüller
    '--exclude-module=tkinter',
    '--exclude-module=matplotlib',
    '--exclude-module=pandas',
    '--exclude-module=numpy',
    '--exclude-module=PIL',
    '--exclude-module=IPython',
    '--exclude-module=pytest',
    '--exclude-module=doctest',
    '--exclude-module=pdb',
    '--exclude-module=unittest',
    '--exclude-module=test',
    '--exclude-module=setuptools',
    '--exclude-module=distutils',
    '--exclude-module=email',
    # Python stdlib'den gereksizler
    '--exclude-module=curses',
    '--exclude-module=readline',
    '--exclude-module=pydoc',
    '--exclude-module=pydoc_data',
    # DLL boyutunu azalt
    '--log-level=WARN',
])

print("\n✅ EXE başarıyla oluşturuldu!")
print(f"📁 Konum: {os.path.join(project_dir, 'dist', 'HyperOSUnlocker.exe')}")
print("\n📝 Program Bilgileri:")
print("   İsim: HyperOS Bootloader Unlocker")
print("   Versiyon: 1.0.0.0")
print("   Telif Hakkı: © 2026 SerdarOnline")
print("   Açıklama: Xiaomi Bootloader Kilit Açma Aracı")
