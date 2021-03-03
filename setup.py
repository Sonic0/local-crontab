from setuptools import setup, find_packages

setup(
    name='local-crontab',
    version='0.1.0',
    license='MIT License',
    description='Convert local crontabs to UTC crontabs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andrea Salvatori',
    author_email='andrea.salvatori92@gmail.com',
    url='https://github.com/Sonic0/local-crontab',
    packages=find_packages(where='.', exclude=['tests*', '*.tests*']),
    keywords='cron, timezone, utc',
    install_requires=['cron-converter', 'click', 'python-dateutil'],
    include_package_data=True,
    extras_require={
            'test': ['unittest'],
        },
    entry_points={
            'console_scripts': ['local-crontab=local_crontab.command_line:main'],
        },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.8',
)
