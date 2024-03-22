/* eslint-disable react/prop-types */
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = ({ username, setUserName }) => {
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(username);
    if (username.trim() === "") {
      setErrorMessage("Please enter a username.");
      return;
    }
    setErrorMessage("");
    console.log("Username:", username);
    navigate("/emotion")
  };

  return (
    <div className="font-Oregano flex justify-center items-center from-orange-400 to-yellow-500 bg-orange-400 h-screen">
      <form
        className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
        onSubmit={handleSubmit}
      >
        <div className="mb-6">
          <label
            className="block font-Oregano text-4xl text-gray-700  font-bold mb-2"
            htmlFor="username"
          >
            Username
          </label>
          <input
            className="shadow appearance-none border rounded text-2xl w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="username"
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUserName(e.target.value)}
            required
          />
        </div>
        <div className="flex items-center justify-between">
          <button
            className="from-orange-400 to-yellow-500 text-3xl bg-orange-400 hover:bg-zinc-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
          >
            Sign In
          </button>
        </div>
        {errorMessage && (
          <p className="text-red-500 text-xs italic mt-4">{errorMessage}</p>
        )}
      </form>
    </div>
  );
};

export default Login;
