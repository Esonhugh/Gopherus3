from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
long_description = None
import gopherus3

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='gopherus3', # 包名称
      package_dir={'gopherus3': 'gopherus3'}, # 包目录
      version='0.0.5', # 版本
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python', 'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3'
      ],
      install_requires=['ping3'],
      # entry_points={'console_scripts': ['']},
      package_data={'': ['*.json']},
      author='esonhugh', # 作者
      entry_points={'console_scripts': ['gopherus3=gopherus3.gopherus:main']},
      author_email='esonhughoutside@gmail.com', # 作者邮箱
      description='goher protocol link creator', # 介绍
      long_description=long_description, # 长介绍，在pypi项目页显示
      long_description_content_type='text/markdown', # 长介绍使用的类型，我使用的是md
      url='https://github.com/Esonhugh/Gopherus3', # 包主页，一般是github项目主页
      license='MIT', # 协议
      keywords='gopher gopherus gopherus3 gopherus-python3') # 关键字 搜索用