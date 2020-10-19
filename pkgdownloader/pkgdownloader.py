from pkgdownloader.downloader import Downloader
from argparse import ArgumentParser, Namespace
from pkgdownloader.templates import Templates
import os

argsparse = ArgumentParser()

def parser() -> Namespace:
    argsparse.add_argument(
        '--os',
        type=str,
        action='store',
        help="Target OS for which to pull packages.",
        dest="os_type"
        )

    argsparse.add_argument(
        '--version', 
        type=str,
        action='store',
        help="Target OS Version for which to pull packages.",
        dest="os_version"
        )

    argsparse.add_argument(
        '--packages', nargs="+",
        type=str,
        action='store',default=None,
        help="Packages to download.",
        dest="packages_list"
        )
    
    argsparse.add_argument(
        '--location',
        type=str,
        action='store',default=None,
        help="Target location for download.",
        dest="download_location"
        )

    args = argsparse.parse_args()

    return args

def buildTemplate(arguments):
    template = Templates(
        image=arguments.os_type,
        tag=arguments.os_version
    )

    template.dockerfile_setup(arguments.packages_list)

def dockerRunner(arguments):
    downloadManager = Downloader(
        os=arguments.os_type,
        version=arguments.os_version
    )

    downloadManager.build_image()
    download_location = arguments.download_location if arguments.download_location else os.getcwd()
    downloadManager.run_image(
        location=download_location
    )
    downloadManager.cleanup()

def run():
    args = parser()
    buildTemplate(arguments=args)
    dockerRunner(arguments=args)
    print(f"[+] Finished downloading {args.packages_list}")