from Cython.Build import cythonize
from setuptools import Extension, setup

ext_modules = [
    Extension(
        name="mdp_python.MDecisionProcess",  # Nome do pacote no Python
        sources=[
            "mdp_python/MDecisionProcess.pyx",  # O seu wrapper Cython
            "cpp_core/AgentEnvironment.cpp",  # A implementação C++
            "cpp_core/DynamicProgramming.cpp",  # A implementação C++
            "cpp_core/ValueFunctions.cpp",  # (Adicione se você os separou em arquivos diferentes)
        ],
        include_dirs=["cpp_core"],  # Onde o compilador vai achar os arquivos .hpp
        language="c++",  # Avisa que estamos usando C++ e não C
    )
]

setup(
    name="MDP_Engine",
    ext_modules=cythonize(ext_modules, language_level="3"),
)
