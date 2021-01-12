from setuptools import setup, find_packages

setup(
    name='local-crontab',
    version='0.0.1',
    license='MIT License',
    description='Convert local crontabs to UTC crontabs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andrea Salvatori',
    author_email='andrea.salvatori92@gmail.com',
    url='https://github.com/Sonic0/local-crontab',
    packages=find_packages(where='src', exclude=['tests*', '*.tests*']),
    keywords='cron, timezone, utc, dst',
    install_requires='cron-converter',
    include_package_data=True,
    extras_require={
            'test': ['unittest'],
        },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.8',
)
