import os
import platform

from setuptools import Extension
from setuptools import setup
from setuptools.command.build_ext import build_ext

IS_WINDOWS = platform.system() == "Windows"


class local_build_ext(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)
        import builtins

        builtins.__NUMPY_SETUP__ = False
        import numpy

        self.include_dirs.append(numpy.get_include())


libdir = "lib"
kastore_dir = os.path.join(libdir, "subprojects", "kastore")
tsk_source_files = [
    "core.c",
    "tables.c",
    "trees.c",
    "genotypes.c",
    "stats.c",
    "convert.c",
    "haplotype_matching.c",
]
sources = (
    ["_tskitmodule.c"]
    + [os.path.join(libdir, "tskit", f) for f in tsk_source_files]
    + [os.path.join(kastore_dir, "kastore.c")]
)

defines = []
libraries = []
if IS_WINDOWS:
    libraries.append("Advapi32")
    defines.append(("WIN32", None))

_tskit_module = Extension(
    "_tskit",
    sources=sources,
    extra_compile_args=["-std=c99"],
    libraries=libraries,
    define_macros=defines,
    include_dirs=["lwt_interface", libdir, kastore_dir],
)

setup(
    ext_modules=[_tskit_module],
    cmdclass={"build_ext": local_build_ext},
)
