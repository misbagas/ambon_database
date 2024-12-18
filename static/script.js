// document.getElementById('weather-form').addEventListener('submit', async (e) => {
//     e.preventDefault();

//     const location = document.getElementById('location').value;
//     const response = await fetch(`/weather?location=${location}`);
//     const data = await response.json();

//     const weatherResult = document.getElementById('weather-result');
//     if (response.ok) {
//         weatherResult.innerHTML = `
//             <h2>Weather in ${data.location}</h2>
//             <p>Temperature: ${data.temperature}°C</p>
//             <p>Humidity: ${data.humidity}%</p>
//             <p>Wind Speed: ${data.wind_speed} km/h</p>
//         `;
//     } else {
//         weatherResult.innerHTML = `<p>Error: ${data.error}</p>`;
//     }
// });
