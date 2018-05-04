from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_exe_options = {
    "packages": ['six', 'idna.idnadata', 'appdirs', 'packaging.specifiers', 'packaging.requirements', 'psutil', 'queue'],
    "include_files": ["config.json"]
}

base = 'Console'

executables = [
    Executable('__main__.py', base=base, targetName = 'ia-agent')
]

setup(name='ia-agent',
      version = '1.0',
      description = '',
      options = dict(build_exe = build_exe_options),
      executables = executables)
