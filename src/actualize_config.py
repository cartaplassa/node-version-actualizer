import subprocess
import json
import logging
import semver
from datetime import datetime

logger = logging.getLogger('__main__.' + __name__)
NPM_DATE_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"


def actualize_config(config, date):
    for package, version in config['dependencies'].items():
        if (version == 'latest'):
            latest_version = actualize_package(package, date)
            logger.info(f'Latest version of {package} by date: {latest_version}')
            config['dependencies'][package] = latest_version
    for package, version in config['devDependencies'].items():
        if (version == 'latest'):
            latest_version = actualize_package(package, date)
            logger.info(f'Latest version of {package} by date: {latest_version}')
            config['devDependencies'][package] = latest_version
    return config
    

def actualize_package(name, date):
    query = query_package(name)
    if 'error' in query.keys():
        return "latest"
    logger.debug(f'{name} created at: {query["created"]}')
    logger.debug(f'{name} last modified at: {query["modified"]}')
    versions = list(query.items())[2:]
    # TODO error handling
    # [(version, timestemp), (version, timestamp)]
    iter_version = versions[0][1]
    for index in range(len(versions)):
        if is_release(versions[index][0]):
            iter_version = versions[index][0]
        try:
            if datetime.strptime(versions[index + 1][1], NPM_DATE_FMT) > date:
                return iter_version
        except IndexError:
            return iter_version


def query_package(name):
    query = subprocess.run(["npm", "view", name, "time", "--json"], capture_output=True)
    return json.loads(query.stdout)

def is_release(version):
    ver = semver.Version.parse(version)
    return True if ver.prerelease is None and ver.build is None else False