# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件
支持中文字体和资源文件
"""

block_cipher = None

# 资源文件配置
datas = [
    ('assets/', 'assets'),
]

# 隐藏导入配置
hiddenimports = [
    'pygame',
    'pkg_resources.py2_warn',
]

# 资源文件排除配置
exclude_binaries = []

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=exclude_binaries,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TankBattle',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
