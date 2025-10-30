import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

function EmploymentChart({ data }) {
  if (!data || data.length === 0) return null;

  // Sort data by month for proper timeline display
  const sortedData = [...data].sort((a, b) => {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const aIndex = months.indexOf(a.month);
    const bIndex = months.indexOf(b.month);
    return aIndex - bIndex;
  });

  const labels = sortedData.map(item => `${item.month} ${item.fin_year}`);
  const householdsData = sortedData.map(item => item.total_households_worked);
  const individualsData = sortedData.map(item => item.total_individuals_worked);
  const womenData = sortedData.map(item => item.women_persondays);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Total Households Worked',
        data: householdsData,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Total Individuals Worked',
        data: individualsData,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
      {
        label: 'Women Persondays',
        data: womenData,
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Employment Data Over Time',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Count',
        },
      },
    },
  };

  return <Bar data={chartData} options={options} />;
}

function ExpenditureChart({ data }) {
  if (!data || data.length === 0) return null;

  // Sort data by month for proper timeline display
  const sortedData = [...data].sort((a, b) => {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const aIndex = months.indexOf(a.month);
    const bIndex = months.indexOf(b.month);
    return aIndex - bIndex;
  });

  const labels = sortedData.map(item => `${item.month} ${item.fin_year}`);
  const totalExpData = sortedData.map(item => item.total_exp);
  const wagesData = sortedData.map(item => item.wages);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Total Expenditure (₹ lakhs)',
        data: totalExpData,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1,
      },
      {
        label: 'Wages (₹ lakhs)',
        data: wagesData,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Expenditure Over Time',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Amount (₹ lakhs)',
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
}

export { EmploymentChart, ExpenditureChart };