import { Text, View } from "react-native";
import CameraView from "@/components/CameraView";
import { useState } from "react";
import { ScrollView } from "react-native-gesture-handler";

export default function Body() {
  const [cameraOpen, setCameraOpen] = useState(true);
  const [videoFrames, setVideoFrames] = useState<string[]>([]);
  const [transcript, setTranscript] = useState<string[]>(["Hello", "World!"]);
  return (
    <ScrollView
      contentContainerStyle={{
        flexGrow: 1,
        padding: 10,
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      <div style={{ width: '60vw', height: '60vw', position: 'relative' }}>
        <CameraView cameraOpen={cameraOpen} setVideoFrames={setVideoFrames} />
        <div style={{ position: 'absolute', bottom: '125px', left: '0', right: '0', backgroundColor: 'gray', textAlign: 'center' }}>
          {...transcript}
        </div>
      </div>
      <button style={{ width: '240px', height: '40px'}}>
        <span 
          style={{ fontSize: '25px' }}
          onClick={() => {setCameraOpen(prev => !prev);}}
        >
          {cameraOpen ? "Close Camera" : "Open Camera"}
        </span>
      </button>
      <div style={{ marginTop: '50px' }}>
        <h3 style={{ textAlign: 'center' }}> Latest 75 Frames </h3>
        {<div style={{ 
            height: '100%', 
            display: 'flex', 
            flexDirection: 'row', 
            flexWrap: 'wrap', 
            padding: '10', 
            justifyContent: 'center' 
        }}>
          {videoFrames.slice(0, 75).map((frame, index) => {
            return <div key={index} style={{ display: 'flex', flexDirection: 'column', margin: 5 }}> 
              <span>frame: {videoFrames.length - index}</span>
              <img 
                src={frame}
                style={{ height: '150px', width: '200px' }}
              />
            </div>
          })}
        </div>}
      </div>
    </ScrollView>
  );
}
