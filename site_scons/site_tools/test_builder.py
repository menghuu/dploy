import builder_util

builder_factory = builder_util.BuilderFactory(tool_name='pytest',
                                              bin_name='py.test',
                                              builder_name='Test',
                                              action='-v $SOURCE')
generate = builder_factory.get_generate()
exists = builder_factory.get_exists()

