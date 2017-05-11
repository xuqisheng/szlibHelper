function formatTime(date) {
  var year = date.getFullYear()
  var month = date.getMonth() + 1
  var day = date.getDate()

  var hour = date.getHours()
  var minute = date.getMinutes()
  var second = date.getSeconds()


  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

function formatNumber(n) {
  n = n.toString()
  return n[1] ? n : '0' + n
}

module.exports = {
  formatTime: formatTime,
  fetchSzlibCover: fetchSzlibCover,
  getRemainDays: getRemainDays,
  getReturnDate: getReturnDate,
  calSelectDateString: calSelectDateString,
  transDateString: transDateString,
  isEmptyObject: isEmptyObject
}

function isEmptyObject(e) {
  var t;
  for (t in e)
    return !1;
  return !0
}  

function fetchSzlibCover(object) {
  // GET http://202.112.150.126/index.php?client=szlib&isbn=978-7-301-18331-1/cover HTTP/1.1
  wx.downloadFile({
      url: 'https://www.jiangfuqiang.cn/getSzlibCover/' + object.isbn + ".jpg",
      header: {
          'content-type': 'application/x-www-form-urlencoded'
      },
      success: function(res) {
        console.log(res);
        var coverPath = res.tempFilePath;
        // save it, 14kb per cover picture
        wx.saveFile({
          tempFilePath: coverPath,
          success: function(res) {
            var savedFilePath = res.savedFilePath
          }
        });
        // update UI
        object.success(coverPath);
      },
      failed: function(res) {
        console.log("fetch cover "+ isbn + " failed");
      }
    });
}

function calSelectDateString(selected) {
  var begin = new Date();
  if (selected == 1) {
    begin.setMonth(begin.getMonth()-3);
  } else if (selected == 2) {
    begin.setFullYear(begin.getFullYear()-1);
  } else if (selected == 3) {
    begin.setFullYear(begin.getFullYear() - 3);
  }
  return [stringFromDate(begin), stringFromDate(new Date())];
}

function stringFromDate(currentDate) {
  var month = currentDate.getMonth() + 1;
  var monthStr = "" + month;
  if (month<10) {
    monthStr = "0" + monthStr;
  }
  var dateStr = "" + currentDate.getDate()
  if (currentDate.getDate()<10) {
    dateStr = "0" + dateStr;
  }
  var fin = currentDate.getFullYear() + '-' + monthStr + '-' + dateStr;
  console.log("fin date str: " + fin);
  return fin;
}

function getReturnDate(returnDateNum) {
  var dateStr = "" + returnDateNum;
  var year = dateStr.substr(0,4);
  var month = dateStr.substr(4,2);
  var day = dateStr.substr(6, 2);
  return year + '-' + month + '-' + day
}

function transDateString(dateStr) {
  return dateStr.substr(0, 4) + dateStr.substr(5, 2) + dateStr.substr(8, 2);
}

function getRemainDays(returnDateNum) {
  var dateStr = "" + returnDateNum;
  var month = "" + dateStr.substr(4,2)-1;
  var returndate = new Date(dateStr.substr(0,4), month, dateStr.substr(6,2));
  //console.log("the return date: " + returndate);
  var currentdate = new Date();
  var days = Math.round((returndate - currentdate)/(1000*60*60*24));
  //console.log("the days: " + days);
  return days;
}
