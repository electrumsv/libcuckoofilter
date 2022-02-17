from distutils.core import setup, Extension

module1 = Extension('bsvcuckoo',
                    define_macros=[('MAJOR_VERSION', '1'),
                                   ('MINOR_VERSION', '0')],
                    include_dirs=['include'],
                    sources=["src/cuckoo_filter.c", "src/cuckoo_python.c"])

setup(name='bsvcuckoo',
      version='1.0',
      description='A cuckoo filter implementation.',
      author='Roger Taylor',
      author_email='roger.taylor.email@gmail.com',
      url='https://example.com',
      long_description='''
TBD
''',
      ext_modules=[module1])
