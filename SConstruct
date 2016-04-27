import os.path

env = Environment(tools=['default', 'pytest_builder', 'pylint_builder'])

source_test = Glob(os.path.join('tests','*.py'))

source_all = Glob('*.py') + [Dir('dploy')] +  source_test

PhonyTarget('setup-requirements',
            'pip install -r requirements.txt',
            env)
env.Alias('lint', env.Pylint(source_all))
env.Alias('test', env.Pytest(source_test))
env.Alias('setup', 'setup-requirements')

Default(['lint', 'test'])
