using UnityEditor;
using UnityEngine;

public class assetBundler : MonoBehaviour
{
    static void Pack()
    {
        var bundleDir = "Assets/BundleAssets";
        var bundledDir = "Assets/streamingAssets";

        var newBundle = AssetImporter.GetAtPath(bundleDir);
        newBundle.assetBundleName = "newbundle";
        Debug.Log("Bundle created!");

        BuildPipeline.BuildAssetBundles(bundledDir,
            BuildAssetBundleOptions.None,
            BuildTarget.Android);
    }
}