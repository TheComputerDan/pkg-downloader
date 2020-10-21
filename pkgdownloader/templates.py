from jinja2 import FileSystemLoader, Environment
from pathlib import Path
import os

class Templates(object):
    def __init__(self, image:str, tag:str):
        self.image = image
        self.tag = tag
        self.jinja_extension = ".jinja"
        self.dockerfile_template_rpm = "DOCKERFILE-rpm.jinja"
        self.dockerfile_template_deb = "DOCKERFILE-deb.jinja"
        self.docker_compose_template = "docker-compose.yml.jinja"
        self.docker_directory = Path(__file__).parents[0] / "docker"
        self.templates_location = Path(__file__).parents[0] / "templates"
        self.rpm_distributions = ['centos']
        self.deb_distributions = ['debian','ubuntu']

    def print_file(self):
        print(self.docker_directory)

    def dockerfile_setup(self, packages:list,**kwargs):
        templateLoader = FileSystemLoader(searchpath=self.templates_location)
        templateEnv = Environment(loader=templateLoader)

        init_script = kwargs.get('init_script')

        if self.image in self.rpm_distributions:
            dockerfile_template = self.dockerfile_template_rpm
        elif self.image in self.deb_distributions:
            dockerfile_template = self.dockerfile_template_deb
        else:
            raise NotImplemented(f"{self.image} is currently unsupported.")
        
        template = templateEnv.get_template(dockerfile_template)

        outputText = template.render(image=self.image,tag=self.tag,packages=packages,init_script=init_script)

        new_path = self.docker_directory / dockerfile_template.split(".jinja")[0]
        with open(new_path, 'w') as nf:
            nf.write(outputText)

    def base_packages_directory(self) -> Path:
        return self.docker_directory / Path(f"{self.image}_{self.tag}_packages")

    def volume_directory(self, packages:list) -> Path:
        base_package_dir = Path(f"{self.image}_{self.tag}_packages")
        for package in packages:
            os.makedirs(self.docker_directory / base_package_dir / package)
        return base_package_dir