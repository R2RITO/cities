from setuptools.extension import Extension
from setuptools import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from pathlib import Path
import shutil
import os


sourcefiles = set()

# Main sources
sourcefiles.add(Extension('cities.*',
                          ['cities/__init__.py']))

# private_ingest sources
sourcefiles.add(Extension('cities.private_ingest.*',
                          ['cities/private_ingest/*.py']))
sourcefiles.add(Extension('cities.private_ingest.serializers.*',
                          ['cities/private_ingest/serializers/*.py']))
sourcefiles.add(Extension('cities.private_ingest.utils.*',
                          ['cities/private_ingest/utils/*.py']))
sourcefiles.add(Extension('cities.private_ingest.views.*',
                          ['cities/private_ingest/views/*.py']))

# chicago_ingest sources
sourcefiles.add(Extension('cities.chicago_ingest.*',
                          ['cities/chicago_ingest/*.py']))
sourcefiles.add(Extension('cities.chicago_ingest.views.*',
                          ['cities/chicago_ingest/views/*.py']))

# dw_storage sources
sourcefiles.add(Extension('cities.dw_storage.*',
                          ['cities/dw_storage/*.py']))
sourcefiles.add(Extension('cities.dw_storage.utils.*',
                          ['cities/dw_storage/utils/*.py']))


# Main app sources
sourcefiles.add(Extension('cities.cities.*',
                          ['cities/cities/__init__.py']))
sourcefiles.add(Extension('cities.cities.*',
                          ['cities/cities/settings.py']))
sourcefiles.add(Extension('cities.cities.*',
                          ['cities/cities/urls.py']))


class MyBuildExt(build_ext):
    def run(self):
        build_ext.run(self)

        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent

        target_dir = build_dir if not self.inplace else root_dir

        # Manage.py
        self._copy_file(Path('cities') / 'manage.py', root_dir, target_dir)

        # Wsgi file
        self._copy_file(Path('cities/cities') / 'wsgi.py', root_dir, target_dir)
        self._copy_file(Path('cities/cities') / 'asgi.py', root_dir, target_dir)

    def _copy_file(self, path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return

        shutil.copyfile(str(source_dir / path), str(destination_dir / path))


setup(
    ext_modules=cythonize(
        sourcefiles,
        build_dir="build",
        compiler_directives=dict(
            always_allow_keywords=True,
            language_level=3,
        )
    ),
    cmdclass=dict(
        build_ext=MyBuildExt
    ),
    packages=[]
)
