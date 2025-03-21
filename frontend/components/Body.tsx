import React, { useState, useEffect } from "react"
import CameraView from "./CameraView"
import SideBar from "./SideBar"
import { FaRegEye } from "react-icons/fa";
import { FaRegEyeSlash } from "react-icons/fa";

export default function Body() {
  const [isRecording, setIsRecording] = useState(false)
  const [guideLinesActive, setGuideLinesActive] = useState(true)
  const [transcription, setTranscription] = useState<string[]>([])
  const [hasCameraPermission, setHasCameraPermission] = useState(false)
  const [videoFrames, setVideoFrames] = useState<string[]>([])

  useEffect(() => {
    const checkCameraPermission = async () => {
      try {
        await navigator.mediaDevices.getUserMedia({ video: true })
        setHasCameraPermission(true)
      } catch (error) {
        setHasCameraPermission(false)
        console.error("Error accessing camera:", error)
      }
    }

    checkCameraPermission()
  }, [])

  useEffect(() => {
    if (!isRecording) return

    // simulating token streaming for transcription
    const transcriptionInterval = setInterval(() => {
      setTranscription((prev) => [...prev, "word"])
    }, 200)

    return () => {
      clearInterval(transcriptionInterval)
    }
  }, [isRecording])

  const handleFrame = (imageSrc: string) => {
    setVideoFrames((prevFrames) => [imageSrc, ...prevFrames.slice(0, 149)])
  }

  const toggleRecording = () => {
    if (!isRecording)
      setTranscription([])
    setIsRecording(!isRecording)
  }

  return (
    <div
      style={{
        height: "100vh",
        width: "100%",
        backgroundColor: "#fefae0",
        color: "#283618",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "2rem",
      }}
    >
      <h1
        style={{
          fontSize: "3rem",
          fontWeight: "bold",
          color: "#606c38",
          marginBottom: "2rem",
        }}
      >
        LipSeek
      </h1>

      <div
        style={{
          display: "flex",
          width: "100%",
          maxWidth: "1300px",
          backgroundColor: "rgba(221, 161, 94, 0.1)",
          boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
          borderRadius: "1rem",
          overflow: "hidden",
          backdropFilter: "blur(10px)",
          border: "1px solid #bc6c25",
        }}
      >
        <div
          style={{
            flex: "1",
            padding: "2rem",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <CameraView 
            hasCameraPermission={hasCameraPermission} 
            isRecording={isRecording} 
            guideLinesActive={guideLinesActive}
            onFrame={handleFrame} 
          />
          <div style={{ display: "flex", width: "100%", flexDirection: "row", justifyContent: "center" }}>
            <button
              onClick={toggleRecording}
              disabled={!hasCameraPermission}
              style={{
                padding: "0.75rem",
                fontSize: "1.125rem",
                fontWeight: "600",
                width: "85%",
                color: "#fefae0",
                backgroundColor: isRecording ? "#bc6c25" : "#606c38",
                border: "none",
                borderRadius: "0.5rem",
                cursor: "pointer",
                transition: "background-color 0.3s ease",
              }}
            >
              {isRecording ? "Stop Recording" : "Start Recording"}
            </button>
            <button
            onClick={() => { setGuideLinesActive(!guideLinesActive) }}
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                padding: "0.75rem",
                fontSize: "1.125rem",
                fontWeight: "600",
                marginLeft: "0.5rem",
                width: "10%",
                color: "#fefae0",
                backgroundColor: !guideLinesActive ? "#bc6c25" : "#606c38",
                border: "none",
                borderRadius: "0.5rem",
                cursor: "pointer",
                transition: "background-color 0.3s ease",
              }}
            >
              {guideLinesActive ? 
                <FaRegEyeSlash style={{ width: "100%" }} /> : 
                <FaRegEye style={{ width: "100%" }} />
              }
            </button>
          </div>
        </div>

        <SideBar transcription={transcription} videoFrames={videoFrames.slice(0, 5)} />
      </div>
    </div>
  )
}
