const envBase = window.APP_API_BASE_URL || "";

export const config = {
  apiBaseUrl: envBase || "http://localhost:5000",
  minWpm: 250,
  maxWpm: 1000,
};
