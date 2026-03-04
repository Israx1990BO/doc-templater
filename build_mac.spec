# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for macOS build of EDTECH DOC TEMPLATER."""
import os
import shutil
import subprocess

block_cipher = None

# --- Paths ---
PROJECT = os.path.abspath('.')
TESS_BIN = '/opt/homebrew/bin/tesseract'
TESS_DATA = '/opt/homebrew/share/tessdata'
TESS_LIB = '/opt/homebrew/lib'

# --- Tesseract dylibs (recursive deps) ---
tess_dylibs = []
for lib_name in [
    'libtesseract.5.dylib',
    'libleptonica.6.dylib',
]:
    lib_path = os.path.join(TESS_LIB, lib_name)
    if os.path.exists(lib_path):
        tess_dylibs.append((lib_path, 'tesseract'))

# --- Tesseract binary + lang data ---
tess_binaries = [(TESS_BIN, 'tesseract')]
# Only bundle Spanish + English tessdata (keep bundle small)
tess_datas = []
for lang_file in ['eng.traineddata', 'spa.traineddata', 'osd.traineddata']:
    src = os.path.join(TESS_DATA, lang_file)
    if os.path.exists(src):
        tess_datas.append((src, 'tesseract/tessdata'))

a = Analysis(
    ['test_app.py'],
    pathex=[PROJECT],
    binaries=tess_binaries + tess_dylibs,
    datas=[
        ('static', 'static'),
        ('templates', 'templates'),
    ] + tess_datas,
    hiddenimports=[
        'flask',
        'werkzeug',
        'jinja2',
        'webview',
        'docx',
        'PIL',
        'cv2',
        'pytesseract',
        'img2table',
        'img2table.ocr',
        'img2table.document',
        'requests',
        'engineio.async_drivers.threading',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'scipy', 'numpy.testing'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='EDTECH DOC TEMPLATER',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='app_icon.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EDTECH DOC TEMPLATER',
)

app = BUNDLE(
    coll,
    name='EDTECH DOC TEMPLATER.app',
    icon='app_icon.icns',
    bundle_identifier='com.edtech.doctemplater',
    info_plist={
        'CFBundleDisplayName': 'EDTECH DOC TEMPLATER',
        'CFBundleShortVersionString': '3.5.0',
        'CFBundleVersion': '3.5.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.15',
    },
)
