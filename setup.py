"""
The setup.py file is an essential part of packaging and distributing Python Projects. It is used by setuptools
(of disutils in older python versions) to define the configuration of your project such as dependencies
metadata and many more
"""

from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    This function will return a list of environments
    """

    try:
        with open('requirements.txt','r') as f:
            lines=f.readlines()
            list1:List[str]=[]
            for i in lines:
                requirement=i.strip()
                #Ignore the empty lines and -e . 
                if requirement and requirement!="-e .":
                    list1.append(requirement)
    except Exception as e:
        print("Requirement.txt not found")
    return list1

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Kartik Mehta",
    author_email="kartik.prakashbhai.mehta@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements() 
)

#After -e . is executed you can see that a file named NetworkSecurity.egg-info file is created it contiains the main setup