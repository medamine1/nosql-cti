import axios from "axios";

export async function logoutApi(token) {
  return axios.post(
    "/api/logout",
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
}
