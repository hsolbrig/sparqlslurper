from pbr.version import VersionInfo

# A hand agent to use for testing
__version__ = VersionInfo('sparqlslurper')
UserAgent = f"{__version__.package}/{__version__.version_string()} " \
            f"(https://github.com/hsolbrig/PyShEx; solbrig@jhu.edu)"