import { useState, useEffect, useRef } from "react";
import "./App.css";

import Draggable from "react-draggable";
import { Resizable } from "react-resizable";

function App() {
  const refDraggable = useRef({});
  const [data, setData] = useState({ message: "view username" });
  const [size, setSize] = useState({ width: 200, height: 200 });

  const onResize = (event, { node, size, handle }) => {
    setSize({ width: size.width, height: size.height });
  };

  const [registerFromData, setRegisterFromData] = useState({
    email: "",
    password: "",
    name: "",
  });

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  useEffect(() => {
    const token = localStorage.getItem("jwt_webmarker");
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const getUserName = async () => {
    const token = localStorage.getItem("jwt_webmarker");

    const response = await fetch("http://localhost:8000/username", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    const data = (await response.json()) || { username: "No data" };
    setData(data);
  };

  const authenticate = async () => {
    const form = new URLSearchParams();
    form.append("username", formData.username);
    form.append("password", formData.password);

    const response = await fetch("http://localhost:8000/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: form,
    });
    const data = await response.json();
    if (data.access_token) {
      setIsAuthenticated(true);
    }
    localStorage.setItem("jwt_webmarker", data.access_token);
  };

  const logout = async () => {
    localStorage.removeItem("jwt_webmarker");
    setIsAuthenticated(false);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleChangeRegister = (e) => {
    const { name, value } = e.target;
    setRegisterFromData({
      ...registerFromData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    authenticate();
  };

  const register_new_user = async () => {
    fetch("http://localhost:8000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(registerFromData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        if (data.access_token) {
          setIsAuthenticated(true);
        }
        localStorage.setItem("jwt_webmarker", data.access_token);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleSubmitRegister = async (e) => {
    e.preventDefault();
    register_new_user();
  };

  return (
    <>
      <div style={{ position: "relative" }}>
        {!isAuthenticated && (
          <Draggable>
            <form
              onSubmit={handleSubmit}
              className="glass"
              ref={(el) => (refDraggable.current.form1 = el)}
            >
              <div style={{ margin: "10px" }}>
                <h2 style={{ color: "black" }}>Login Form</h2>
              </div>
              <div style={{ margin: "10px" }}>
                <input
                  className="inputFields"
                  type="text"
                  name="username"
                  onChange={handleChange}
                  value={formData.username}
                  placeholder="Email"
                />
              </div>
              <div style={{ margin: "10px" }}>
                <input
                  className="inputFields"
                  type="password"
                  name="password"
                  onChange={handleChange}
                  value={formData.password}
                  placeholder="Password"
                />
              </div>
              <button type="submit">Login</button>
            </form>
          </Draggable>
        )}
        {!isAuthenticated && (
          <Draggable>
            <form
              onSubmit={handleSubmitRegister}
              className="glass"
              ref={(el) => (refDraggable.current.form1 = el)}
            >
              <div style={{ margin: "10px" }}>
                <h2 style={{ color: "black" }}>Register Form</h2>
              </div>
              <div style={{ margin: "10px" }}>
                <input
                  className="inputFields"
                  type="text"
                  name="name"
                  onChange={handleChangeRegister}
                  value={registerFromData.name}
                  placeholder="Name"
                />
              </div>
              <div style={{ margin: "10px" }}>
                <input
                  className="inputFields"
                  type="text"
                  name="email"
                  onChange={handleChangeRegister}
                  value={registerFromData.username}
                  placeholder="Email"
                />
              </div>
              <div style={{ margin: "10px" }}>
                <input
                  className="inputFields"
                  type="password"
                  name="password"
                  onChange={handleChangeRegister}
                  value={registerFromData.password}
                  placeholder="Password"
                />
              </div>
              <button type="submit">Login</button>
            </form>
          </Draggable>
        )}
        {/* <Draggable> */}
        {isAuthenticated && (
          <Resizable
            height={size.height}
            width={size.width}
            onResize={onResize}
          >
            <div
              id="draggable"
              className="glass card"
              ref={(el) => (refDraggable.current.div1 = el)}
            >
              <button style={{ marginLeft: "10px" }} onClick={getUserName}>
                {data.username}
              </button>
              <button style={{ marginLeft: "10px" }} onClick={logout}>
                LogOut
              </button>
            </div>
          </Resizable>
        )}
        {/* </Draggable> */}
      </div>
    </>
  );
}

export default App;
