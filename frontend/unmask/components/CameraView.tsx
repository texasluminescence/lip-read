import type React from "react"
import { useEffect, useRef } from "react"
import Webcam from "react-webcam"
import GuideLines from "./GuideLines"

interface CameraViewProps {
  hasCameraPermission: boolean
  isRecording: boolean
  guideLinesActive: boolean
  onFrame: (imageSrc: string) => void
}

const CameraView: React.FC<CameraViewProps> = ({ hasCameraPermission, isRecording, guideLinesActive, onFrame }) => {
  const webcamRef = useRef<Webcam>(null)

  useEffect(() => {
    if (!hasCameraPermission || !isRecording) return

    const frameCaptureInterval = window.setInterval(() => {
      const imageSrc = webcamRef.current?.getScreenshot()
      if (imageSrc) {
        onFrame(imageSrc)
      }
    }, 100)

    return () => {
      clearInterval(frameCaptureInterval)
    }
  }, [isRecording, hasCameraPermission, onFrame])

  return (
    <div
      style={{
        position: "relative",
        aspectRatio: "16 / 9",
        backgroundColor: "#283618",
        borderRadius: "0.75rem",
        overflow: "hidden",
        boxShadow: "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)",
        marginBottom: "1rem",
      }}
    >
      {!hasCameraPermission ? (
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#dda15e",
            textAlign: "center",
            padding: "1rem",
          }}
        >
          <p>Camera permission not granted</p>
        </div>
      ) : (
        <div style={{ position: "relative", width: "100%", height: "100%" }}>
          <Webcam
            ref={webcamRef}
            audio={false}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
            screenshotFormat="image/jpeg"
            videoConstraints={{
              facingMode: "user",
            }}
          />
          <GuideLines guideLinesActive={guideLinesActive} />
        </div>
      )}
    </div>
  )
}

export default CameraView
