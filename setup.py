from distutils.core import setup, Extension
import sys

module1 = Extension('bsvcuckoo',
                    include_dirs=['include'],
                    sources=["src/cuckoo_filter.c", "src/cuckoo_python.c"],
                    # https://cibuildwheel.readthedocs.io/en/stable/faq/#windows-importerror-dll-load-failed-the-specific-module-could-not-be-found
                    extra_compile_args=['/d2FH4-'] if sys.platform == 'win32' else [])

setup(name='bsvcuckoo',
      version='1.3',
      description='A cuckoo filter implementation.',
      author='Roger Taylor',
      author_email='roger.taylor.email@gmail.com',
      url='https://github.com/electrumsv/libcuckoofilter',
      long_description=open('README.md', 'r').read(),
      long_description_content_type='text/markdown',
      license='MIT Licence',
      # This warns about no `__init__.py` file but seems to install workable types.
      packages=['bsvcuckoo-stubs'],
      package_data={"bsvcuckoo-stubs": ['__init__.pyi']},
      # The actual package.
      ext_modules=[ module1 ])
