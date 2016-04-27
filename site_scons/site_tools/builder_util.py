class BuilderFactory():
    def __init__(self, tool_name, bin_name, builder_name, action):
        self.tool_name = tool_name
        self.bin_name = bin_name
        self.builder_name =builder_name
        self.action = action

    def get_generate(self):
        def generate(env):
            import SCons.Builder
            import SCons.Action

            tool_bin = self.find_tool_bin(env)
            if tool_bin != None:
                action = tool_bin + ' ' + self.action
                env['BUILDERS'][self.builder_name] = SCons.Builder.Builder(action=action)
            else:
                env['BUILDERS'][self.builder_name] = SCons.Builder.Builder(action=env.Action(self.complain))
        return generate

    def get_exists(self):
        def exists(env):
            return self.find_tool_bin(env) != None
        return exists

    def find_tool_bin(self, env):
        tool_bin = env.WhereIs(self.bin_name)
        if tool_bin == None:
            print('INFORMATION: {name}: not found.'.format(name=name))
        return tool_bin

    def complain(self, target, source, env):
        print('INFORMATION: {name} binary was not found (see above).'.format(name=self.bin_name))

