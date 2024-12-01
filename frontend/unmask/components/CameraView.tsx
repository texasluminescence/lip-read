import React, { useEffect, useRef, useState } from 'react';
import Webcam from 'react-webcam';

const CameraView: React.FC<{ cameraOpen: boolean, setVideoFrames: React.Dispatch<React.SetStateAction<string[]>> }> = ({ cameraOpen, setVideoFrames }) => {
    const [hasCameraPermission, setHasCameraPermission] = useState(false);
    const [videoStream, setVideoStream] = useState<MediaStream | null>(null);
    const webcamRef = useRef<Webcam>(null);

    useEffect(() => {
        const checkCameraPermission = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                setHasCameraPermission(true);
                setVideoStream(stream);
            } catch (error) {
                setHasCameraPermission(false);
                console.error('Error accessing camera:', error);
            }
        };

        checkCameraPermission();
    }, []);

    useEffect(() => {
        if (!hasCameraPermission)
            return;
        let frameCaptureInterval: number | null = null;
        if (cameraOpen && webcamRef.current) {
            frameCaptureInterval = window.setInterval(() => {
                const imageSrc = webcamRef.current?.getScreenshot();
                if (imageSrc) // stores latest frame
                    setVideoFrames(prevFrames => [imageSrc, ...prevFrames]);
            }, 100);
        } else {
            // stop if !cameraOpen or webcam disappears
            if (frameCaptureInterval) // make typescript happy
                clearInterval(frameCaptureInterval);
        }

        return () => {
            if (frameCaptureInterval)
                clearInterval(frameCaptureInterval);
        };
    }, [cameraOpen, hasCameraPermission]);

    return (
        <div style={{ display: 'inline-block', width: '100%', height: '100%' }}>
            {hasCameraPermission && cameraOpen && <Webcam
                ref={webcamRef}
                audio={false}
                style={{ width: '100%', height: '100%' }}
                screenshotFormat="image/jpeg"
                videoConstraints={{
                    facingMode: 'user',
                }}
            />}
        </div>
    );
};

export default CameraView;