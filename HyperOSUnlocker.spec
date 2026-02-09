# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['hyperosunlocker_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('xiaomi.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HyperOSUnlocker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='D:\\Yedek\\Çalışmalar\\auto-hyperos-unlocker-main\\version_info.txt',
    icon=['D:\\Yedek\\Çalışmalar\\auto-hyperos-unlocker-main\\xiaomi.ico'],
)
