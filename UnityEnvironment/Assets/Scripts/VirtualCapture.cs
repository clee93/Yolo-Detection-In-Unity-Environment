using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Threading;

//https://github.com/Siliconifier/Python-Unity-Socket-Communication

public class VirtualCapture : MonoBehaviour
{
    public Camera camera;
    public Vector2Int resolution;

    int numToSendToPython = 0;
    UdpSocket udpSocket;
    // Start is called before the first frame update
    void Start()
    {
        udpSocket = FindObjectOfType<UdpSocket>();
        InvokeRepeating("StreamImage", 0f, 0.03f);  //1s delay, repeat every 1s

        //RenderTexture rt = new RenderTexture(resolution.x, resolution.y, 24);
        //camera.targetTexture = rt;
        //RenderTexture.active = rt;
    }

    // Update is called once per frame
    void StreamImage()
    {
        //SendToPython();
        udpSocket.SendData(RenderImg(camera, resolution.x, resolution.y));
    }
    byte[] RenderImg(Camera camera, int resWidth, int resHeight)
    {
        RenderTexture rt = new RenderTexture(resWidth, resHeight, 24);
        camera.targetTexture = rt;
        Texture2D screenShot = new Texture2D(resWidth, resHeight, TextureFormat.ARGB32, false);
        camera.Render();
        RenderTexture.active = rt;
        screenShot.ReadPixels(new Rect(0, 0, resWidth, resHeight), 0, 0);
        camera.targetTexture = null;
        RenderTexture.active = null; // Just In Case, to avoid errors
        byte[] bytes = screenShot.EncodeToJPG();

        Destroy(rt);
        Destroy(screenShot);
        return (bytes);
    }

    public void SendToPython()
    {
        udpSocket.SendData("Sent From Unity: " + numToSendToPython.ToString());
        numToSendToPython++;
    }
}
