[app]android.ndk_path = /data/data/com.termux/files/home/Q1/android-ndk-r25b
android.sdk_path = /data/data/com.termux/files/usr/opt/android-sdk
title = Q1
package.name = q1app
package.domain = com.q1
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db
version = 1.0
requirements = python3,kivy,sqlite3
orientation = portrait
android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.ndk_path = /data/data/com.termux/files/home/Q1/android-ndk-r25b
android.sdk_path = /data/data/com.termux/files/usr/opt/android-sdk
android.skip_update = True

[buildozer]
log_level = 2
warn_on_root = 1
