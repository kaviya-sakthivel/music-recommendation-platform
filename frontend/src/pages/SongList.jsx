import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axiosConfig";

export default function SongList() {
  const navigate = useNavigate();
  const [songs, setSongs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const res = await api.get("/songs/");
        setSongs(res.data);
      } catch (err) {
        setError("Failed to load songs");
      } finally {
        setLoading(false);
      }
    };
    fetchSongs();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-3xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800">🎵 SoundSphere</h1>
          <button
            onClick={handleLogout}
            className="text-sm text-red-600 hover:underline"
          >
            Logout
          </button>
        </div>

        {loading && <p className="text-gray-500">Loading songs...</p>}
        {error && <p className="text-red-500">{error}</p>}

        <div className="space-y-3">
          {songs.map((song) => (
            <div
              key={song.id}
              className="bg-white p-4 rounded-lg shadow-sm flex justify-between items-center hover:shadow-md transition"
            >
              <div>
                <h2 className="font-semibold text-gray-800">{song.title}</h2>
                <p className="text-sm text-gray-500">
                  {song.artist} {song.genre && `• ${song.genre}`}
                </p>
              </div>
              <span className="text-sm text-gray-400">
                {song.duration ? `${Math.floor(song.duration / 60)}:${String(song.duration % 60).padStart(2, "0")}` : ""}
              </span>
            </div>
          ))}
        </div>

        {!loading && songs.length === 0 && !error && (
          <p className="text-gray-500 text-center mt-10">No songs found.</p>
        )}
      </div>
    </div>
  );
}