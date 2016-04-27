import os.path

env = Environment()

source_test = Glob(os.path.join('tests','*.py'))
source_test_str = ' '.join(str(src) for src in Glob(os.path.join('tests','*.py')))

source_all = Glob('*.py') + [Dir('dploy')] + source_test
source_all_str = ' '.join(str(src) for src in source_all)

PhonyTarget('setup-requirements',
            'pip install --user -r requirements.txt',
            env)
PhonyTarget('lint', 'pylint --files-output=n --reports=n ' + source_all_str, env)
PhonyTarget('test', 'py.test -v', env)
env.Alias('setup', 'setup-requirements')

Default(['lint', 'test'])
