function doPost(e) {
  try {
    // Get the active sheet
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Get current date and time
    var now = new Date();
    var date = Utilities.formatDate(now, Session.getScriptTimeZone(), "yyyy-MM-dd");
    var time = Utilities.formatDate(now, Session.getScriptTimeZone(), "HH:mm:ss");
    
    // Determine time of day
    var hour = now.getHours();
    var timeOfDay = "Night";
    if (hour >= 5 && hour < 12) timeOfDay = "Morning";
    else if (hour >= 12 && hour < 17) timeOfDay = "Afternoon";
    else if (hour >= 17 && hour < 22) timeOfDay = "Evening";
    
    // Parse the incoming data
    var data = JSON.parse(e.postData.contents);
    var user_id = data.user_id;
    var username = data.username || "";
    var first_name = data.first_name || "";
    var last_name = data.last_name || "";
    var action = data.action;
    var details = data.details || {};
    
    // Get all data in the sheet
    var dataRange = sheet.getDataRange();
    var values = dataRange.getValues();
    
    // Find the last row for this user
    var lastUserRow = -1;
    for (var i = values.length - 1; i >= 1; i--) {
      if (values[i][4] == user_id) { // User ID is in column E (index 4)
        lastUserRow = i;
        break;
      }
    }
    
    // Prepare the row data
    var rowData = [
      date,                    // Date
      time,                    // Time
      timeOfDay,              // Time of Day
      user_id,                // User ID
      username,               // Username
      first_name,             // First Name
      last_name,              // Last Name
      action == "Bot Started" ? "Yes" : "", // Bot Started
      action == "Model Selected" ? "Yes" : "", // Model Selected
      details.Model || "",    // Model Name
      details.Duration || "", // Package Duration
      details.Price || "",    // Package Price
      action == "Order Confirmed" ? "Yes" : "", // Order Confirmed
      action == "Payment Initiated" ? "Yes" : "", // Clicked I Have Paid
      action == "Screenshot Sent" ? "Yes" : "", // Screenshot Sent
      action == "Payment Verified" ? "Success" : 
        action == "Payment Failed" ? "Failed" : "Pending", // Payment Status
      details.Feedback || "", // User Feedback
      details.Message || ""   // User Message
    ];
    
    // If this is a model or package selection, create a new row
    if (action == "Model Selected" || action == "Package Selected") {
      sheet.appendRow(rowData);
    } else {
      // For other actions, update the last row
      if (lastUserRow > 0) {
        var range = sheet.getRange(lastUserRow + 1, 1, 1, rowData.length);
        var currentData = range.getValues()[0];
        
        // Update only the changed values
        for (var i = 0; i < rowData.length; i++) {
          if (rowData[i] !== "") {
            currentData[i] = rowData[i];
          }
        }
        
        range.setValues([currentData]);
      } else {
        // If no previous row exists, create a new one
        sheet.appendRow(rowData);
      }
    }
    
    // Return success response
    return ContentService.createTextOutput(JSON.stringify({
      "status": "success",
      "message": "Data processed successfully"
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    // Return error response
    return ContentService.createTextOutput(JSON.stringify({
      "status": "error",
      "message": error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// Function to set up headers if they don't exist
function setupHeaders() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var headers = [
    "Date",
    "Time",
    "Time of Day",
    "User ID",
    "Username",
    "First Name",
    "Last Name",
    "Bot Started",
    "Model Selected",
    "Model Name",
    "Package Duration",
    "Package Price",
    "Order Confirmed",
    "Clicked I Have Paid",
    "Screenshot Sent",
    "Payment Status",
    "User Feedback",
    "User Message"
  ];
  
  // Check if headers exist
  if (sheet.getRange("A1").getValue() == "") {
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    // Format headers
    sheet.getRange(1, 1, 1, headers.length)
      .setBackground("#4285F4")
      .setFontColor("white")
      .setFontWeight("bold");
  }
}

// Run this function once to set up headers
function onOpen() {
  setupHeaders();
} 