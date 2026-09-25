import { useEffect, useState } from "react";
import { getForecasts } from "../api/forecasts";

export default function Forecasts(){
  const [data, setData] = useState([]);
  useEffect(() => {
    getForecasts().then(setData);
  },[]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">
        Demand Forecasting
      </h1>
      <div className="grid gap-4">
        {data.map(f=>(
          <div key={f.id} className="border rounded-lg p-4">
            <h2 className="font-bold">
              Product #{f.product_id}
            </h2>

            <p>
              Daily Demand: {f.daily_demand.toFixed(2)}
            </p>
            <p>
              Stockout: {f.stockout_date || "No projected stockout"}
            </p>
            <p>
              Reorder: {f.reorder_quantity}
            </p>
            <p>
              Confidence: {f.confidence}
            </p>
            <p>
              History Start: {f.history_start}
            </p>
            <p>
              History End: {f.history_end}
            </p>
            <p>
              Refreshed: {new Date(f.created_at).toLocaleString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}