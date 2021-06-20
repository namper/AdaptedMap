import { useEffect, useRef, useState } from "react";
import Webcam from "webcam-easy";

export const Camera = ({ addMarkerToMap }) => {
  const [picture, setPicture] = useState(null);
  const webcamElement = useRef(null);
  const canvasElement = useRef(null);
  const snapSoundElement = useRef(null);
  console.log("webcamelement ", webcamElement.current);
  const webCamRef = useRef(null);
  useEffect(() => {
    webCamRef.current = new Webcam(
      webcamElement.current,
      "environment",
      canvasElement.current,
      snapSoundElement.current
    );

    webCamRef.current
      .start()
      .then((result) => {
        webCamRef.current.className = "webcam-wrapper";
        console.log("webcamred", webCamRef.current);
        console.log("webcam started");
      })
      .catch((err) => {
        console.log(err);
      });

    const app = document.getElementById("App");
    app.style.backgroundColor = "black";
  }, []);

  return (
    <>
      {!picture && (
        <>
          <video
            id="webcam"
            ref={webcamElement}
            autoplay
            playsinline
            className="take-video-wrapper"
          ></video>
          <canvas id="canvas" ref={canvasElement} class="d-none"></canvas>
          <audio
            id="snapSound"
            ref={snapSoundElement}
            src="audio/snap.wav"
            preload="auto"
          ></audio>
        </>
      )}

      {console.log("picture========", picture)}

      {!picture && (
        <button
          style={{
            position: "fixed",
            width: "100px",
            height: "19px",
            bottom: 0,
            height: "50px",
            width: "80vw",
            bottom: "5vh",
            borderRadius: "50px",
          }}
          onClick={() => {
            // webCamRef.current.flip({ facingMode: "enviroment" });
            let picture = webCamRef.current.snap();
            // document.querySelector("#download-photo").href = picture;

            document.querySelector("#download-photo").src = picture;
            const img = document.getElementById("download-photo");
            img.style.display = "block";
            webCamRef.current.stop();
            console.log("---", picture);
            setPicture(picture);
          }}
        >
          take photo
        </button>
      )}

      <img id="download-photo" />
      {picture && (
        <div
          style={{
            width: "100%",
            height: "50px",
            position: "fixed",
            bottom: 0,
            display: "flex",
            justifyContent: "space-between",
          }}
        >
          <div style={{ padding: 10, color: "white" }}>გაუქმება</div>
          <div
            style={{ padding: 10, color: "white" }}
            onClick={() => addMarkerToMap(picture)}
          >
            ატვირთვა
          </div>
        </div>
      )}
    </>
  );
};
