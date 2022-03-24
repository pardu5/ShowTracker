# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Show_Tracker.py'],
             pathex=[],
             binaries=[],
             datas=[
                 ('.\\images\\blue_plus_circle.png', '.\\images\\'),
                 ('.\\images\\cross_red_circle.png', '.\\images\\'),
                 ('.\\images\\green_play_button.png', '.\\images\\'),
                 ('.\\images\\internet-globe.png', '.\\images\\'),
                 ('.\\images\\eye_ball_circle.png', '.\\images\\'),
                 ('.\\config\\.env', '.\\config\\.'),
                 ('.\\config\\config.json', '.\\config\\')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Show_Tracker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Show_Tracker')
