import { useEffect, useState } from "react";
import { UserDetailsApi } from "../services/Api";
import NavBar from "../components/NavBar";
import { logout, isAuthenticated } from "../services/Auth";
import { useNavigate, Navigate } from "react-router-dom";
import axios from "axios"; // Ensure axios is imported correctly

export default function DashboardPage() {
    const navigate = useNavigate();

    const [user, setUser] = useState({ name: "", email: "", localId: "" });
    const [searchQuery, setSearchQuery] = useState("");
    const [videos, setVideos] = useState([]);

    useEffect(() => {
        if (isAuthenticated()) {
            UserDetailsApi().then((response) => {
                setUser({
                    name: response.data.users[0].displayName,
                    email: response.data.users[0].email,
                    localId: response.data.users[0].localId,
                });
            });
        }
    }, []);

    const logoutUser = () => {
        logout();
        navigate("/login");
    };
    
    const handleSearch = () => {
        // Make an API call to Flask when the submit button is clicked
        console.log(searchQuery);
        axios.post('http://localhost:5000/search', {
            search_query: searchQuery
        })
        .then(response => {
            setVideos(response.data);
            console.log(response.data)
        })
        .catch(error => {
            console.error('Error fetching videos:', error);
        });
    };
    if (!isAuthenticated()) {
        return <Navigate to="/login" />;
    }

    return (
        <div>
            <NavBar logoutUser={logoutUser} />
            <main role="main" className="container mt-5">
                <div className="container">
                    <div className="text-center mt-5">
                        <label>
                            Search: <input
                                name="myInput"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </label>
                        <button type="submit" onClick={handleSearch}>Submit</button>
                    </div>
                </div>
                
                <div>
                    {videos.map((video, index) => (
                        <div key={index}>
                           <h3>{video.title}</h3>
                            <p>Views: {video.views}</p>
                            <p>Likes: {video.likes}</p>
                            <p>Comments: {video.comments}</p>
                            <a href={video.url}>Watch Video</a>
                        </div>
                    ))}
                </div>
            </main>
        </div>
    );
}
