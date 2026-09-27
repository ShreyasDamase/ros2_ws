from setuptools import find_packages, setup

package_name = 'integration_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/integration_launch.py']),
        ('share/' + package_name + '/config', ['config/velocity_params.yml']),

    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Shreyas Damase',
    maintainer_email='shreyasdamase@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'velocity_publisher = integration_demo.velocity_publisher:main',
            'velocity_subscriber = integration_demo.velocity_subscriber:main'
        ],
    },
)
