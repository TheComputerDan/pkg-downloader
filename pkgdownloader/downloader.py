from docker import from_env
from pathlib import Path
from pkgdownloader.templates import Templates

class Downloader(object):

    def __init__(self, os, version):
        self.docker_directory = Path(__file__).parents[0] / "docker"
        self.tag = f"packages_dowloader_{os}_{version}"
        self.client = from_env()
        self.os = os
        self.version = version
        self.rpm_distributions = ['centos','fedora']
        self.deb_distributions = ['debian','ubuntu']

    def build_image(self):

        if self.os in self.rpm_distributions:
            dockerfile_name = "DOCKERFILE-rpm"
        elif self.os in self.deb_distributions:
            dockerfile_name = "DOCKERFILE-deb"
        else:
            raise NotImplemented(f"{self.image} is currently unsupported.")

        output = self.client.images.build(
            path=str(self.docker_directory),
            dockerfile=dockerfile_name,
            tag=self.tag
        )

        return output

    def run_image(self, **kwargs):

        template = Templates(image=self.os,tag=self.version)

        if kwargs.get("location"):
            location =  Path(kwargs.get("location")) / Path(f"{self.os}_{self.version}_packages")
        else: 
            location = template.base_packages_directory()

        self.client.containers.run(
            image=self.tag,
            volumes={
                str(location): {
                    'bind': f'/{self.os}_{self.version}_packages',
                    'mode': 'rw'
                }
            },
            auto_remove=True
        )
