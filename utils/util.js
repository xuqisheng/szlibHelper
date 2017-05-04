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
  fetchSzlibCover: fetchSzlibCover
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
        coverPath = res.tempFilePath;
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