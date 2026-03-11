/**
 * Central API client for backend calls.
 * Base URL and auth token are configured here for reuse across the app.
 */

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

const AUTH_TOKEN_KEY = "authToken";
const USER_ID_KEY = "userId";

export function getToken() {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

export function setAuth(userId, token) {
  if (userId) localStorage.setItem(USER_ID_KEY, userId);
  if (token) localStorage.setItem(AUTH_TOKEN_KEY, token);
}

export function clearAuth() {
  localStorage.removeItem(USER_ID_KEY);
  localStorage.removeItem(AUTH_TOKEN_KEY);
}

export function getUserId() {
  return localStorage.getItem(USER_ID_KEY);
}

export function isAuthenticated() {
  return !!getToken();
}

/**
 * POST request to an API path (e.g. "/api/signin").
 * @param {string} path - Path without base URL (e.g. "/api/signin")
 * @param {object} body - JSON body
 * @param {boolean} useAuth - If true, send Authorization: Bearer <token>
 * @returns {Promise<{ ok: boolean, data: object, status: number }>}
 */
export async function post(path, body, useAuth = false) {
  const url = `${BASE_URL}${path}`;
  const headers = {
    "Content-Type": "application/json",
  };
  if (useAuth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }
  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });
  const data = await response.json().catch(() => ({}));
  return { ok: response.ok, data, status: response.status };
}

/**
 * GET request (for future use).
 */
export async function get(path, useAuth = false) {
  const url = `${BASE_URL}${path}`;
  const headers = {};
  if (useAuth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }
  const response = await fetch(url, { method: "GET", headers });
  const data = await response.json().catch(() => ({}));
  return { ok: response.ok, data, status: response.status };
}

export default { BASE_URL, getToken, setAuth, clearAuth, getUserId, isAuthenticated, post, get };
