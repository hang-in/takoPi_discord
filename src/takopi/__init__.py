from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("takopi")
except PackageNotFoundError:
    __version__ = version("takopi-discord")
