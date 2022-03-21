using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

[DisallowMultipleComponent]
public class WebcamManager : MonoBehaviour
{

	[System.NonSerialized] public int currentCamera = -1;
	[System.NonSerialized] public WebCamTexture WebCamTexture;

	public UnityEvent OnCameraChange;


	// Start is called before the first frame update
	void Start()
	{
		WebCamTexture = new WebCamTexture();
		ChangeCamera();
	}

	public void ChangeCamera()
	{
		if (WebCamTexture.devices.Length <= 0)
		{
			Debug.LogError("No Webcam devices were found");
		}

		currentCamera += 1;
		if (currentCamera >= WebCamTexture.devices.Length)
			currentCamera = 0;

		if (WebCamTexture)
			WebCamTexture.Stop();

		WebCamTexture.deviceName = WebCamTexture.devices[currentCamera].name;
		WebCamTexture.Play();
		OnCameraChange.Invoke();
	}

	public void UpdateText(Text text)
	{
		text.text = "Switch Camera:\n\nUsing '" + WebCamTexture.deviceName + "'";
	}

	public void UpdateTexture(RawImage rawImage)
	{
		rawImage.texture = WebCamTexture;
	}

	// Update is called once per frame
	void Update()
	{
		
	}
}
