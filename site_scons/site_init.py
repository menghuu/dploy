def PhonyTarget(target, action, env):
    env.AlwaysBuild(env.Alias(target, [], action))
