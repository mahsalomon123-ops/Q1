name: Build APK

on:
  push:
    branches: [ master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - name: Install deps
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev cmake libffi-dev libssl-dev
        pip install buildozer cython==0.29.36
    - name: Build
      run: |
        export APP_ANDROID_ACCEPT_SDK_LICENSE=1
        export TMPDIR=$RUNNER_TEMP
        buildozer android debug
    - name: Upload
      uses: actions/upload-artifact@v4
      with:
        name: package
        path: bin/*.apk
