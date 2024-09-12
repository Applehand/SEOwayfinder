from setuptools import setup
from setuptools.command.install import install
import subprocess

class PostInstallCommands(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        try:
            import playwright
            subprocess.check_call(['playwright', 'install'])
            print("Playwright successfully installed.")
        except ImportError:
            print("Playwright is not installed. Please install it using 'pip install playwright'.")

setup(
    cmdclass={
        'install': PostInstallCommands,
    },
)
