from setuptools import setup

package_name = 'perception_genie'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Hyunseok Yang',
    maintainer_email='hyunseok7.yang@lge.com',
    description='publish groundtruth relative info ',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ground_truth = perception_genie.perception_ground_truth:main'
        ],
    },
)
