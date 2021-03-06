from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='local-crontab',
    version='0.2.0',
    license='MIT',
    description='Convert local crontabs to UTC crontabs',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Andrea Salvatori',
    author_email='andrea.salvatori92@gmail.com',
    url='https://github.com/Sonic0/local-crontab',
    packages=['local_crontab'],
    keywords='cron, timezone, utc',
    install_requires=['cron-converter', 'click', 'python-dateutil'],
    include_package_data=True,
    extras_require={
            'test': ['unittest'],
        },
    entry_points={
            'console_scripts': ['local-crontab=local_crontab.cmd_line:main'],
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
