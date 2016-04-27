import builder_util

tool_name = 'pytest'
bin_name = 'py.test'
builder_name = 'Pytest'
action = '-v $SOURCES'

builder_factory = builder_util.BuilderFactory(tool_name,
                                              bin_name,
                                              builder_name,
                                              action)
generate = builder_factory.get_generate()
exists = builder_factory.get_exists()

