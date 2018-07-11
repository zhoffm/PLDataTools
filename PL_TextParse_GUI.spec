# -*- mode: python -*-

block_cipher = None


a = Analysis(['PL_TextParse_GUI.py'],
             pathex=['C:\\Users\\zhoffman\\PythonProjects\\PLDataTools'],
             binaries=[],
             datas=[('.\\assets\\icons\\pl_icon.ico', 'assets\\icons')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PL_TextParse_GUI',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='assets\\icons\\pl_icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PL_TextParse_GUI')
