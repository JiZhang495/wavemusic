import os
from setuptools import setup, Extension
import pybind11

os.environ["CC"] = "gcc"
os.environ["CXX"] = "g++"

ext_modules = [
    Extension(
        name="simple",
        sources=["src/simple.cpp", "src/sigen.cpp"],
        include_dirs=[pybind11.get_include()],
        define_macros=[("BUILD_PYBIND", None)],
        language="c++",
        extra_compile_args=["-std=c++17","-fPIC", "-fvisibility=default"]
    )
]

setup(
    name="simple",
    version="0.1",
    ext_modules=ext_modules,
)
