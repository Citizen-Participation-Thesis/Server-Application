import base64
import os.path
from os import system, path, mkdir, makedirs, rmdir, remove, popen, chdir, replace
import time

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files.base import File, ContentFile

from .models import Project

logger = get_task_logger(__name__)

# Update these to fit your local setup
unityPath = 'C:\\"Program Files"\\Unity\\Hub\\Editor\\2020.3.26f1\\Editor\\Unity'
projectPath = "C:\\Users\\olavh\\BundleProject"  # Unity project path
initialPath = "C:\\Users\\olavh\\Desktop\\Bundling-Service"  # This repository root

assetDir = projectPath + "\\Assets"
bundleDir = assetDir + "\\BundleAssets"
bundledDirName = "\\streamingAssets"
bundledDir = assetDir + bundledDirName
editorDir = assetDir + "\\Editor"

bundleScript = "assetBundler"
bundleMethod = "Pack"
buildDirName = "\\bundle"
newBundleName = "\\newbundle"
buildDir = bundleDir


def run(cmd):
    system("cmd /c" + cmd)


def safe_remove(p):
    if path.isfile(p):
        logger.info("Removed: " + p)
        remove(p)
    else:
        logger.info("Non existent: " + p)


def safe_remove_unity(p):
    safe_remove(p)
    safe_remove(p + ".meta")


@shared_task
def bundle(names, files, title):
    if len(names) != len(files) or len(names) < 1:
        logger.info("Error: Files not sent properly")

    if not path.exists(buildDir):
        makedirs(buildDir)
    for i in range(len(names)):
        temp = files[i][2:-1]
        temp = bytes(temp, "ascii")
        file = base64.b64decode(temp)
        with open(buildDir + "\\" + names[i]+'.fbx', 'wb+') as destination:
            destination.write(file)
        logger.info("Wrote file " + str(i + 1) + " of " + str(len(names)))

    if not path.exists(editorDir):
        makedirs(editorDir)
        logger.info("dir: Editor added")
    else:
        logger.info("Exists: "+editorDir)
    if not path.exists(bundledDir):
        makedirs(bundledDir)
        logger.info("dir: Bundled added")
    else:
        logger.info("Exists: "+bundledDir)

    if not path.exists(editorDir + "\\" + bundleScript + ".cs"):
        logger.info("copy "+initialPath + "\\" + bundleScript + ".cs " + editorDir + "\\" + bundleScript + ".cs")
        popen("copy "+initialPath + "\\" + bundleScript + ".cs " + editorDir + "\\" + bundleScript + ".cs")
        logger.info("Script injected")

    chdir(editorDir)

    logger.info("Bundling...")

    method = bundleScript + "." + bundleMethod
    logger.info(unityPath + " -batchMode -nographics -projectPath " + projectPath + " -executeMethod " + method + " -quit")
    run(unityPath + " -batchMode -nographics -projectPath " + projectPath + " -executeMethod " + method + " -quit")

    while not path.exists(bundledDir+newBundleName):
        time.sleep(2)

    logger.info("File exists!")
    if path.isfile(bundledDir+newBundleName):
        project = Project.objects.get(title=title)
        encoded = open(bundledDir + newBundleName, "rb").read()
        project.bundle.save(title + "-bundle", ContentFile(encoded))
        project.status = "Deployed"
        project.save()
        logger.info("Bundled!")
    else:
        logger.info("Bundling failed!")

    logger.info("Cleanup initiating")

    for name in names:
        fp = buildDir + "\\" + name + '.fbx'
        safe_remove_unity(fp)

    safe_remove_unity(bundledDir + newBundleName)

    safe_remove_unity(bundledDir + newBundleName + ".manifest")
    safe_remove_unity(bundledDir + bundledDirName)
    safe_remove_unity(bundledDir + bundledDirName + ".manifest")

    logger.info("Deployed!")

    return title + " successfully deployed!"
