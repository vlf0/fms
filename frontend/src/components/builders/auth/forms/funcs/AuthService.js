const API_BASE_URL = process.env.REACT_APP_API_HOST;

console.log(API_BASE_URL)

export const loginUser = async (name, password) => {

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/login`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, password }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Login failed");
    }

    return { success: true, message: "Login successful!" };
  } catch (error) {
    return { success: false, message: error.message };
  }
};


export const checkAuth = async () => {

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/check_user`, {
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error("Not authenticated");
    }

    return { success: true, message: "User is authenticated" };
  } catch (error) {
    return { success: false, message: error.message };
  }
};
