const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getForecasts(){
  const r = await fetch(`${API}/forecasts/`);
  if(!r.ok) throw new Error(`Failed to fetch forecasts: ${r.status}`);
  return r.json();
}

export async function generateForecast(id){
  const r = await fetch(`${API}/forecasts/product/${id}`,{method: "POST"});
  return r.json();
}