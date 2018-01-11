from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='aws_tools',
      version='0.1',
      description='Tools for Cytovas AWS Stuff'
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: Commercial',
        'Programming Language :: Python :: 3.X',
      ],
      keywords='aws s3 cytovas',
      url='https://console.aws.amazon.com/codecommit/home?region=us-east-1#/repository/aws_tools/'
      author='Jeremy Leipzig',
      author_email='leipzig@cytovas.com',
      license='Commerical',
      packages=['aws_tools'],
      install_requires=[
          'subprocess',
          'boto3',
          'json',
          'requests',
          'time',
          'click',
          'os',
          'sys',
          'uuid',
          'pandas'
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['aws_tools=aws_tools.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
