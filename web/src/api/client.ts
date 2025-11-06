import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' }
});

export interface LoginResponse {
  access_token: string;
  user: {
    user_id: string;
    name: string;
    email: string;
  };
}

export const login = async (email: string) => {
  const response = await client.post<LoginResponse>('/auth/login', {
    email,
    otp: '123456'
  });
  return response.data;
};

export default client;
