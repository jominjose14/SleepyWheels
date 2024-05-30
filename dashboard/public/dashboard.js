const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

function getMonthName(monthNumber) {
  if (monthNumber < 1 || monthNumber > 12) return "Invalid";
  return months[monthNumber - 1];
}

function generateRowFromTimestamp(timestamp) {
  const year = timestamp.substr(0, 4);
  const day =
    getMonthName(timestamp.substr(5, 2)) + " " + timestamp.substr(8, 2);
  const time = timestamp.substr(11);

  return `
    <div>${year}</div>
    <div>${day}</div>
    <div>${time}</div>
  `;
}

function populateTable(tableId, data) {
  const $table = document.getElementById(tableId);
  $table.innerHTML = "";

  if (data == null) {
    $table.innerHTML = `
            <div style='color: #999;'>An</div>
            <div style='color: #999;'>Error</div>
            <div style='color: #999;'>Occurred</div>
        `;
  } else if (data.length == 0) {
    $table.innerHTML = `
        <div></div>
        <div style='color: #999;'>Empty</div>
        <div></div>
    `;
  } else {
    let rowsHtml = "";
    for (let i = data.length - 1; i >= 0; i--) {
      rowsHtml += generateRowFromTimestamp(data[i].timestamp);
    }
    $table.innerHTML = rowsHtml;
  }
}

async function populateTables() {
  try {
    const response = await fetch("/alarm");
    const responseJson = await response.json();
    populateTable("alarms-table", responseJson.data);
  } catch (e) {
    console.log("Error while filling alarms table");
    populateTable("alarms-table", null);
  }

  try {
    const response = await fetch("/yawn");
    const responseJson = await response.json();
    populateTable("yawns-table", responseJson.data);
  } catch (e) {
    console.log("Error while filling yawns table");
    populateTable("yawns-table", null);
  }
}

populateTables();
