import React from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";

const StockChart = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="timestamp" tick={{ fontSize: 10 }} />
        <YAxis domain={["auto", "auto"]} />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="close" stroke="#8884d8" name="Close Price" />
        <Line type="monotone" dataKey="sma_5" stroke="#82ca9d" name="SMA-5" />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default StockChart;
