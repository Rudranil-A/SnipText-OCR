# SnipText.spec

block_cipher = None

a = Analysis(
    ['SnipText.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('config.ini', '.'),          # Include settings/config
        ('assets/*', 'assets'),       # Include all assets like icons, themes, etc.
        ('modules/*', 'modules'),     # Include your custom snipper and settings modules
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SnipTextApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False  # Set to True only if you want the terminal to open too
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='SnipTextApp'
)
