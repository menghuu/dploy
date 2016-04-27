import SCons.Builder
import SCons.Action
import builder_util

tool_name = 'pylint'
bin_name = tool_name
builder_name = 'Pylint'
action = '--files-output=n --reports=n $SOURCES'

builder_factory = builder_util.BuilderFactory(tool_name,
                                              bin_name,
                                              builder_name,
                                              action)
generate = builder_factory.get_generate()
exists = builder_factory.get_exists()
