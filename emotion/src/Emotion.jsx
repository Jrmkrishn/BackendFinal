/* eslint-disable react/prop-types */
import { useState } from "react";
import axios from "axios";

const Emotion = ({ username }) => {
  const [emotionResult, setEmotionResult] = useState("");

  const startAnalysis = async () => {
    const formdata = new FormData();
    formdata.append("username", username);
    try {
      const res = await axios.post(
        "http://localhost:8000/analyze_emotion",
        {},
        {
          headers: {
            "Content-Type": "application/json",
            username: username,
          },
        }
      );
      console.log(res);
      setEmotionResult(res.data.message);
    } catch (error) {
      console.error("Error starting emotion analysis:", error);
    }
  };

  const shutdown = async () => {
    try {
      const res = await axios.post("http://localhost:8000/shutdown");
      setEmotionResult(res.data.message);

      console.log("Server shutting down...");
    } catch (error) {
      console.error("Error shutting down server:", error);
    }
  };

  return (
    <div className="font-Oregano bg-gradient-to-r from-orange-400 to-yellow-500 bg-orange-400 w-full h-screen flex justify-center items-center flex-col">
      <h1 className="flex items-center font-bold tracking-tighter text-4xl">
        Interview Facial Detection Recognition
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="w-12 h-12"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M15.182 15.182a4.5 4.5 0 0 1-6.364 0M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0ZM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Z"
          />
        </svg>
      </h1>
      <div className="my-10 rounded-lg">
        <video id="video" className="rounded-lg" autoPlay></video>
      </div>
      <div className="text-2xl py-10 font-semibold">{emotionResult}</div>
      <div className="flex max-w-sm w-full justify-between text-slate-100">
        <button
          className="px-4 py-2 bg-zinc-900 rounded-lg"
          onClick={startAnalysis}
          disabled={false}
        >
          Start Meeting
        </button>
        <button
          className="px-4 py-2 bg-zinc-900 rounded-lg"
          onClick={shutdown}
          disabled={false}
        >
          Close Meeting
        </button>
      </div>
    </div>
  );
};

export default Emotion;
