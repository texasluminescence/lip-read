import type React from "react"

interface GuideLineProps {
    guideLinesActive: boolean
}

const GuideLines: React.FC<GuideLineProps> = ({ guideLinesActive }) => {
    return (
        <>
            <div style={{
                position: "absolute",
                display: `${guideLinesActive ? "inline" : "none"}`,
                top: "50%",
                left: 0,
                right: 0,
                width: "100%",
                height: "30%",
                borderTop: "2px dotted #bc6c25",
                borderBottom: "2px dotted #bc6c25",
                zIndex: 1
            }} />

            <div style={{
                position: "absolute",
                display: `${guideLinesActive ? "inline" : "none"}`,
                top: 0,
                left: "35%",
                right: 0,
                width: "30%",
                height: "100%",
                borderLeft: "2px dotted #bc6c25",
                borderRight: "2px dotted #bc6c25",
                zIndex: 1
            }} />
        </>
    )
}

export default GuideLines