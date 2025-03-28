import { useEffect, useState } from "react";
import axios from "axios";
import "./Profile.css";
import profile from "../assets/profile.png";

function Profile() {
    const [user, setUser] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const mockData = {
            first_name: "John",
            last_name: "Doe",
            email: "a@gmail.com"
        };
        setUser(mockData);
        setLoading(false);
    }, []);

    // useEffect(() => {
    //     // You can mock the user data here
    //     const data = {
    //         first_name: "John",
    //         last_name: "Doe",
    //         email: "a@gmail.com"
    //     };

    //     setUser(data);  // Update state with mock data

    //     // If you're mocking data, no need to perform an axios call
    //     setLoading(false);  // Assuming loading is false after setting the mock data

    // }, []);  // Empty dependency array ensures this runs once when the component mounts

    // If data is still loading, show a loading message
    if (loading) return <p>Loading...</p>;

    // If there was an error in setting the user data (not applicable here), show an error
    if (error) return <p className="error">{error}</p>;

    return (
        <div className="profile-container" id="profile">
            <img src={profile} alt="Profile" className="profile-image" />
            <div className="profile-info">
                <h1>Profile</h1>
                <h2>{user?.first_name} {user?.last_name}</h2>
                <h2>Email: {user?.email}</h2>
            </div>
        </div>
    );
}

export default Profile;
