import type React from "react"
import { useRef, useEffect, useState } from "react"

interface SideBarProps {
  transcription: string[]
  videoFrames: string[]
}

const SideBar: React.FC<SideBarProps> = ({ transcription, videoFrames }) => {
  const transcriptionRef = useRef<HTMLInputElement>(null);
  const [isAtBottom, setIsAtBottom] = useState<Boolean>(true)

  const checkIfAtBottom = () => {
    const container = transcriptionRef.current;
    if (container) {
        const isAtBottom =
            container.scrollHeight - container.scrollTop === container.clientHeight;
        setIsAtBottom(isAtBottom);
    }
  };

  useEffect(() => {
    if (transcriptionRef && transcriptionRef.current) {
      const container = transcriptionRef.current;
      if (isAtBottom) {
        container.scrollTo({
          top: container.scrollHeight,
          behavior: 'smooth'
        });
      }
    }
  }, [transcriptionRef?.current?.scrollHeight])

  useEffect(() => {
    const elem = transcriptionRef.current
    if (elem) {

    }
  }, [transcription])
  return (
    <div
      style={{
        flex: "1",
        padding: "2rem",
        borderLeft: "1px solid #bc6c25",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <h2
        style={{
          fontSize: "1.5rem",
          fontWeight: "600",
          color: "#606c38",
          marginBottom: "1rem",
        }}
      >
        Transcription
      </h2>
      <div
        ref={transcriptionRef}
        onScrollCapture={checkIfAtBottom}
        style={{
          flex: "1",
          backgroundColor: "rgba(40, 54, 24, 0.1)",
          borderRadius: "0.75rem",
          paddingTop: "1rem",
          paddingBottom: "1rem",
          paddingLeft: "1.5rem",
          paddingRight: "1.5rem",
          overflowY: "auto",
          marginBottom: "1rem",
        }}
      >
        <div style={{ height: "8rem", width: "100%" }}>
          <p
            style={{
              fontSize: "1.125rem",
              color: "#283618",
              lineHeight: "1.75",
              whiteSpace: "pre-wrap",
              overflowY: "auto"
            }}
          >
            {transcription.join(" ")}
          </p>
        </div>
      </div>
      <div>
        <h3
          style={{
            fontSize: "1.25rem",
            fontWeight: "600",
            color: "#606c38",
            marginBottom: "0.5rem",
          }}
        >
          Latest 5 Frames
        </h3>
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "0.5rem",
            minHeight: "96px",
            justifyContent: "center",
          }}
        >
          {videoFrames.map((frame, index) => (
            <div
              key={index}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <span
                style={{
                  fontSize: "0.875rem",
                  color: "#283618",
                  marginBottom: "0.25rem",
                }}
              >
                frame: {videoFrames.length - index}
              </span>
              <img
                src={frame || "/placeholder.svg"}
                alt={`Frame ${videoFrames.length - index}`}
                style={{
                  height: "75px",
                  width: "100px",
                  objectFit: "cover",
                  borderRadius: "0.25rem",
                }}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default SideBar