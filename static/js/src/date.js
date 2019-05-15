// Copy & Paste this
Date.prototype.getUnixTime = function() { return this.getTime()/1000|0 };
if(!Date.now) Date.now = function() { return new Date(); }
Date.time = function() { return Date.now().getUnixTime(); }

// Get the current time as Unix time
var currentUnixTime = Date.time();
currentUnixTime = Date.now().getUnixTime(); // same as above

// Parse a date and get it as Unix time
var parsedUnixTime = new Date('Mon, 25 Dec 1995 13:30:00 GMT').getUnixTime();
// parsedUnixTime==819898200