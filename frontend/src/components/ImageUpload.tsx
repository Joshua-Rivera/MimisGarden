import {useState} from "react";
import PredictionCard from "./PredictionCard.jsx";

export default function ImageUpload() {
    // stores image file the user selects
    const [selectedFile, setSelectedFile] = useState(null);

    //stores image preview link
    const [previewUrl, setPreviewUrl] = useState("");

    //stores prediction result
    const [prediction, setPrediction] = useState(null);

    //runs when user chooses an image
    function handleFileChange(event) {
        const file = event.target.files[0];

        if (!file){return;}

        //saves selected file
        setSelectedFile(file);

        //creates preview of selected img
        setPreviewUrl(URL.createObjectURL(file));

        //clears old prediction when new img is chosen
        setPrediction(null);
    }
}